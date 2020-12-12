FROM python:3.6.12

ENV SPACY_MODEL=en_core_web_sm

RUN pip install lexnlp flask flask-restful blackstone jsonpickle
RUN pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz

ADD server.py /
ADD Legislation.py /
ADD NamedEntity.py /

EXPOSE 4449

CMD [ "python", "./server.py" ]