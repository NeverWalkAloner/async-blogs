# Dockerfile
FROM python:3.7
WORKDIR /async-blogs
COPY . /async-blogs
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
