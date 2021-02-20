import os
import sys
import jsonpickle
import spacy
from blackstone.pipeline.abbreviations import AbbreviationDetector
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from blackstone.utils.legislation_linker import extract_legislation_relations
from Legislation import Legislation
from NamedEntity import NamedEntity
from Abbreviation import Abbreviation
from Sentence import Sentence
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules import CITATION_PATTERNS

nlp = spacy.load("en_blackstone_proto")

abbreviation_pipe = AbbreviationDetector(nlp)
nlp.add_pipe(abbreviation_pipe)

app = Flask(__name__)
api = Api(app)

@app.route('/abbreviation', methods=['POST'])
def abbreviation():
    requestData = request.get_json()
    text = requestData['text']
       
    doc = nlp(text) 
    abbreviation = []

    for abrv in doc._.abbreviations:
        abbreviation.append(Abbreviation(abrv.string, abrv.start_char, abrv.end_char, abrv._.long_form.string))

    return jsonpickle.encode(abbreviation, unpicklable=False)


@app.route('/legislation', methods=['POST'])
def legislation():
    requestData = request.get_json()
    text = requestData['text']
                
    doc = nlp(text) 
    relations = extract_legislation_relations(doc)

    legislations = []

    for provision, provision_url, instrument, instrument_url in relations:
        legislations.append(Legislation(provision.text,provision_url,instrument.text,instrument_url))

    return jsonpickle.encode(legislations, unpicklable=False)

@app.route('/ner', methods=['POST'])
def ner():
    requestData = request.get_json()
    text = requestData['text']
                
    doc = nlp(text) 
    namedEntities = []

    for entity in doc.ents:
        namedEntities.append(NamedEntity(entity.text,entity.label_))

    return jsonpickle.encode(namedEntities, unpicklable=False)

@app.route('/sentences', methods=['POST'])
def sentences():
    requestData = request.get_json()
    text = requestData['text']
                
    doc = nlp(text) 
    sentences = []

    for sent in doc.sents:
        sentences.append(Sentence(sent.text))

    return jsonpickle.encode(sentences, unpicklable=False)

@app.route('/status')
def status():
    # Render the page
    return "Blackstone Web API - Working"



if __name__ == '__main__':
       app.run(host='0.0.0.0', port=4449, processes=4)
