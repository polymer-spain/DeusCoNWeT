""" Copyright 2014 Luis Ruiz Ruiz
    Copyright 2014 Ana Isabel Lopera Martínez
    Copyright 2014 Miguel Ortega Moreno
    Copyright 2014 Juan Francisco Salamanca Carmona

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
from google.appengine.ext import ndb
from google.appengine.ext import endpoints
import os
import sys
import httplib, urllib
import json
import string
import math, hashlib


# Local imports
import eventListener
import githubClient
from polymer_bricks_api_messages import ComponentBasicInfo
from polymer_bricks_api_messages import ComponentDetails
from core_methods_exceptions import NotFoundException, RateNotUpdatedException, \
ComponentAlreadyStoredException
from ndb import Repo, Autor, Tag, Release, UserRating
# Add the folder lib to make a local import
sys.path.insert(0, 'lib')
import Tracker

# Tracker for Google Analytics
tracker = Tracker.create('UA-55678584-1', name='myTracker', use_post=True)
  
# Generates the sha512 id corresponding to the full_name of the repo
def generateRepoHash(repoFullName):
  m = hashlib.sha256()
  m.update(repoFullName)
  return m.hexdigest()


"""Core methods """
# Method to get the user rating in the RPC message relative to a component
def getUserRating(idComponent, userId):
  rating = 0.0
  userRating = UserRating.query(ndb.AND(UserRating.google_user_id==userId, UserRating.repo_full_name_id == idComponent)).get()
  #print "DEBUG "  + str(userRating.rating_value)
  if not userRating == None:
    rating = userRating.rating_value 
  return rating

# Get component method. Returns a dict about the details of the component
def getComponent(idComponent, userId):
  component = None
  result = Repo.query(Repo.full_name_id == idComponent).get()
  if not result == None:
    component = result.toRPCMessage('detailed')
    if not userId == 0:
      userRating = getUserRating(idComponent, userId)
      component.userRating = userRating
  return component

# STABLE version
def getFilteredComponents_stable(sort, order, value, limit, userId):
  
  # Falta definir los índices de búsqueda.

# Returns a list of components filtered by a given value
def getFilteredComponents(sort, order, value):
  
  # Falta definir los índices de búsqueda.
  
#Method to rate a component
def rateComponent(idComponent, user, userRating):
  status = False
  # print "DEBUG: idComponent recibido en rateComponent " + idComponent
  # Check if the components exists. If not, return
  repo = Repo.query(Repo.full_name_id  == idComponent).get()
  if not repo == None:
    storedRating = UserRating.query(ndb.AND(UserRating.google_user_id == user,
     UserRating.repo_full_name_id == idComponent)).get()
    if storedRating == None:
      # Create the new rating
      newRating = UserRating(google_user_id = user,
        repo_full_name_id = repo.full_name_id,repo_hash = repo.repo_hash,
        rating_value= userRating)
      newRating.put()
      #Recalculate the reputation of the repo
      repo.reputation_sum = repo.reputation_sum + userRating 
      repo.ratingsCount = repo.ratingsCount + 1
      repo.reputation = float(repo.reputation_sum / repo.ratingsCount)
      repo.put()
      print "DEBUG: Creado usuario. Almacenada reputacion"
      status = True
    else:
      # The User had rated the component previously
      raise RateNotUpdatedException("The user had rated the component previously")
  else:
      raise NotFoundException("Component not found in Datastore")

  return status
  

# Method to rate a component
def rateComponent_stable(idComponent, rating):
  status = False
  repo = Repo.query(Repo.full_name_id == idComponent).get()
  if not repo == None:
    status = True
    repo.reputation_sum = repo.reputation_sum + rating 
    repo.ratingsCount = repo.ratingsCount + 1
    repo.reputation = float(repo.reputation_sum / repo.ratingsCount)
    repo.put()
  return status

# Upload method
def upload(urlparam):
  global basePath, connection, headers, params, etagEvent, repoId
  component = True
  status = False
  path = urlparam.split("/")
  basePath = "/repos/" + path[len(path)-2] + "/" + path[len(path)-1]
  repoId = ""
  repo_owner = ""
  etagEvent = ""

  #Open connection to the API endpoint
  githubClient.openConnection(basePath)

  # Set available request, in order to get statistics about the request consumed in the upload operation
  availableRequest = githubClient.getRateLimitRemaining("core")

  # Get repo info
  repoDetails = githubClient.getRepoInfo()

  # Check if the call to GitHub returned the details about the repo required 
  # (if not, the url doesn't correspond to a repo, or the githubClient encountered
  # an error while doing the call to the GitHub API) 
  if repoDetails == None:
    component = False
  else:
    # Set the repoId and repo_owner
    repoId = repoDetails["id"]
    repo_owner = repoDetails["owner"]["login"] 

    # Check if languages are js/css/html
    languages = githubClient.getRepoLanguages()
    languagesList = []
    if len(languages) == 0:
      component = False
      print "ERROR: El repositorio no es un componente"
      print "\t(No hay lenguajes definidos en el repositorio)"
    else:
      for key, value in languages.iteritems():
        if key not in ["JavaScript", "CSS", "HTML"]:
          component = False
          print "ERROR: El repositorio no es un componente (lenguaje del repo no valido)"
        else:
          languagesList.append(key)

  # If the url given corresponds to a web component, 
  # the metadata about it is stored and it is sent the number of
  # stars of the repo to Google Analytics

  if component:
    # Also check if the component was uploaded previously
    if not (Repo.query(Repo.full_name_id == repoDetails['full_name']).count()) == 0:
      raise ComponentAlreadyStoredException("The component had been stored")
    else:
      # Get the Repo tags
      tagsList = githubClient.getTags(True)

      # Gets the commit details asociated to every tag
      # CommitList contains the commits related to all tags in tagsList
      commitList = githubClient.getCommitsTags(tagsList)

      #Adds the releases to the repo 
      releases = githubClient.getReleases()

      # Gets the user details
      userDetails = githubClient.getUserDetails(repo_owner) 
    
      # Stores the info about the repo in the datastore
      repo_full_name = repoDetails["full_name"].replace("/","_")
      lowerCaseFullName = string.lower(repo_full_name)
      full_name_hash = generateRepoHash(repo_full_name)
      name_lower_case = string.lower(repoDetails["name"])
      repo = Repo(full_name=repoDetails["full_name"], repo_id=repoId, name_repo=repoDetails["name"], 
        owner=User(login=userDetails["login"], user_id=userDetails["id"], html_url=userDetails["html_url"],
        followers=userDetails["followers"]), html_url=repoDetails["html_url"], description=repoDetails["description"],
        stars=repoDetails["stargazers_count"], forks=repoDetails["forks_count"], reputation=0.0, languages=languagesList,
        full_name_id=repo_full_name, repo_hash=full_name_hash, reputation_sum=0, ratingsCount=0,
        name_repo_lower_case=name_lower_case)
      repo_key = repo.put()

      # The repo is yet stored. Now, it is necessary to update it with the remaining information
      list_tag = []
      list_release = []
      for tag, commit in zip(tagsList,commitList):
        aux_tag = Tag(name_tag=tag["name"], date_tag=commit["date"], author=commit["author"], zipball_url=tag["zipball_url"], tarball_url=tag["tarball_url"])
        list_tag.append(aux_tag)

        repo = repo_key.get()
        for release in releases:
          aux_release = Release(tag_name=release["tag_name"], html_url=release["html_url"], name_release=release["name"], description=release["body"], 
           publish_date=release["published_at"], zipball_url=release["zipball_url"], tarball_url=release["tarball_url"])
          list_release.append(aux_release)

      # Now, we store them in the Datastore
      repo = repo_key.get()
      repo.tags = list_tag
      repo.releases = list_release
      repo.put()

      # Sending new events to Google Analytics
      # Sends the stars of the repo to Google Analytics
      tracker.send('event','repo', 'StarsUpdate', repoId, repoDetails["stargazers_count"])

      # Sends the actual version (tag) of the repo to Google Analytics
      if not len(tagsList)==0:
        version = tagsList[0]["name"]   
      else:
        version = 'default'

      # Send event repo VersionUpdate sended to Google Analytics 
      tracker.send('event','repo', 'VersionUpdate', repoId, version)

      # Gets statistics about the request to gihtub consumed in the upload operation
      remainingRequests = githubClient.getRateLimitRemaining("core")
      requestConsumed = availableRequest - remainingRequests
      # print "LOG_INFO: Requests to Github endpoint remaining: " + str(remainingRequests)
      # print "LOG_INFO: Requests to Github endpoint consumed: " + str(requestConsumed)   + '\n'

      # Close the connection with github endpoint
      githubClient.closeConnection()
    
      # The component has been uploaded succesfully
      status = True
      print "LOG_INFO: Component uploaded succesfully"
  # If the repo is not a component, we set the corresponding return status
  else:
    raise NotFoundException("Github repo not found")

  return status

