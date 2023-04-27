<div align="center">

![Research](https://www.houstonmethodist.org/-/media/images/research/cancer-center/cancer_center_banner_1140x400.ashx?h=400&iar=0&mw=1382&w=1140&hash=28362AFB38ACA244FB16263E4AA3E267)
<h1><img src="https://img.icons8.com/color/512/pink-ribbon.png" width="30" height="30">
 Diagnosis API 
<img src="https://img.icons8.com/color/512/pink-ribbon.png" width="30" height="30">
</h1>

Docker containerized REST API to query data on Breast Cancer Diagnosis, with Redis NoSQL Database integration and public access deployment using Kubernetes.  
</div>

#

## Data Description
The Breast Cancer Wisconsin dataset includes data from hundreds of breast cancer cases to develop an effective diagnosis for future cases. 
For each case, the fine needle aspiration procedure was performed to take a sample from the cell nuclei present within the mass found on the body.

From the sample, various measurements were taken, including the area, texture, smoothness, and compactness.
Utilizing these measurements in the dataset, an effective and reliable diagnosis can be made to determine the outcome of each case and to predict the survival status based on these features.
<br><br>
<b>The dataset contains 32 attributes with information on:</b><br>
1. ID number
2. Diagnosis (M = malignant, B = benign)

Column 3-32 contains ten real-valued features are computed for each cell nucleus:
* radius (mean of distances from center to points on the perimeter)
* texture (standard deviation of gray-scale values)
* perimeter
* area
* smoothness (local variation in radius lengths)
* compactness (perimeter^2 / area - 1.0)
* concavity (severity of concave portions of the contour)
* concave points (number of concave portions of the contour)
* symmetry
* fractal dimension ("coastline approximation" - 1)

The mean, standard error, and "worst" or largest (mean of the three
largest values) of these features were computed for each image,
resulting in 30 features.  For instance, field 3 is Mean Radius, field
13 is Radius SE, field 23 is Worst Radius.

All feature values are recoded with four significant digits, with no missing attribute values and class distribution of 357 benign and 212 malignant.

The original dataset is available from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)), and detailed documentation is available on [University of Wisconsin-Madison](https://pages.cs.wisc.edu/~olvi/uwmp/cancer.html) research page.


## Implementation
The project uses **Python 3.8.10**, in particular **Flask 2.2.2** for REST API development, **Redis 7** for NoSQL Database, and **Docker 20.10.12** for containerization. Kubernetes is used for container ochestration and deployment. 

### Files
The file structure of this project is as below:
```
Diagnosis_API/
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.wrk
│   └── docker-compose.yml
├── kubernetes/
│   ├── deployment-python-debug.yml
│   └── prod
│       ├── app-prod-api-deployment.yml
│       ├── app-prod-api-ingress.yml
│       ├── app-prod-api-nodeport.yml
│       ├── app-prod-api-service.yml
│       ├── app-prod-db-deployment.yml
│       ├── app-prod-db-pvc.yml
│       ├── app-prod-db-service.yml
│       └── app-prod-wrk-deployment.yml
├── README.md
├── src/
│   ├── diagnosis_api.py
│   ├── jobs.py
│   └── worker.py
└── wdbc.data.csv
```

## Installation

You have the option to build this project from source, or use the provided Docker container on DockerHub. A Docker installation is required, as we build and run a Docker image.

We describe below the installation process using terminal commands, which are expected to run on a Ubuntu 20.04.5 machine with Python3. Installation may differ for other systems.


### Option 1: Automate deployment using `docker-compose` from source
Since this is a Docker build, the requirements need not be installed, as it will automatically be done on the Docker image. All commands, unless otherwise noted, are to be run in a terminal.

* First, install Docker: `sudo apt-get install docker` or follow installation instructions for [Docker Desktop](https://www.docker.com/get-started/) for your system. We are using **Docker 20.10.12**
* Next, install docker-compose: `sudo apt-get install docker-compose-plugin` or follow the instructions [here](https://docs.docker.com/compose/install/linux/). We are using **Docker Compose 1.25.0**
* Clone the  repository: `https://github.com/dhannywi/Diagnosis_API.git`
* Then, navigate to the `Diagnosis_API` directory by executing the command `cd Diagnosis_API`

**The quickest way to get your services up and running is to use `docker-compose` to automate deployment.**
* Create a `data` folder inside the `Diagnosis_API/docker/` directory by executing the command `mkdir data`. This allows Redis to store data in the disk so that the data is persistent, even when the services are killed.
* Go back to the root `Diagnosis_API` directory and execute the command `docker-compose -f docker/docker-compose.yml up --build`. Your images are built and services are up and running when you see the message:
```console
$ docker-compose -f docker/docker-compose.yml up --build
Creating network "docker_default" with the default driver
Building flask-app
Step 1/11 : FROM ubuntu
 ---> 08d22c0ceb15
...
redis-db_1   | 1:M 26 Apr 2023 22:18:39.313 * DB loaded from disk: 0.004 seconds
redis-db_1   | 1:M 26 Apr 2023 22:18:39.313 * Ready to accept connections
...
flask-app_1  | Press CTRL+C to quit
flask-app_1  |  * Restarting with stat
flask-app_1  |  * Debugger is active!
flask-app_1  |  * Debugger PIN: 622-922-706
```
* In a new terminal, execute `docker ps -a`. You should see the containers running.
* Execute `docker images` to check that the images are built
```console
user:$ docker images
REPOSITORY               TAG       IMAGE ID       CREATED         SIZE
dhannywi/diagnosis_wrk   1.0       25da27e938ee   2 minutes ago   1.05GB
dhannywi/diagnosis_app   1.0       2a42caa1289e   3 minutes ago   1.06GB
```
* Now you are ready to use the REST API locally using `curl localhost:5000/<route>`
* If you want to enable public access for your API, you will need to push the images to Docker Hub, then deploy the Kubernetes cluster.
    1. First, you will need to login `docker login`
    2. Then, push the two images by executing `docker push dhannywi/diagnosis_wrk:1.0` and `docker push dhannywi/diagnosis_app:1.0`. If you are building your own image, change `dhannywi` to your docker hub username.
    3. Check your Docker Hub page to see if the images are there. If you encounter `denied: requested access to the resource is denied` error while pushing the images, follow the instructions [here](https://jhooq.com/requested-access-to-resource-is-denied/#2-step-1---lets-do-the-docker-logout-first)
    4. Note: If you are using your own image for kubernetes deployment, please see details in `Customization for Developers` prior to running kubernetes deployments.
* When you are done using the API, take down the services by executing `docker-compose -f docker/docker-compose.yml down` inside the `Diagnosis_API` folder

## Option 2: Deployment using images from docker hub
Similar to option 1, you will need to have **Docker 20.10.12** installed to run the commands. Howeve, we will be pulling existing images in the docker hub instead of building it from source.
* First, install Docker: `sudo apt-get install docker` or follow installation instructions for [Docker Desktop](https://www.docker.com/get-started/) for your system. We are using **Docker 20.10.12**
* Next, install docker-compose: `sudo apt-get install docker-compose-plugin` or follow the instructions [here](https://docs.docker.com/compose/install/linux/). We are using **Docker Compose 1.25.0**
* Clone the  repository: `https://github.com/dhannywi/Diagnosis_API.git`
* Then, navigate to the `Diagnosis_API` directory by executing the command `cd Diagnosis_API`
* Create a `data` folder inside the `Diagnosis_API/docker/` directory by executing the command `mkdir data`. This allows Redis to store data in the disk so that the data is persistent, even when the services are killed.
* Pull images from docker hub: `docker pull redis:7`, `docker pull dhannywi/diagnosis_wrk:1.0` and `docker pull dhannywi/diagnosis_app:1.0`.
* Go to the root `Diagnosis_API` folder and execute `docker-compose -f docker/docker-compose.yml up` to get the images running and services connected.
* Check if sevices are connected by executing `docker ps -a`
* Now you are ready to use the REST API locally using curl localhost:5000/<route>
* Follow the steps in Kubernetes deployment to enable public access, please note that if you are using different images from ones specified, see details in `Customization for Developers` prior to running kubernetes deployments.
* When you are done using the API, take down the services by executing `docker-compose -f docker/docker-compose.yml down` inside the `Diagnosis_API` folder


## Option 3: Kubernetes Deployment & enabling public access
To run this app on a Kubernetes cluster and eventually make the API publicly accessible, enter the following commands in the console from which you have Kubernetes access. Clone the  repository: `https://github.com/dhannywi/Diagnosis_API.git`, and execute these commands inside the `Diagnosis_API/kubernetes/prod` folder. **Please follow order of execution**:
* `kubectl apply -f app-prod-db-pvc.yml` -- setting up the PVC to save the Redis data from the Flask app.
* `kubectl apply -f app-prod-db-deployment.yml` -- creating a deployment for the Redis database so that the desired state for Redis is always met.
* `kubectl apply -f app-prod-db-service.yml` -- starting the Redis service so that there is a persistent IP address that you can use to communicate to Redis.
* `kubectl apply -f app-prod-wrk-deployment.yml` -- setting up the deployment for the worker on the Kubernetes cluster to help with analysis jobs.
* `kubectl apply -f app-prod-api-service.yml` -- getting a persistent IP address for the Flask app with a service, which can be used to test the app prior to public deployment.
* `kubectl apply -f app-prod-api-deployment.yml` -- setting up the deployment for the Flask app on the Kubernetes cluster.
* **Testing prior to public deployment** Should you want to run a debug deployment to test your API before deployment, use this IP address from api service to run the tests execute `kubectl get services` and take note of the IP address for the flask service. Go back to `Diagnosis_API/kubernetes` folder and execute `kubectl apply -f dwi67-test-python-debug.yml`.
* Execute `kubectl get deployments`. Note the python debug deployment name to access it, execute: `kubectl exec -it py-debug-deployment-f484b4b99-hk6pb -- /bin/bash`. When running curl commands, replace `127.0.0.1` or `localhost` with the IP address for your Flask service.
* `kubectl apply -f app-prod-api-nodeport.yml` -- 
* Before applying the ingress, execute `kubectl get services` to get port number for ingress. The port number for ingress is the number can be found between the `5000:` and `/TCP` of the nodeport's PORT(S). In the example below, it's `30425`.
```console
user:$ kubectl get services
NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
dwi67-test-redis-service      ClusterIP   10.233.36.35    <none>        6379/TCP         2m32s
dwi67-test-service-nodeport   NodePort    10.233.28.230   <none>        5000:30425/TCP   45s
```
* Once you've updated the port number in the ingress, execute `kubectl apply -f app-prod-api-ingress.yml` for public access deployment.
* Execute `kubectl get ingresss` to check that the public access URL is active.
* Now, you can start curling using `dwi67.coe332.tacc.cloud` instead of `localhost:5000`. GET requests can be viewed in your browser, however, POST and DELETE requests need to be done in your terminal.


<details>
<summary><h3>Customization for Developers</h3></summary>

* Running kubernetes commands above will automatically pull the image specified in the scripts from the Docker Hub.
If you wish to use your own Flask API in the Kubernetes cluster, you must change the name of image being pulled in `docker-compose.yml`, `app-prod-wrk-deployment.yml` and `app-prod-api-deployment.yml` to your preferred image on Docker Hub and then re-apply the Kubernetes depolyment.
* You may also want to change the **Environment variable** in your `docker-compose.yml` to reflect your Redis service name. Example:
```console
environment:
  - REDIS_IP=<redis-service-name>
```
* The same change will also need to be done on the `app-prod-api-deployment.yml` and `app-prod-wrk-deployment.yml`:
```console
env:
  - name: REDIS_IP
    value: <redis-service-name>
```
* **Note** the <redis-service-name> need to match the name under `app-prod-db-service.yml` metadata. Example:
```console
---
apiVersion: v1
kind: Service
metadata:
  name: <redis-service-name>
```
* If you wish to use a different URL for public access, change the host under spec in the `app-prod-wrk-deployment.yml` with `"<your-url>.coe332.tacc.cloud"`
```console
spec:
  rules:
  - host: "dwi67.coe332.tacc.cloud"
```

</details>
<br>

## Usage
Once you have the dependencies installed and the server running, we can start querying using the REST API in the Flask app.

Below are the routes for you to request data from:
|    | Route | Method | What it returns |
| -- | ----- | ------ | --------------------- |
| 1. | `/data`   | POST | Put data into Redis   |
| 2. | `/data` | GET | Return all data from Redis |
| 3. | `/data` | DELETE | Delete data in Redis |
| 4. | `/id` | GET | Return json-formatted list of all "ID Number" |
| 5. | `/id/<id_num>` | GET | Return all data associated with <id_num> |
| 6. | `/outcome` | GET | Return a dictionary with information on malignant and benign cases with associated ID Numbers |
| 7. | `/diagnosis-mean-radius` | GET | Return a dictionary with Mean Radius information based on diagnosis |
| 8. | `/image` | POST | Create plot and saves it to Redis |
| 9. | `/image` | GET | Return plot image to the user, if present in the database |
| 10. | `/image` | DELETE | Delete the plot image from the database |
| 11. | `/jobs` | POST | Submits job to worker for analysis of data |
| 12. | `/jobs/<job_id>` | GET | Returns the status of the <job_id> |
| 13. | `/download/<job_id>` | GET | Returns the plot associated with <job_id> |
| 14. | `/help` | GET | Return help text (string) that briefly describes each route |

### Querying Data Using the REST API
Since we need to keep the server running in order to make requests, open an additional shell and change your directory to the same directory your server is running. The data has been automatically loaded and you can start querying. Keep in mind that if you accidentally queried using the `DELETE` method, you will need to query using the `POST` method first in order to re-load the dataset into the database. Otherwise, when data has not been loaded/has been deleted, you will receive the following error message:
```console
user:$ curl localhost:5000/data
Error. Breast cancer data not loaded in
```

### Example Outputs

#### > `user:$ curl localhost:5000/data -X POST`
```console
Data loaded in
```

#### > `user:$ curl localhost:5000/data`
```console
[
.
  },
  {
    "Area SE": "156.8",
    "Compactness SE": "0.0496",
    "Concave Points SE": "0.01561",
    "Concavity SE": "0.06329",
    "Diagnosis": "M",
    "Fractal Dimension SE": "0.004614",
    "ID Number": "8910988",
    "Mean Area": "1491",
    "Mean Compactness": "0.1961",
    "Mean Concave Points": "0.1088",
    "Mean Concavity": "0.2195",
    "Mean Fractal Dimension": "0.06194",
    "Mean Perimeter": "147.3",
    "Mean Radius": "21.75",
    "Mean Smoothness": "0.09401",
    "Mean Symmetry": "0.1721",
    "Mean Texture": "20.99",
    "Perimeter SE": "8.867",
    "Radius SE": "1.167",
    "Smoothness SE": "0.005687",
    "Symmetry SE": "0.01924",
    "Texture SE": "1.352",
    "Worst Area": "2384",
    "Worst Compactness": "0.4725",
    "Worst Concave Points": "0.1841",
    "Worst Concavity": "0.5807",
    "Worst Fractal Dimension": "0.08858",
    "Worst Perimeter": "195.9",
    "Worst Radius": "28.19",
    "Worst Smoothness": "0.1272",
    "Worst Symmetry": "0.2833",
    "Worst Texture": "28.18"
  },
  {
.
]
```

#### > `user:$ curl localhost:5000/data -X DELETE`
```console
Data deleted
```

#### > `user:$ curl localhost:5000/id`
```console
[
.
  "91979701",
  "901549",
  "905520",
.
]
```

#### > `user:$ curl localhost:5000/id/<id_num>`
With `91594602` in place of `<id_num>`
```console
{
  "Area SE": "38.49",
  "Compactness SE": "0.0163",
  "Concave Points SE": "0.009423",
  "Concavity SE": "0.02967",
  "Diagnosis": "M",
  "Fractal Dimension SE": "0.001718",
  "ID Number": "91594602",
  "Mean Area": "701.9",
  "Mean Compactness": "0.08597",
  "Mean Concave Points": "0.04335",
  "Mean Concavity": "0.07486",
  "Mean Fractal Dimension": "0.05915",
  "Mean Perimeter": "97.26",
  "Mean Radius": "15.05",
  "Mean Smoothness": "0.09215",
  "Mean Symmetry": "0.1561",
  "Mean Texture": "19.07",
  "Perimeter SE": "2.63",
  "Radius SE": "0.386",
  "Smoothness SE": "0.004952",
  "Symmetry SE": "0.01152",
  "Texture SE": "1.198",
  "Worst Area": "967",
  "Worst Compactness": "0.2101",
  "Worst Concave Points": "0.112",
  "Worst Concavity": "0.2866",
  "Worst Fractal Dimension": "0.06954",
  "Worst Perimeter": "113.8",
  "Worst Radius": "17.58",
  "Worst Smoothness": "0.1246",
  "Worst Symmetry": "0.2282",
  "Worst Texture": "28.06"
}
```

#### > `user:$ curl localhost:5000/outcome`
```console
{
  "Benign": {
    "IDs": [
      "918192",
      .
      .
      "869224"
    ],
    "Total cases": 357
  },
  "Malignant": {
    "IDs": [
      "852781",
      .
      .
   "866083"
    ],
    "Total cases": 212
  }
}
```

#### > `user:$ curl localhost:5000/diagnosis-mean-radius`
```console
{
  "Benign": {
    "cases": 357,
    "mean_radius": {
      "avg": 12.15,
      "max": 17.85,
      "min": 6.981
    }
  },
  "Malignant": {
    "cases": 212,
    "mean_radius": {
      "avg": 17.46,
      "max": 28.11,
      "min": 10.95
    }
  }
}
```

#### > `user:$ curl localhost:5000/image -X POST`
```console
Graph successfully saved
```

#### > `user:$ curl localhost:5000/image -X GET --output image.png`
```console
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 19318  100 19318    0     0  1257k      0 --:--:-- --:--:-- --:--:-- 1257k
```
<img src="https://raw.githubusercontent.com/dhannywi/Diagnosis_API/29958a340db4a6a71938e4cbd72cc0de0f6df092/kubernetes/prod/image.png" width="500" height="500">

#### > `user:$ curl localhost:5000/image -X DELETE`
```console
Image deleted
```

#### > `user:$ curl localhost:5000/help`
```console
    Usage: curl [host_name]:5000[ROUTE]
    A Flask REST API for querying and returning interesting information from the breast cancer diagnosis dataset.
    Route                           Method  What it returns
    /data                           POST    Put data into Redis database
    /data                           GET     Return entire data set from Redis database
    /data                           DELETE  Delete data in Redis database
    /id                             GET     Return json-formatted list of all "ID Number"
    /id/<id_num>                    GET     Return all data associated with <id_num>
    /outcome	                    GET	    Return a dictionary with information on malignant and benign cases with associated ID Numbers
    /diagnosis-mean-radius          GET     Return a dictionary with Mean Radius information based on diagnosis
    /image                  	    POST    Creates a plot and saves it to Redis
    /image                  	    GET     Returns the plot created
    /image                  	    DELETE  Delete the plot saved in Redis database
    /jobs                           POST    Submits job to worker for analysis of data
    /jobs/<job_id>                  GET     Returns the status of the <job_id>
    /download/<job_id>              GET     Returns the plot associated with <job_id>
    /help                           GET     Return help text that briefly describes each route
```

### Jobs
1. Creating Jobs > `curl localhost:5000/jobs -X POST -d '{"start":6, "end":12}' -H "Content-Type: application/json"` replace the `start` and `end` with desired amount. 
```console
user:$ curl localhost:5000/jobs -X POST -d '{"start":6, "end":12}' -H "Content-Type: application/json"
{
  "id": "9905ff66-c92b-4e01-a455-a847af81b31d",
  "status": "submitted",
  "start": 6,
  "end": 12
}
```

2. Checking job progress > `curl localhost:5000/jobs/<job_id>` replace the `<job_id>` with the id generated from step 1.
```console
user:$ curl localhost:5000/jobs/9905ff66-c92b-4e01-a455-a847af81b31d
{
  "id": "9905ff66-c92b-4e01-a455-a847af81b31d",
  "status": "in progress",
  "start": "6",
  "end": "12"
}
```

3. Downloading job result > `curl localhost:5000/downloads/<job_id>` replace the `<job_id>` with the id generated from step 1.
```console
`user:$ curl localhost:5000/downloads/9905ff66-c92b-4e01-a455-a847af81b31d --output image.png`
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 19318  100 19318    0     0  1257k      0 --:--:-- --:--:-- --:--:-- 1257k
```

## Additional Resources
* [University of Wisconsin-Madison Research](https://pages.cs.wisc.edu/~olvi/uwmp/cancer.html)
* [Breast Cancer Wisconsin (Diagnostic) Data Set](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic))

## Authors
* Dhanny Indrakusuma
* Pranjal Adhikari
* Amanda Lee
