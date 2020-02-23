#!/usr/bin/env python

import os
import csv 
import xml.etree.ElementTree as ET 

corpusDir = "uspanteko_corpus_xml/"
dataDir = "data_for_analysis/"

xmlFiles = os.listdir(corpusDir)

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