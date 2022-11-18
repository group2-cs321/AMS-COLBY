from urllib import request
from urllib.parse import urlparse
from urllib.parse import parse_qs

def get_recovery(start_date, end_date, token = None):
	if not token:
		return "Authorize first" 

	url = 'https://api.ouraring.com/v2/usercollection/daily_readiness' 
	params={ 
	    'start_date': start_date, 
	    'end_date': end_date 
	}
	headers = { 
	  'Authorization': 'Bearer ' + token 
	}
	response = requests.request('GET', url, headers=headers, params=params) 

	return response.json()

def get_sleep():
	pass

