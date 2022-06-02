# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /app
# --no-cache
RUN apk add gcc g++ gfortran musl-dev python3 python3-dev
EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
CMD ["sh", "/app/run_app_dev.sh"]
