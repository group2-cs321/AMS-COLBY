import api_tool
import json
import pytest

def test_get_recovery():

	#1. Without Token
	result = api_tool.get_recovery('2022-11-10', '2022-11-17', token = None)
	assert "Authorize first" in result

def test_get_sleep():
	api_tool.get_sleep()
	