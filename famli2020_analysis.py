#!/usr/bin/env python

import os
import csv 
import xml.etree.ElementTree as ET 

# Files and Directories

corpusDir = "uspanteko_corpus_xml/"
dataDir = "data_for_analysis/"

xmlFiles = os.listdir(corpusDir)

# Parsers

## Takes and IGT-XML file and returns a list of phrase ids of phrases that have adjencts verbs (VI / VT)
def parseVV(xmlfile): 
	verbTags = ["VT", "VI"]
	pharseMatch = []
	tree = ET.parse(xmlfile) 
	root = tree.getroot()
	for phrase in root.findall("./body/postags/phrase"):
		for x, y in zip(phrase, phrase[1:]): # trick to get adject pairs in phrase, i.e., pos tags
			if x.get("text") in verbTags and y.get("text") in verbTags:
				pharseMatch.append(phrase.get("ph_id"))
	return pharseMatch

# Saving analysis

def savetoCSV():
	pass

# Main

test = corpusDir + xmlFiles[0]

def main():
	print parseVV(test)

if __name__ == "__main__":
	main() 