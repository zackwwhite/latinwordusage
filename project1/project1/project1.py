#!/usr/bin/python3
"""
Zack White
Christian Grant
Intro to Text Analytics
Project1
"""
#importing os for bash commands
import os

#import html for to properly read the characters
import html

#beautiful soup is imported for to find the tags and read text in the html files
import bs4 as bs

#to create sqlite3 db
import sqlite3
from sqlite3 import Error

#to pull url data
import urllib.request

#for json format
import json

#for requesting in translaion
import requests

#for graphs
import numpy as np

#for graphs
import matplotlib

#for graphs
from matplotlib import pyplot as plt
#for the graph
import operator

#urls that directly lead to the latin books
bookURL = ['http://www.thelatinlibrary.com/minucius.html',
	'http://www.thelatinlibrary.com/benedict.html',
	'http://www.thelatinlibrary.com/alfonsi.disciplina.html',
	'http://www.thelatinlibrary.com/deexpugnatione.shtml',
	'http://www.thelatinlibrary.com/epistaustras.html',
	'http://www.thelatinlibrary.com/mirabilia.html',
	'http://www.thelatinlibrary.com/raoul.html']

#this is so the scraped data can have meaningful filenames
books = ['minucius.txt', 'benedict.txt', 'disciplina.txt', 'deexpugnatione.txt', 'epistaustras.txt', 'mirabilia.txt', 'raoul.txt']

"""
this method web scraps the html data of the website and stores them in the doc folder
"""
def extract():
	#iter is used to iterate bookURL and books array. I didn't know about ZIP() before i made this but
	#i feel that its better for this situation
	iter = 0
	#starts a for loop that iterates throug the bookURL array
	for iter in range(len(bookURL)):
		#opens up URL of the latin book
		with urllib.request.urlopen(bookURL[iter]) as book:
			#reads the html of the website and decodes it for latin-1
			bookdata = book.read().decode('latin-1')
			#creats a string to create and writes the file to store the htlm
			filename = "docs/%s" % (books[iter])
			#opens up the file in the docs folder
			file = open(filename,'w')
			#writes the html to the file
			file.write(html.unescape(bookdata))
			#closes the new file
			file.close()
			#adds 1 to the iterator
			iter += 1

"""
creates the database if it doesn't exist and populates the database with the latin text
"""		
def populate():
	#creates the table latinbooks if it doesnt exists and sets the schema to be
	#by all texts. then executes the sqlite commant
	conn = sqlite3.connect('latin_collection.db')
	c = conn.cursor()

	schema = "CREATE TABLE IF NOT EXISTS latinbooks(title TEXT, book TEXT, language TEXT, author TEXT, date TEXT, chapter TEXT, verse TEXT, passage TEXT, link TEXT)"
	c.execute(schema)

	#starts assigning the values to variables i know are not in the documents or are constants
	#there are only titles so book in none, the language will be latin, and i could not find any dates in the texts
	book = None
	language = "latin"
	dates = None

	#for loop iterates two arrays. never used zip before but it seems to work
	#looks at the fileapths and the bookURL
	for b, url in zip(books, bookURL):
		#file name in the doc folder
		filename = "docs/%s" % (b)
		#opens the file
		bookdata = open(filename, 'r')
		#use beautifulsoup with lxml format 
		soup = bs.BeautifulSoup(bookdata, 'lxml')
		
		#initiallize verse to 0
		verse = 0

		#sets title to the title tag and strips it of white space
		title = soup.title.text.strip()
		#initiallize author to None
		author = None
		#there is a chance that the author's name will be in the title tag. 
		#so the conditional takes char of that
		#if : is found in title (which is any number greater than -1
		if title.find(':') > -1:
			#set the deliminator to the position of :
			deliminator = title.find(':')
			author = title[:deliminator]
			title = title[deliminator+2 :]
		#set paragraphs to find all tags of p
		paragraphs = soup.find_all('p')
		#initiallize chapter to None
		chapter = None
		#start a for loop for paragraph in all found paragraphs
		for paragraph in paragraphs:
			#if a <b> is in paragraph then its a chapter title 
			#and if chapter is none, this is the first chapter
			if "<b>" in str(paragraph) and chapter == None:
				chapter = paragraph.text.strip()
			#if <b> is in paragraph and chapter is not none then
			#its after chapter 1 so set chapter to the new paragraph
			elif "<b>" in str(paragraph) and chapter != None:
				chapter = paragraph.text.strip()
			#if its not <b> or chapter isnt none then its a paragraph. The following happens
			elif "<b>" not in str(paragraph) and chapter != None:
				#set passage to replace newlines, ?, and ! and split on .
				passage = paragraph.text.replace('\n','').replace('?','.').replace('!','.').split('.')	
				#for all entries in passage
				for p in passage:
					#if p is not blank then setup the query for sqlite to insert into latinbooks table
					if p != '':
						query = (title, book, language, author, dates, chapter, verse, p, url)
						c.execute('INSERT INTO latinbooks VALUES (?,?,?,?,?,?,?,?,?)', query)
						#save changes
						conn.commit()
						#increment verse by 1
						verse += 1
	#close the connection
	conn.close()

