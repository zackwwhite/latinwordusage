#!/usr/bin/env python
#-*- coding: utf-8 -*-
import project1
from project1 import project1

def main():
	#extract latin books
	project1.extract()

	#create sqlite3 db named latin_collection
	#populate db with info from books
	project1.populate()
	#creates virtual table latin_fts
	project1.createVirtualTable()
	#populates virtual table
	project1.populateVirtualTable()
	#runs user interface that translates, displays charts or lists of passages
	project1.UserInterface()	
if __name__ == '__main__':
	main()
