import pytest
import project1
from project1 import project1

#links to the latin books
books = ['minucius.txt', 'benedict.txt', 'disciplina.txt', 'deexpugnatione.txt', 'epistaustras.txt', 'mirabilia.txt', 'raoul.txt']
#number of characters in each book
counts = [85270, 95717, 110998, 91181, 36503, 33535, 273245]

"""
Calls the book in the docs directory, reads it and returns the length of the string
"""
def charinfile(name):
	#creates string path with the name of the book
	filename = 'docs/%s' % (name)
	#opens the book and stores it as a string
	file = open(filename, 'r').read()
	#return the number of characters in the file
	return(len(file))

"""
extracts the bookdata, puts them in the docs folder, then asserts the test by counting the number of characters extracted with the number of characters expected to be extracted
"""
def test_count():
	#extract the text 
	project1.extract()
	#runs through all the lengths and tests the number of characters in each file
	for  iter in range(len(books)):
		assert charinfile(books[iter]) == counts[iter]
