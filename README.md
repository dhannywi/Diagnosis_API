<div align="center">

![Research](https://www.houstonmethodist.org/-/media/images/research/cancer-center/cancer_center_banner_1140x400.ashx?h=400&iar=0&mw=1382&w=1140&hash=28362AFB38ACA244FB16263E4AA3E267)
<h1><img src="https://img.icons8.com/color/512/pink-ribbon.png" width="30" height="30">
 Diagnosis API 
<img src="https://img.icons8.com/color/512/pink-ribbon.png" width="30" height="30">
</h1>

REST API to query data on Breast Cancer Diagnosis.  
</div>

#

## Data Description
The Breast Cancer Wisconsin dataset includes data from hundreds of breast cancer cases to develop an effective prognosis for future cases. 
For each case, the fine needle aspiration procedure was performed to take a sample from the cell nuclei present within the mass found on the body.

From the sample, various measurements were taken, including the area, texture, smoothness, and compactness.
Utilizing these measurements in the dataset, an effective and reliable prognosis can be made to determine the outcome of each case and to predict the survival status based on these features.
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

The original dataset is available from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Prognostic)), and detailed documentation is available on [University of Wisconsin-Madison](https://pages.cs.wisc.edu/~olvi/uwmp/cancer.html) research page.


## Implementation
The project uses **Python 3.8.10**, in particular **Flask 2.2.2** for REST API development, **Redis 7** for NoSQL Database, and **Docker 20.10.12** for containerization. Kubernetes is used for container ochestration and deployment. 

### Files
The file structure of this project is as below:
```
Prognosis_API/
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.wrk
│   └── docker-compose.yml
├── kubernetes/
│   ├── 
│   ├── 
│   ├── 
│   ├── 
│   ├── 
│   └── 
├── README.md
└── src/
    ├── prognosis_api.py
    ├── jobs.py
    └── worker.py
```

## Installation

You have the option to build this project from source, or use the provided Docker container on DockerHub. A Docker installation is required, as we build and run a Docker image.

We describe below the installation process using terminal commands, which are expected to run on a Ubuntu 20.04.5 machine with Python3. Installation may differ for other systems.


#### Option 1: Automate deployment using `docker-compose`
The quickest way to get your services up and running is to use `docker-compose` to automate deployment.
* Create a `data` folder inside the `Diagnosis_API/docker/` directory, execute `mkdir data`. This allows redis to store data in the disk so that the data persist, even when the services are killed.
* Go back to the root `Diagnosis_API` directory and execute `docker-compose -f docker/docker-compose.yml up --build` Your images are built and services are up and running when you see the message:
```console
```


<details>
<summary><h3>Customization for Developers</h3></summary>

* Running commands above will automatically pull the image specified in the scripts from the docker hub.
If you wish to use your own Flask API in the kubernetes cluster, you must change the name of image being pulled in `docker-compose.yml` and `flask-deployment.yml` to your preferred image on Docker Hub and then re-apply the kubernetes depolyment.
* You may also want to change the **Environment variable** in your `docker-compose.yml` to reflect your redis service name. Example:
```console
environment:
  - REDIS_IP=<redis-service-name>
```
* The same change will also need to be done on the `flask-deployment.yml`:
```console
env:
  - name: REDIS_IP
    value: <redis-service-name>
```
* **Note** the <redis-service-name> need to match the name under `redis-service.yml` metadata. Example:
```console
---
apiVersion: v1
kind: Service
metadata:
  name: <redis-service-name>
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
| 6. | `/image` | POST | Create plot and saves it to Redis |
| 7. | `/image` | GET | Return plot image to the user, if present in the database |
| 8. | `/image` | DELETE | Delete the plot image from the database |
| 9. | `/outcome` | GET | Return a json dictionary containing information regarding malignant and benign cases |
| 10. | `/help` | GET | Return help text (string) that briefly describes each route |

### Querying data using the REST API
Since we need to keep the server running in order to make requests, open an additional shell and change your directory to the same directory your server is running. The data has been automatically loaded and you can start querying. Keep in mind that if you accidentally queried using the `DELETE` method, you will need to query using the `POST` method first in order to re-load the dataset into the database. Otherwise, when data has not been loaded/ has been deleted, you will receive an error message. For example:
```console

```

## Additional Resources
* [University of Wisconsin-Madison Research](https://pages.cs.wisc.edu/~olvi/uwmp/cancer.html)
* [Breast Cancer Wisconsin (Prognostic) Data Set](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Prognostic))

## Authors
* Dhanny Indrakusuma
* Pranjal Adhikari
