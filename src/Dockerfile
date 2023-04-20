FROM python:3.8.10

RUN pip install Flask==2.2.0
RUN pip install requests==2.22.0
RUN pip install redis==4.5.1
RUN pip install matplotlib==3.7.1
RUN pip install PyYAML==6.0
RUN pip install hotqueue==0.2.8

COPY diagnosis_api.py /diagnosis_api.py

CMD ["python", "diagnosis_api.py"]