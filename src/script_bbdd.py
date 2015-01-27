import httplib, urllib

#f = open('prueba.txt', 'r')
connection = httplib.HTTPConnection('localhost:8080')
headers = {'Content-type': 'application/x-www-form-urlencoded',
			'Accept': 'text/plain'}
params = urllib.urlencode({'url': 'https://github.com/Mortega5/star-rate',
		'user': '102386634694700574028'})
connection.request("POST", '/subir', params, headers)
resp = connection.getresponse()
response = resp.read()
print response
connection.close()