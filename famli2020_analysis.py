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


# # NOTE: Maybe we can be more general by skipping intermediate entries with an origin class. 
# # Verbs don't have origin class in XML scheme
def vv_match(phrase):
	verb_tags = ["VT", "VI"]
	matches = []
	pos = phrase.findall("pos") #return all pos tags under phrase
	for p in pos:
		if p.get("orig_cls") != None:
			pos.remove(p)
	for p1, p2 in zip(pos, pos[1:]): # trick to get adjacent pairs in phrase, i.e., pos tags
		if p1.get("text") in verb_tags and p2.get("text") in verb_tags: # True if adjacent verb tags
			matches.append((p1,p2))
	return matches


## Takes an IGT-XML file and returns a list of dictionaries characterizing 
## sentences with adjacent verbs prepped for adding to CSV.
def parse_vv(xmlfile): 
	rows = []
	tree = ET.parse(xmlfile) 
	root = tree.getroot()
	for phrase in root.findall("./body/postags/phrase"):
		matches = vv_match(phrase)
		if len(matches) > 0:
			for m in matches:
				try:
					row = {"tx_title": None, "phrase_id": None, "v1": None, "v2": None, "sentence": None, "translation": None}
					row["tx_title"] = root.get("title")
					row["phrase_id"] = phrase.get("ph_id")
					row["v1"] = root.find("./body/morphemes/phrase/morph[@morph_id='" + m[0].get("morph_ref") + "']").get("text") 
					row["v2"] = root.find("./body/morphemes/phrase/morph[@morph_id='" + m[1].get("morph_ref") + "']").get("text")
					row["sentence"] = root.find("./body/phrases/phrase[@ph_id='" + phrase.get("ph_id") + "']/plaintext").text.strip()
					row["translation"] = root.find("./body/translations/phrase[@ph_id='" + phrase.get("ph_id") + "']/trans").text.strip()
					rows.append(row)
				except AttributeError:
					pass
	return rows 


## Takes an IGT-XML file and returns a list of phrase objects with transitive verbs, but no person-marking.
## CHECK: THIS MIGHT BE RETURNING SOME FALSE POSITIVES
def parse_no_pers(xmlfile):
	rows = []
	tree = ET.parse(xmlfile) 
	root = tree.getroot()
	for phrase in root.findall("./body/postags/phrase"):
		for x, y in zip(phrase, phrase[1:]): # trick to get adject pairs in phrase, i.e., pos tags
			try:
				if y.get("text") == "VT" and x.get("text")[0] != "E": # True if any VT ever not follows an ergative
					try:
						row = {"tx_title": None, "phrase_id": None, "v": None, "sentence": None, "translation": None}
						row["tx_title"] = root.get("title")
						row["phrase_id"] = phrase.get("ph_id")
						row["v"] = root.find("./body/morphemes/phrase/morph[@morph_id='" + y.get("morph_ref") + "']").get("text") 
						row["sentence"] = root.find("./body/phrases/phrase[@ph_id='" + phrase.get("ph_id") + "']/plaintext").text.strip()
						row["translation"] = root.find("./body/translations/phrase[@ph_id='" + phrase.get("ph_id") + "']/trans").text.strip()
						rows.append(row)
					except AttributeError:
						pass 
			except IndexError:
				pass
	return rows

#
# Main
#


def main():
	with open(data_dir + "VV.csv", "w") as csvfile:
		fieldnames = ["tx_title", "phrase_id", "v1", "v2", "sentence", "translation"]
		writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
		writer.writeheader()
		for xmlfile in xml_files:
			for row in parse_vv(corpus_dir + xmlfile):
				writer.writerow(row)
	with open(data_dir + "noPERS.csv", "w") as csvfile:
		fieldnames = ["tx_title", "phrase_id", "v", "sentence", "translation"]
		writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
		writer.writeheader()
		for xmlfile in xml_files:
			for row in parse_no_pers(corpus_dir + xmlfile):
				writer.writerow(row)

if __name__ == "__main__":
	main() 