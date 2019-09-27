FROM python:2.7-slim
RUN apt-get update
COPY requirements.txt /
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get install nano
COPY . /
CMD ["python", "more_magical_model.py"]
