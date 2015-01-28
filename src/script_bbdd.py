import httplib, urllib

f = open('src/prueba.txt', 'r')
connection = httplib.HTTPConnection('localhost:8080')
headers = {'Content-type': 'application/x-www-form-urlencoded',
			'Accept': 'text/plain'}
for line in f:
	params = urllib.urlencode({'url': line,
							'user': '102386634694700574028'})
	connection.request("POST", '/componentes', params, headers)
	resp = connection.getresponse()
	response = resp.read()
	print response
connection.close()