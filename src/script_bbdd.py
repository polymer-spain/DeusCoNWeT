import httplib, urllib

f = open('src/prueba.txt', 'r')
connection = httplib.HTTPConnection('localhost:8080')
headers = {'Content-type': 'application/x-www-form-urlencoded',
			'Accept': 'text/plain'}
url = f.readline()
while url:
	params = urllib.urlencode({'url': f.readline(),
							'user': '102386634694700574028'})
	connection.request("POST", '/subir', params, headers)
	resp = connection.getresponse()
	response = resp.read()
	print response
	url = f.readline()
connection.close()