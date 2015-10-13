from google.appengine.ext import webapp

request = Request('/')
request.method = 'POST'
request.body = 'check=a&check=b&name=Bob'

# The whole MultiDict:
# POST([('check', 'a'), ('check', 'b'), ('name', 'Bob')])
post_values = request.POST
print post_values

# The last value for a key: 'b'
check_value = request.POST['check']
print check_value

# All values for a key: ['a', 'b']
check_values = request.POST.getall('check')
print check_values

# An iterable with alll items in the MultiDict:
# [('check', 'a'), ('check', 'b'), ('name', 'Bob')]
values = request.POST.items()
print values