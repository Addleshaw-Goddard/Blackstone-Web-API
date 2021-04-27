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
from Models.Legislation import Legislation
from Models.NamedEntity import NamedEntity
from Models.Abbreviation import Abbreviation
from Models.Sentence import Sentence
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
def Act(item: Request):
    abbreviation = []

    doc = nlp(item.text) 

    for abrv in doc._.abbreviations:
        abbreviation.append(Abbreviation(abrv.string, abrv.start_char, abrv.end_char, abrv._.long_form.string))

    return JSONResponse(content=jsonable_encoder(abbreviation))



@app.post("/abbreviation")
def Act(item: Request):
    abbreviation = []

    doc = nlp(item.text) 

    for abrv in doc._.abbreviations:
        abbreviation.append(Abbreviation(abrv.string, abrv.start_char, abrv.end_char, abrv._.long_form.string))

    return JSONResponse(content=jsonable_encoder(abbreviation))

@app.route('/legislation', methods=['POST'])
def legislation():

    legislations = []

    doc = nlp(item.text) 
    relations = extract_legislation_relations(doc)


    for provision, provision_url, instrument, instrument_url in relations:
        legislations.append(Legislation(provision.text,provision_url,instrument.text,instrument_url))

    return JSONResponse(content=jsonable_encoder(legislations))

@app.route('/ner', methods=['POST'])
def legislation():

    legislations = []

    doc = nlp(item.text) 
    namedEntities = []

    for entity in doc.ents:
        namedEntities.append(NamedEntity(entity.text,entity.label_))

    return JSONResponse(content=jsonable_encoder(namedEntities))

@app.route('/sentences', methods=['POST'])
def legislation():

    legislations = []

    doc = nlp(item.text) 
    sentences = []

    for sent in doc.sents:
        sentences.append(Sentence(sent.text))

    return JSONResponse(content=jsonable_encoder(sentences))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)