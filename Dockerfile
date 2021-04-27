FROM python:3.6.12

ENV SPACY_MODEL=en_core_web_sm

RUN pip install fastapi blackstone uvicorn
RUN pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz

EXPOSE 80

COPY ./app /app

CMD ["python", "/app/main.py"]
