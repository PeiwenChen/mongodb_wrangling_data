#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}

classification_label = ['family_label','class_label', 'phylum_label', 'order_label', 'kingdom_label','genus_label']

def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()
        for line in reader:
            record = {}
            classification = {}
            # mappging dict, get data
            for k in process_fields:
                linedata = line[k]
                if linedata == 'NULL': 
                    linedata = None
                else:
                    linedata = linedata.lstrip() 
                    linedata = linedata.rstrip()
                if k in classification_label: # one of classification labels
                    classification[fields[k]] = linedata
                else:# clean other data 
                    clean_data = linedata
                    if k == 'rdf-schema#label' and linedata != None:
                        s = linedata.find('(')  
                        e = linedata.find(')') 
                        if s == -1 or e == -1:
                            clean_data = linedata  # no brackets
                        else:
                            clean_data = linedata[:s] + linedata[e+1:]
                            clean_data = clean_data.rstrip() # after removing brackets, there could be spaces at the end 
                    if k == 'name':
                        if linedata == None or not linedata.isalpha():
                            clean_data = record['label']
                    if k == 'synonym' and linedata != None:
                        clean_data = parse_array(linedata)

                    record[fields[k]] = clean_data
                record["classification"] = classification

            # append record to list
            data.append(record)
            pass
    return data


def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]
"""
print line in reader :
{'22-rdf-syntax-ns#type_label': '{animal|arachnid|eukaryote|species|owl#Thing}', 'family': 'http://dbpedia.org/resource/Orb-weaver_spider', 'conservationStatusSystem': 'NULL', 'family_label': 'Orb-weaver spider', 'depiction': 'http://upload.wikimedia.org/wikipedia/commons/f/fd/Argiope_sp.jpg', 'phylum': 'http://dbpedia.org/resource/Arthropod', 'thumbnail_label': '200px-Argiope_sp.jpg', 'conservationStatus': 'NULL', 'species': 'NULL', 'rdf-schema#label': 'Argiope (spider)', 'order_label': 'Spider', 'binomialAuthority': 'NULL', 'division_label': 'NULL', 'kingdom_label': 'Animal', 'binomialAuthority_label': 'NULL', 'thumbnail': 'http://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Argiope_sp.jpg/200px-Argiope_sp.jpg', 'kingdom': 'http://dbpedia.org/resource/Animal', 'division': 'NULL', 'class_label': 'Arachnid', 'phylum_label': 'Arthropod', 'URI': 'http://dbpedia.org/resource/Argiope_(spider)', '22-rdf-syntax-ns#type': '{http://dbpedia.org/ontology/Animal|http://dbpedia.org/ontology/Arachnid|http://dbpedia.org/ontology/Eukaryote|http://dbpedia.org/ontology/Species|http://www.w3.org/2002/07/owl#Thing}', 'species_label': 'NULL', 'rdf-schema#comment': 'The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced.', 'class': 'http://dbpedia.org/resource/Arachnid', 'depiction_label': 'Argiope_sp.jpg', 'synonym': 'NULL', 'name': 'Argiope', 'genus_label': 'NULL', 'genus': 'NULL', 'order': 'http://dbpedia.org/resource/Spider'}
"""

def test():
    data = process_file(DATAFILE, FIELDS)
    # pprint.pprint(data)
    # pprint.pprint(data[0])
    assert data[0] == {
                        "synonym": None, 
                        "name": "Argiope", 
                        "classification": {
                            "kingdom": "Animal", 
                            "family": "Orb-weaver spider", 
                            "order": "Spider", 
                            "phylum": "Arthropod", 
                            "genus": None, 
                            "class": "Arachnid"
                        }, 
                        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
                        "label": "Argiope", 
                        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
                    }



if __name__ == "__main__":
    test()
