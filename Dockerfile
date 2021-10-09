FROM python:3
MAINTAINER Ross Pearson
# Make port 5000 available to the world outside this container
EXPOSE 5000
COPY requirements.txt /
RUN pip install -r /requirements.txt
#flask run from install file
RUN pip install flask
RUN pip install flask-restful
COPY . /app
WORKDIR /app

RUN chmod 644 app.py
CMD ["python", "app.py", "-p 5000"]