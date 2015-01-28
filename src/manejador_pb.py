# -*- coding: utf8 -*-
""" Copyright 2015 Luis Ruiz Ruiz
	Copyright 2015 Ana Isabel Lopera Martinez
	Copyright 2015 Miguel Ortega Moreno

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

import webapp2
import re, string, json
# Local imports
from ndb import Tag, Release, Autor, Repo, UserRating 
import cliente_gitHub


class ComponentInfo:
  """ 
  Class that defines a reduced set of properties about a component
  (Repo entity) stored
  Attributes:
    componentId -- Id of the component stored
    name -- name of the component
    author -- author of the component
    description -- description about the component
    nStars -- stars of the component in GitHub
    starRate -- average rating of the component in the application
    nForks -- forks of the component in GitHub
    userRating -- rate of the user logged about the component in the application 
    
  """
  def __init__(self, componentId, name, author, description, nStars, starRate, nForks, userRating):
    self.componentId = componentId
    self.name = name
    self.author = author
    self.description = description
    self.nStars = nStars
    self.starRate = starRate
    self.nForks = nForks
    self.userRating = userRating

class ComponentListHandler(webapp2.RequestHandler):
  """
  Class that defines the component list resource.
  It acts as the handler of the /components resource

  Methods:
  get -- Gets a filtered list of the components stored in the system  
  post -- Uploads a component
  """

  # GET Method
  def get(self):
    """ Gets a filtered list of the components stored in the system
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    # Get the params in the request
    user = self.request.get("user", default_value = "none")
    sortBy = self.request.get("sortBy", default_value = "stars")
    query = self.request.get("query", default_value = "none")
    orderBy = self.request.get("orderBy", default_value = "desc")
    response = [{'componentId': "ailopera_pruebaAPI",
      'name' : "pruebaAPI",
      'author' : "ailopera",
      'description' : "Mega awesome component!",
      'nStars' : 7,
      'starRate' : 0,
      'nForks' : 14,
      'userRating' : 3.5
    }]
    self.response.write(json.dumps(response))

  #POST Method
  def post(self):
    """ Uploads a component. The component is stored in the Datastore of the application
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    url = self.request.get("url", default_value="none")
    user = self.request.get("user", default_value="none")

    component = True
    path = url.split("/")
    basePath = "/repos/" + path[len(path)-2] + "/" + path[len(path)-1]
    repoId = ""
    repo_owner = ""

    #Open connection to the API endpoint
    cliente_gitHub.openConnection(basePath)

    # Set available request, in order to get statistics about the request consumed in the upload operation
    availableRequest = cliente_gitHub.getRateLimitRemaining("core")

    # Get repo info
    repoDetails = cliente_gitHub.getRepoInfo()

    # Check if the call to GitHub returned the details about the repo required 
    # (if not, the url doesn't correspond to a repo, or the cliente_gitHub encountered
    # an error while doing the call to the GitHub API) 
    if repoDetails == None:
      component = False
    else:
      # Set the repoId and repo_owner
      repoId = repoDetails["id"]
      repo_owner = repoDetails["owner"]["login"] 
    
    # Get the languages of the repo
    languages = cliente_gitHub.getRepoLanguages()
    languagesList = []
    for key, value in languages.iteritems():
      languagesList.append(key)

    # If the url given corresponds to a web component, 
    # the metadata about it is stored and it is sent the number of
    # stars of the repo to Google Analytics
    if component:
      # Also check if the component was uploaded previously
      if not (Repo.query(Repo.full_name == repoDetails['full_name']).count()) == 0:
        #raise ComponentAlreadyStoredException("The component had been stored")
        #TODO build the response
        self.response.set_status(403)
      else:
        # Get the Repo tags
        tagsList = cliente_gitHub.getTags(True)

        # Gets the commit details asociated to every tag
        # CommitList contains the commits related to all tags in tagsList
        commitList = cliente_gitHub.getCommitsTags(tagsList)

        #Adds the releases to the repo 
        releases = cliente_gitHub.getReleases()

        # Gets the user details
        userDetails = cliente_gitHub.getUserDetails(repo_owner) 
    
        # Stores the info about the repo in the datastore
        repo_full_name = repoDetails["full_name"].replace("/","_")
        lowerCaseFullName = string.lower(repo_full_name)
        #TODO: See if we have to set full_name_hash:
        #      full_name_hash = generateRepoHash(repo_full_name)
        name_lower_case = string.lower(repoDetails["name"])
        repo = Repo(full_name=repoDetails["full_name"], repo_id=repoId, name_repo=repoDetails["name"], 
          owner=Autor(login=userDetails["login"], user_id=userDetails["id"], html_url=userDetails["html_url"],
          followers=userDetails["followers"]), html_url=repoDetails["html_url"], description=repoDetails["description"],
          stars=repoDetails["stargazers_count"], forks=repoDetails["forks_count"], reputation=0.0, languages=languagesList,
          full_name_id=repo_full_name, repo_hash="", reputation_sum=0, ratingsCount=0, name_repo_lower_case=lowerCaseFullName)
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

      # The component has been uploaded succesfully
      print "LOG_INFO: Component uploaded succesfully"
      #TODO Build the response
      self.response.set_status(200)

    # If the uri doesn't correspond to a component, return an error status
    else:
      #TODO Build the response
      self.response.set_status(404)

    # Gets statistics about the request to gihtub consumed in the upload operation
    remainingRequests = cliente_gitHub.getRateLimitRemaining("core")
    requestConsumed = availableRequest - remainingRequests
    print "LOG_INFO: Requests to Github endpoint remaining: " + str(remainingRequests)
    print "LOG_INFO: Requests to Github endpoint consumed: " + str(requestConsumed)   + '\n'

    # Close the connection with github endpoint
    cliente_gitHub.closeConnection()
    
    
class ComponentHandler(webapp2.RequestHandler):
  """
  Class that defines the component resource
  It acts as the handler of the /components/{component_id} resource
  Methods:
  get -- Gets the info about a component 
  put -- Adds a rating about a component  
  """

  # GET Method
  def get(self, component_id):
    """ Gets the info about a component or
    gets a filtered list of the components stored in the system
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    # Get the params in the request
    #componentId = self.request.get("componentId", default_value = "null")
    user = self.request.get("user", default_value = "null")
    componentId = self.request.path
    print "DEBUG: PATH queried " + componentId
    
    # Returns the component queried
    #component = ndb.Repo.query(Repo.full_name_id == component_id).get()
    # TODO: Renders the page
    #response = {'componentId': component.full_name_id,
    #'name' : component.name_repo,
    #'author' : component.owner,
    #'description' : component.description,
    #'nStars' : component.stars,
    #'starRate' : 0,
    #'nForks' : component.forks,
    #'userRating' : 0
    #}

    self.response.out.write("GET Component " + component_id)


  # POST Method
  def post(self):
    """ - Add a rating about a component
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    componentId = self.request.get("componentId", default_value = "null")
    user = self.request.get("user", default_value = "null")
    rate = self.request.get("rate", default_value = 0)




app = webapp2.WSGIApplication([
    (r'/componentes', ComponentListHandler),
    (r'/componentes/(\w+)', ComponentHandler)
], debug=True)