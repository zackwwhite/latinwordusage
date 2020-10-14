import pytest
import project1
from project1 import project1


"""
runs the translate function and tests it with the expected returned word
"""
def test_Translate():
	#runs the translate function and tests it with the expected returned word
	assert project1.translateENLA('what') == "terram"
