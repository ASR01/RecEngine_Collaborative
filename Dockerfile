ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.9.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

EXPOSE 8501

COPY --from=py3 / /
COPY ./app /app
COPY ./model /app/model
COPY ./data /app/data

WORKDIR /app

RUN pip3 install -r requirements.txt
ARG PYSPARK_VERSION=3.2.0
RUN pip --no-cache-dir install pyspark==${PYSPARK_VERSION}


ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]