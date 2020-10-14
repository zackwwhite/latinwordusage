import pytest
import sqlite3
import project1
from project1 import project1

"""
connects to the dtabase and counts the number of rows in latinbooks table
"""
def rowcount():
	#connects to latin_collection.db and establishes cursor
	conn = sqlite3.connect('../project1/latin_collection.db')
	c = conn.cursor()

	#creates count string
	count = "SELECT count(*) FROM latinbooks"
	#executes statement
	c.execute(count)
	#returns the result
	return c.fetchone()[0]

"""
Test the populate function by populating the table and compares the counted rows with the expected count
"""
def test_rowcount():
	#populates latinbooks table
	project1.populate()
	#tests row count against the expects number of rows
	assert rowcount() == 5351
