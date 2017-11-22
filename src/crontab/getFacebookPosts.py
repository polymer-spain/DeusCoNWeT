import sys
import os
import yaml
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__), "../api_handlers"))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__), "../api_handlers/lib"))
import mongoDB
from mongoDB import FacebookPosts, Token
import datetime
import urllib
import grequests
import json
from urlparse import urlparse, parse_qs
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "../api_handlers/config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)


today = datetime.datetime.now().strftime('%d-%m-%Y')
all_tokens = Token.objects

base_url = cfg['FACEBOOK_CONFIG']['url']
params ={}
params['fields'] = cfg['FACEBOOK_CONFIG']['fields']
params['since'] = today
params['locale'] = cfg['FACEBOOK_CONFIG']['locale']
posts_urls = []
match_access_token = {}
for token in Token.objects:
  cipher = mongoDB.getCipher(str(token.id))
  access_token = mongoDB.decodeAES(cipher, token.token)
  params['access_token'] = access_token
  match_access_token[access_token] = token.identifier
  url = "%s?%s" % (base_url, urllib.urlencode(params))
  posts_urls.append(url)

# make all requests in parallel
posts_requests = (grequests.get(url) for url in posts_urls)
responses_post = grequests.map(posts_requests)

# get all posts
for resp in responses_post:
  posts = resp.json()
  o = urlparse(resp.request.url)
  query = parse_qs(o.query)
  access_token = query['access_token'][0]
  # store posts
  mongoDB.createPosts(match_access_token[access_token], posts)
