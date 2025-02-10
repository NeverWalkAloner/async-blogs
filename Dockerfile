# Dockerfile
FROM python:3.8
WORKDIR /async-blogs
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
COPY requirements.txt /async-blogs
RUN pip install -r requirements.txt
COPY . /async-blogs
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
