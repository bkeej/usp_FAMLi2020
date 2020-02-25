#!/usr/bin/env python

import os
import csv 
import xml.etree.ElementTree as ET 

#
# Files and Directories
#

corpus_dir = "uspanteko_corpus_xml/"
data_dir = "data_for_analysis/"

xml_files = os.listdir(corpus_dir)

#
# Parsers
#

## Takes an IGT-XML file and returns a list of phrase objects that have adjacent verbs (ie., VI / VT)
def parse_vv(xmlfile): 
	verb_tags = ["VT", "VI"]
	parse_match = []
	tree = ET.parse(xmlfile) 
	root = tree.getroot()
	for phrase in root.findall("./body/postags/phrase"):
		for x, y in zip(phrase, phrase[1:]): # trick to get adjacent pairs in phrase, i.e., pos tags
			if x.get("text") in verb_tags and y.get("text") in verb_tags: # True if adjacent verb tags
				parse_match.append(phrase.get("ph_id"))
	return parse_match

## Takes an IGT-XML file and returns a list of phrase objects with transitive verbs, but no person-marking.
def parse_no_pers(xmlfile):
	parse_match = []
	tree = ET.parse(xmlfile) 
	root = tree.getroot()
	for phrase in root.findall("./body/postags/phrase"):
		for x, y in zip(phrase, phrase[1:]): # trick to get adject pairs in phrase, i.e., pos tags
			if y.get("text") == "VT" and not x.get("text") == "PERS": # True if any VT ever not follows PERS
				parse_match.append(phrase.get("ph_id"))
	return parse_match

#
# Saving analysis 
#

# Takes a phrase id and returns a list of strings to write to CSV 
def vv_to_row(phrase):
	pass

# Takes a phrase id and returns a list of strings to write to CSV
def no_pers_to_row(phrase):
	pass


#
# Main
#

test = corpus_dir + xml_files[0]

def main():
	print parse_vv(test)
	print parse_no_pers(test)

if __name__ == "__main__":
	main() 