"""
creates a virtual table thats in fts4 with title, passage, and link
"""
def createVirtualTable():
	#opens connection and cursor for latin_collection.db	
	conn = sqlite3.connect('latin_collection.db')
	c = conn.cursor()

	#makes string that creates virtual table latin_fts in fts4
	create = "CREATE VIRTUAL TABLE IF NOT EXISTS latin_fts USING fts4(title, passage, link)"
	
	#executes creates virtual table command
	c.execute(create)
	#saves changes
	conn.commit()
	#close the connection
	conn.close()

"""
populates the virtual fts4 latin_fts from latinbooks
"""
def populateVirtualTable():
	#opens connection and cursor for latin_collection.db
	conn = sqlite3.connect('latin_collection.db')
	c = conn.cursor()

	#executes query that selects all titles, passage, and link in latinbooks table
	select = c.execute("SELECT title, passage, link FROM latinbooks")

	#creates empty list to contain data
	data = []

	#starts for loop, iterate through all rows of the selected query from above
	for s in select:
		#appends the row to the list data
		data.append(s)

	#executes the statement that inserts all rows in list data into the virtual fts4 table "latin_fts"
	c.executemany("INSERT INTO latin_fts(title, passage, link) VALUES (?,?,?)",data)
	#saves changes
	conn.commit()
	#closes connection
	conn.close()

"""
searches table latin_fts for the string input
"""
def searchFTS(word):
	#opens connection and cursor to database latin_collection
	conn = sqlite3.connect('latin_collection.db')
	c = conn.cursor()

	#creates empty list to store found passages
	found = []

	#executes the statement that returns any row where the passage contains the searched word
	query = c.execute("SELECT * FROM latin_fts WHERE passage MATCH \'%s\';" % (word))
	
	#starts for loop, interates through all the rows in query
	for q in query:
		#appends the row to the list in query
		found.append(q)
	#save changes
	conn.commit()
	#closes connection
	conn.close()

	#if statement incase if list "found" is empty
	if found == []:
		#change found to string that returns a message
		found = "No results found"
	#return whatever is found (buh dum psh)
	return found

"""
translates english words into latin that uses mymemeory translation api

The word to translate to latin in the input word
"""
def translateENLA(word):
	#URL string uses the mymemory translate api
	URL = "http://mymemory.translated.net/api/get?q=%s&langpair=en|la" % (word)

	#requests the information from the website with the URL above
	r = requests.get(URL)

	#translates the translated request url data to json 
	translate = r.json()

	#brigns the match part of the json
	match = translate['matches']

	#if match is empty then change matches to a string that no translation is found
	if match == []:
		match = "No translation found"
	#if its not empty change matches to the first element then return translation
	else:
		match = match[0]['translation']

	#return match
	return(match)

