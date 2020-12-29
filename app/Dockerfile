FROM python:3.8
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y openconnect
CMD python app.py