import pytest
import sqlite3
import project1
from project1 import project1

"""
coutns the number of rows in the virtual table latin_fts
"""
def rowcount():
	#establishes connection and cursor
	conn = sqlite3.connect('latin_collection.db')
	c = conn.cursor()

	#makes string to count number of rows
	count = "SELECT count(*) FROM latin_fts"
	#executes command
	c.execute(count)
	#stores number of rows counted
	rc = c.fetchone()[0]
	#returns rowcount
	return(rc)

"""
creates the table, populates the virutal table, then tests by counting the rows founds vs expected rows
"""
def test_rowcount():
	#creates virtual table latin_fts
	project1.createVirtualTable()
	#populates latin_fts
	project1.populateVirtualTable()
	#test by counts rows and testing it with expected row
	assert rowcount() == 5351

