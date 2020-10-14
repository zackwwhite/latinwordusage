import pytest
import project1
from project1 import project1

"""
No other fnacy methods here. Just creates virtual table to be safe then runs the test by counting the number of rows returned 
from the whether when searching for the latin version of "when"
"""
def test_phrasecount():
	#creates virtual table beecause testing freaks out other wise
	project1.createVirtualTable()
	#count the number of rows returned with the number of expected number of rows
	assert len(project1.searchFTS('cum')) == 535
