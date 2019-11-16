FROM python:3.6
ADD /data /app
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/"
RUN apt-get -y upgrade && apt-get -y update
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["/bin/bash", "run.sh"]