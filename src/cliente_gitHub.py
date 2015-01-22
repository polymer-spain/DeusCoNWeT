""" Copyright 2014 Luis Ruiz Ruiz
	Copyright 2014 Ana Isabel Lopera Martínez
	Copyright 2014 Miguel Ortega Moreno

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

basePath = "" # Path for the repo (:user/:repo)
connection = None
params = urllib.urlencode({})

# Other OAuth token posible 
# "Authorization": "token 4b844fda635ed7e58460a1c65252df7090c38438"
headers = {"Accept": "application/vnd.github.v3+json",
"User-Agent": "PolymerBricks-App",
"Authorization": "token f2da3d1103042894713e2862d836e09c9bb6991c"}

# Opens the connection to the GitHub API endpoint
def openConnection(basePathRepo):
  global basePath, repoId, connection
  basePath = basePathRepo
  connection = httplib.HTTPSConnection("api.github.com")
  
# Closes the connection to the GitHub API endpoint
def closeConnection():
  connection.close()

#Returns the info about the repo
def getRepoInfo():
  connection.request("GET", basePath, params, headers)
  response = connection.getresponse()
  if response.status == 403:
    print "Limit Rate exceded (Request: GET repository)"
    return None
  elif response.status == 404:
    print "La URL dada no corresponde a un repositorio válido o el repositorio es privado"
    return None
  repoDetails = json.loads(response.read())
  return repoDetails

#Gets the languages of a given repo
def getRepoLanguages():
  requestPath = basePath + "/languages"
  connection.request("GET", requestPath, params, headers)
  response = connection.getresponse()
  if response.status == 403:
    print "Limit Rate exceded (Request: GET languages of a repository)"
    return None
  languages = json.loads(response.read())
  return languages

# Gets the details of the repo owner. Returns a dict with the most significant fields
def getUserDetails(user):
  requestPath = "/users/" + user
  connection.request("GET", requestPath, params, headers)
  response = connection.getresponse()
  if response.status == 403:
    print "Limit Rate exceded (Request: GET user details)"
    return None
  userInfo = json.loads(response.read())
  userDict = {'login': userInfo["login"], 'id': userInfo["id"], "html_url": userInfo["html_url"],
  "followers": userInfo["followers"]}
  return userDict

# Get the commit associated to every tag specified in tagsList. Returns a list of tags (dict objects)
# tagsList : list of tags
def getCommitsTags(tagsList):
  commitsList = [] # CommitList is a List of dicts
  for item in tagsList:
    commit_sha = item["commit"]["sha"]
    details = getCommitDetails(commit_sha)
    commitsList.append(details)
  return commitsList

# Given the sha-code, returns a dict with the commit Details
def getCommitDetails(commit_sha):
  requestPath = basePath + '/commits/' + commit_sha
  connection.request("GET", requestPath, params, headers)
  print requestPath
  response = connection.getresponse()
  if response.status == 403:
    print "Limit Rate exceded (Request: GET commit of a repository)"
    return None
  commitInfo = json.loads(response.read())
  commitDict = {'author': commitInfo["author"]["login"], 'date': commitInfo["commit"]["author"]["date"]}
  return commitDict

# Gets the tags of the repository. Returns a list with the tags
# If pagination is true, all pages for tags result are requested
def getTags(pagination):
  requestPath = basePath + "/tags"
  connection.request("GET",requestPath, params, headers)
  response = connection.getresponse()
  if response.status == 403:
    print "Limit Rate exceded (Request: GET tags of a repository)"
    return None
  tagsList = json.loads(response.read()) # TagList is a List of dicts
  
  # Get the rest of pages of Tag request
  link = response.getheader("link", "singlePage")
  if not link == "singlePage" and pagination:
    tagsList = tagsList + paginateResults(link)
  return tagsList


# Gets the releases of the repository. Returns a List of dicts with the details of each release
def getReleases():
  releases = []
  requestPath = basePath + '/releases'
  connection.request("GET", requestPath, params, headers)
  response = connection.getresponse()
  if response.status == 403:
    print "Limit rate exceded (Request: GET releases for a repository)"
    return None
  releasesList = json.loads(response.read()) # releasesList is a List of Dicts
  
  # Pagination of results
  link = response.getheader("link", "singlePage")
  if not link == "singlePage":
    releasesList = releasesList + paginateResults(link)
  return releasesList

# Get the requests available for PolymerBricks for the actual hour
# Resource takes two posible values: core or search
def getRateLimitRemaining(resource):
  requestPath = '/rate_limit'
  connection.request("GET", requestPath, params, headers)
  response = connection.getresponse()
  data = json.loads(response.read())
  requestRemaining = data["resources"][resource]["remaining"]
  return requestRemaining


# Traverses the pages indicated in Link header of a request, from page 2 to end.  
#  Returns results collected from every page.
def paginateResults(linkHeader):
  resultsList = []
  lastPage = False
  linkList = linkHeader.replace(";", ",").replace(" ", "").split(",")
  lastLink = linkList[2]
  # Requests for the next page until last page has been reached 
  while not lastPage:
    linkList = linkHeader.replace("\"", "").replace(";", ",").split(",")
    requestPath = linkList[0].replace("<", "").replace(">", "").replace("https://api.github.com", "")
    connection.request("GET",requestPath, params, headers)
    response = connection.getresponse()
    linkHeader = response.getheader("link")
    if response.status == 403:
      print "Limit Rate exceded (Request: GET paginated results related to a repository)"
      return None
    # Append new results of tags to taglist
    resultsList = resultsList + json.loads(response.read())
    # Check if the last page has been reached
    if linkList[0] == lastLink:
      lastPage = True
    print lastPage
  return resultsList


def searchRepo(searchParameters):
  connection.request("GET", "/search/repositories?q=" + searchParameters + "+in:name,description&per_page=60", params, headers)
  response = connection.getresponse()
  data = json.loads(response.read())
  return data

