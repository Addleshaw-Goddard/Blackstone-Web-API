from typing import Optional
from fastapi import FastAPI, Depends
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import uvicorn
import types
import spacy
from blackstone.pipeline.abbreviations import AbbreviationDetector
from blackstone.utils.legislation_linker import extract_legislation_relations
from models.Legislation import Legislation
from models.NamedEntity import NamedEntity
from models.Abbreviation import Abbreviation
from models.Sentence import Sentence
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules import CITATION_PATTERNS

class Request(BaseModel):
    text: str

nlp = spacy.load("en_blackstone_proto")

abbreviation_pipe = AbbreviationDetector(nlp)
nlp.add_pipe(abbreviation_pipe)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Working"}

@app.post("/abbreviation")
def Abbreviation(item: Request):
    abbreviation = []

    doc = nlp(item.text) 

    for abrv in doc._.abbreviations:
        abbreviation.append(Abbreviation(abrv.string, abrv.start_char, abrv.end_char, abrv._.long_form.string))

    return JSONResponse(content=jsonable_encoder(abbreviation))

@app.post("/legislation")
def Legislation(item: Request):

    doc = nlp(item.text) 
    relations = extract_legislation_relations(doc)

    for provision, provision_url, instrument, instrument_url in relations:
        legislations.append(Legislation(provision.text,provision_url,instrument.text,instrument_url))

    return JSONResponse(content=jsonable_encoder(legislations))

@app.post("/ner")
def Ner(item: Request):

    doc = nlp(item.text) 
    namedEntities = []

    for entity in doc.ents:
        namedEntities.append(NamedEntity(entity.text,entity.label_))

    return JSONResponse(content=jsonable_encoder(namedEntities))

@app.post("/sentences")
def Sentences(item: Request):

    doc = nlp(item.text) 
    sentences = []

    for sent in doc.sents:
        sentences.append(Sentence(sent.text))

    return JSONResponse(content=jsonable_encoder(sentences))

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Blackstone NLP Web API",
        version="1.0.0",
        description="Provided by Addleshaw Goddard",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://avatars.githubusercontent.com/u/65235518?s=200&v=4"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
