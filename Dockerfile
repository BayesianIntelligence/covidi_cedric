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

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/covidi_cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/covidi_cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

CMD ["python", "app.py", "-p 5000"]