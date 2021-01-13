# Blackstone Web API

Blackstone is a spaCy model and library for processing long-form, unstructured legal text. Blackstone is an experimental research project from the Incorporated Council of Law Reporting for England and Wales' research lab, ICLR&D.

This project wraps an API layer around Blackstone written in Python.  

## Get Started

You will need Docker installed on your machine and access to the internet. 

To start this project simply run:

`docker-compose up -d`

Running the above command starts the underlying Blackstone project as well as the API layer, which by default is running on port 4449 at http://localhost:4449.

## Running precompiled image

You can also pull and run this docker image from Docker Hub:

```docker pull addleshawgoddard/blackstone-web-api```

followed by

```docker run -p 4449:4449 addleshawgoddard/blackstone-web-api```


## Endpoints

All of the below endpoints accept a POST request with a JSON body that includes a "text" property. 

```json
{
  "text": "The Secretary of State was at pains to emphasise that, if a withdrawal agreement is made, it is very likely to be a treaty requiring ratification and as such would have to be submitted for review by Parliament, acting separately, under the negative resolution procedure set out in section 20 of the Constitutional Reform and Governance Act 2010. Theft is defined in section 1 of the Theft Act 1968"
}
```

### /ner

The NER component of the Blackstone model has been trained to detect the following entity types:

| Ent        | Name           | Examples  |
| ------------- |-------------| -----:|
| CASENAME    | Case names | e.g. *Smith v Jones*, *In re Jones*, In *Jones'* case |
| CITATION      | Citations (unique identifiers for reported and unreported cases)     |   e.g. (2002) 2 Cr App R 123 |
| INSTRUMENT | Written legal instruments     |    e.g. Theft Act 1968, European Convention on Human Rights, CPR |
| PROVISION | Unit within a written legal instrument   |    e.g. section 1, art 2(3) |
| COURT | Court or tribunal   |    e.g. Court of Appeal, Upper Tribunal |
| JUDGE | References to judges |    e.g. Eady J, Lord Bingham of Cornhill |

The API will return a JSON response with the following structure: 

```json

[{"text": "section 20", "label": "PROVISION"}, {"text": "Constitutional Reform and Governance Act 2010", "label":
"INSTRUMENT"}, {"text": "section 1", "label": "PROVISION"}, {"text": "Theft Act 1968", "label": "INSTRUMENT"}]

```

### /legislation

Blackstone's Legislation Linker attempts to couple a reference to a PROVISION to it's parent INSTRUMENT by using the NER model to identify the presence of an INSTRUMENT and then navigating the dependency tree to identify the child provision.

Once Blackstone has identified a PROVISION:INSTRUMENT pair, it will attempt to generate target URLs to both the provision and the instrument on legislation.gov.uk.

The API will return a JSON response with the following structure: 

```json

[{"provision": "section 20", "provision_url": "https://www.legislation.gov.uk/ukpga/2010/25/section/20", "instrument":
"Constitutional Reform and Governance Act 2010", "instrument_url":
"https://www.legislation.gov.uk/ukpga/2010/25/contents"}, {"provision": "section 1", "provision_url":
"https://www.legislation.gov.uk/ukpga/1968/60/section/1", "instrument": "Theft Act 1968", "instrument_url":
"https://www.legislation.gov.uk/ukpga/1968/60/contents"}]

```


### /sentences

Blackstone ships with a custom rule-based sentence segmenter that addresses a range of characteristics inherent in legal texts that have a tendency to baffle out-of-the-box sentence segmentation rules.

This behaviour can be extended by optionally passing a list of spaCy-style Matcher patterns that will explicitly prevent sentence boundary detection inside matches.

The API will return a JSON response with the following structure: 

```json

{
 ["The Secretary of State was at pains to emphasise that, if a withdrawal agreement is made, it is very likely to be a treaty requiring ratification and as such would have to be submitted for review by Parliament, acting separately, under the negative resolution procedure set out in section 20 of the Constitutional Reform and Governance Act 2010.", "Theft is defined in section 1 of the Theft Act 1968"]
}

```
