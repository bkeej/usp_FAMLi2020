#!/usr/bin/env python

import os
import csv 
import xml.etree.ElementTree as ET 

#Files and Directories

corpusDir = "uspanteko_corpus_xml/"
dataDir = "data_for_analysis/"

xmlFiles = os.listdir(corpusDir)

# Tags of interest

verbTags = ["VT", "VI"]


def parseXML(xmlfile): 
	tree = ET.parse(xmlfile) 
	root = tree.getroot() 
	print root

def savetoCSV():
	pass

# Main

test = corpusDir + xmlFiles[0]

def main():
	parseXML(test)

if __name__ == "__main__":
	main() 