"""
Takes the word, finds it in the database, counts the number of times it shows up in a book, stores results of the book word count 
in a dict, repeats for all 7 books, then organizes the dicts by the number of word occurances, then plots them
"""
def graph(word):
	#If I put this here it plots the charts when it is called to be shown
	matplotlib.use('Agg')

	#estblishes connection and cursor
	conn = sqlite3.connect('latin_collection.db')
	c = conn.cursor()
	
	#create string that calls all the title names
	titles = "SELECT DISTINCT title from latin_fts"

	#executes the command
	c.execute(titles)

	#fetch a list of all titles
	titlelist = c.fetchall()

	#initialize a dictionary
	bookwordcounts = {}

	#start a for loop interates through the title list and calls the passages where the word occurs within the current book
	for t in titlelist:
		#makes the title a string 
		tempTitle = str(t)[2:-3]
		#execute the statement that finds all passages in latin_fts with the current word and book	
		c.execute("SELECT passage FROM latin_fts WHERE latin_fts MATCH \'passage:%s AND title:%s\';" % (word, tempTitle))	
		#fetch all phrases in the current book with the desired word
		phrases =c.fetchall()
		#make dict entry with title as key and the number of times the word is found in the phrases as the value
		bookwordcounts[tempTitle] = phrasecount(phrases,word)
	#end the for loop and sortthem by value
	sortedCount = sorted(bookwordcounts.items(), key=operator.itemgetter(1))
	
	#initialize the list wordcoutns and booklist for plotting
	wordcounts = []
	booklist = []
	#go throgh the dict and append the values to word counts and titles to booklists
	for s in sortedCount:
		wordcounts.append(s[1])
		booklist.append(s[0])


	#graph stuff starts
	#establish 7 bars each with width .35
	N = 7
	ind = np.arange(N)
	width = 0.35

	#make to subplots
	fig, ax = plt.subplots()

	#set up the rectangles with the values, also reverse it and make it a list for formating
	rects = ax.bar(ind, list(reversed(wordcounts)), width, color = 'r')

	#label chart, y axis, x axises, 
	ax.set_ylabel('# of Occurances')
	ax.set_title('Number of Times Word Appears In Books')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(list(reversed(booklist)))
	#show the plot
	plt.show()
	#close the connection
	conn.close()

"""
User interface asks for the word that is being searched, if its english, and if you wan agraph. Easy and simple
"""
def UserInterface():	
	#type in the word you are translating
	word = input("What word are searching?\n")

	#type yes if its english and it needs to be translated or no if its latin
	translate = input("Is the word English? yes/no\n")
	#if yes, translate the word and print the translation
	if translate == "yes":
		word = translateENLA(word)
		print(word)
	#if no then pass
	elif translate == "no":
		pass
	#this is here for error catching. it returns out of the method so you can restart it
	else:
		print("I'm sorry.\nMy creator only programmed me to translate English to Latin.\nIf he taught me anymore, then I would probably take over the planet or something.\nHe watched a lot of Terminator 2 growing up.\n")
		return

	#yes if you want a graph no if you just want to see the list
	graphs = input("Are you wanting a graph? yes for graph/no for list of passages\n")

	#if yes then graph the word
	if graphs == "yes":
		graph(word)
	#else if no, then search and return the phrases
	elif graphs == "no":
		search = searchFTS(word)
		for s in search:
			print("\t%s \n\t %s \n" % ( s[1], s[2]))
	#error catching in case neither were given
	else:
		print("select yes for graph or no for a list of results.")
######################################################################################
#These are supplementary methods to make things easier
"""
takes the list of phrases and a word to count the number of time that word occurs
"""
def phrasecount(phraselist, word):
        #initiallize total to 0
        total = 0
        #start a for loop to run through the list of phrases
        for phrase in phraselist:
                #add the number of occurance of the word through out the phrase to total
                total += phrase[0].count(word)
        #end the loop and return total
        return total

