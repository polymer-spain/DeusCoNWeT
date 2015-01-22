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
import endpoints
from protorpc import message_types
from protorpc import remote
import core_methods
from protorpc import messages

# Local imports
from polymer_bricks_api_messages import ComponentBasicInfo
from polymer_bricks_api_messages import ComponentDetails
from polymer_bricks_api_messages import ComponentCollection
from polymer_bricks_api_messages import statusMessage
from core_methods_exceptions import NotFoundException, RateNotUpdatedException, \
ComponentAlreadyStoredException

package = 'Hello'
WEB_CLIENT_ID = '37385538925-jv2d25auk59lisafr1gu83r04d9cuivt.apps.googleusercontent.com'

#     allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID],
@endpoints.api(name='polymerbricks', version='v1',
    description='TEST version of the API')
class PolymerBricksAPI(remote.Service):
    """Class which defines Polymer Bricks API v1"""

    """Definition of API resources"""
    ID_COMPONENT_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        idComponent=messages.StringField(1, variant=messages.Variant.STRING,
            required=True),
        user=messages.StringField(2, variant=messages.Variant.STRING,
            required=False))

    COMPONENT_FILTER_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        sortBy=messages.StringField(1, variant=messages.Variant.STRING,
            required=False),
        orderBy=messages.StringField(2, variant=messages.Variant.STRING,
            required=False),
        query=messages.StringField(3, variant=messages.Variant.STRING,
            required=False),
        limit=messages.IntegerField(4, variant=messages.Variant.INT32,
            required=False),
        user=messages.StringField(5, variant=messages.Variant.STRING,
            required=False))

    URL_COMPONENT_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        url=messages.StringField(1, variant=messages.Variant.STRING,
            required=True)
        )

    RATE_COMPONENT_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        idComponent=messages.StringField(1, variant=messages.Variant.STRING,
            required=True),        
        rate=messages.FloatField(2,variant=messages.Variant.FLOAT,
            required=True),
        user=messages.StringField(3, variant=messages.Variant.STRING,
            required=True))

    """Definition of API METHODS"""
    # Method to GET the list of components
    @endpoints.method(COMPONENT_FILTER_RESOURCE, ComponentCollection,
                      path='components', http_method='GET',
                      name='components.getAllComponents')
    def getAllComponents(self, request):
        # Set default values for a given query param (sortBy and orderBy)
        order = request.orderBy
        sort = request.sortBy

        if request.orderBy == None:
            order = "des"
        if request.sortBy == None:
            sort = "stars"
        print "EL VALOR DE LA QUERY ES: " + str(request.query)


        # Check if the value of the params are correct
        if sort not in ['stars','popular', 'name'] or order not in ['asc', 'des']:
            raise endpoints.BadRequestException()
        else:
            componentsList = core_methods.getFilteredComponents(sort, order, request.query)
            return ComponentCollection(items=componentsList)

    # Method to GET the info about a component
    @endpoints.method(ID_COMPONENT_RESOURCE, ComponentDetails,
                      path='components/{idComponent}', http_method='GET',
                      name='components.getComponent')
    def getComponent(self, request):
        user = 0
        if  not request.user == None:
            user = request.user
        component = core_methods.getComponent(request.idComponent, user)
        if component == None:
            raise endpoints.NotFoundException()
        else:
            return component
            
    # Method to POST (upload) a new component
    @endpoints.method(URL_COMPONENT_RESOURCE, statusMessage,
                      path='components', http_method='POST',
                      name='components.uploadComponent')
    def uploadComponent(self, request):
        try:
            statusUpload = core_methods.upload(request.url)
            print "DEBUG: status returned " + str(statusUpload)
            if statusUpload:
                return statusMessage(status="Component uploaded succesfullly", status_code=200)
        except NotFoundException:
            raise endpoints.NotFoundException()
        except ComponentAlreadyStoredException:
            raise endpoints.ForbiddenException()
            
    # Method to PUT a new rating about a component
    @endpoints.method(RATE_COMPONENT_RESOURCE, statusMessage,
                      path='components/{idComponent}', http_method='PUT',
                      name='components.rateComponent')
    def rateComponent(self, request):
        if request.rate > 5.0:
            raise endpoints.BadRequestException()
        try: 
            status = core_methods.rateComponent(request.idComponent, request.user, request.rate)
            if status:
                return statusMessage(status="Component rated succesfullly", status_code=200)
        # If the component hasn't been rated we return the xxx status
        except RateNotUpdatedException:
            raise endpoints.ForbiddenException()
        except NotFoundException:
            raise endpoints.NotFoundException() 



"""Stable version of the API"""
# allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID]
@endpoints.api(name='polymerbricks', version='v1.1',
    description='API to access from Polymer Bricks site')
class PolymerBricksAPI_STABLE(remote.Service):
    """Class which defines Polymer Bricks API v1"""

    """Definition of API resources"""
    ID_COMPONENT_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        idComponent=messages.StringField(1, variant=messages.Variant.STRING,
            required=True),
        user=messages.StringField(2, variant=messages.Variant.STRING,
            required=False))
    
    COMPONENT_FILTER_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        sortBy=messages.StringField(1, variant=messages.Variant.STRING,
            required=False),
        orderBy=messages.StringField(2, variant=messages.Variant.STRING,
            required=False),
        query=messages.StringField(3, variant=messages.Variant.STRING,
            required=False),
        limit=messages.IntegerField(4, variant=messages.Variant.INT32,
            required=False),
        user=messages.StringField(5, variant=messages.Variant.STRING,
            required=False))

    URL_COMPONENT_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        url=messages.StringField(1, variant=messages.Variant.STRING,
            required=True)
        )

    RATE_COMPONENT_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        idComponent=messages.StringField(1, variant=messages.Variant.STRING,
            required=True),        
        rate=messages.FloatField(2,variant=messages.Variant.FLOAT,
            required=True),
        user=messages.StringField(3, variant=messages.Variant.STRING,
            required=True))

    """Definition of API METHODS"""
    # Method to GET the list of components
    @endpoints.method(COMPONENT_FILTER_RESOURCE, ComponentCollection,
                      path='components', http_method='GET',
                      name='components.getAllComponents')
    def getAllComponents(self, request):
        # Set default values for a given query param (sortBy and orderBy)
        order = request.orderBy
        sort = request.sortBy
        if request.orderBy == None:
            order = "des"
        if request.sortBy == None:
            sort = "stars"

        # Check if the value of the params are correct
        if sort not in ['stars','popular', 'name'] or order not in ['asc', 'des'] or request.limit == 0:
            raise endpoints.BadRequestException()
        else:
            componentsList = core_methods.getFilteredComponents_stable(sort,
                order, request.query, request.limit, request.user)
            return ComponentCollection(items=componentsList)

    # Method to GET the info about a component
    @endpoints.method(ID_COMPONENT_RESOURCE, ComponentDetails,
                      path='components/{idComponent}', http_method='GET',
                      name='components.getComponent')
    def getComponent(self, request):
        user = 0
        if  not request.user == None:
            user = request.user
        component = core_methods.getComponent(request.idComponent, user)
        if component == None:
            raise endpoints.NotFoundException()
        else:
            return component
            
    # Method to POST (upload) a new component
    @endpoints.method(URL_COMPONENT_RESOURCE, statusMessage,
                      path='components', http_method='POST',
                      name='components.uploadComponent')
    def uploadComponent(self, request):
        try:
            statusUpload = core_methods.upload(request.url)
            print "DEBUG: status returned " + str(statusUpload)
            if statusUpload:
                return statusMessage(status="Component uploaded succesfullly", status_code=200)
        except NotFoundException:
            raise endpoints.NotFoundException()
        except ComponentAlreadyStoredException:
            raise endpoints.ForbiddenException()

    # Method to PUT a new rating about a component
    @endpoints.method(RATE_COMPONENT_RESOURCE, statusMessage,
                      path='components/{idComponent}', http_method='PUT',
                      name='components.rateComponent')
    def rateComponent_stable(self, request):
        if request.rate > 5.0:
            raise endpoints.BadRequestException()
        try: 
            status = core_methods.rateComponent(request.idComponent, request.user, request.rate)
            if status:
                return statusMessage(status="Component rated succesfullly", status_code=200)
        # If the component hasn't been rated we return the xxx status
        except RateNotUpdatedException:
            raise endpoints.ForbiddenException()
        except NotFoundException:
            raise endpoints.NotFoundException()


APPLICATION = endpoints.api_server([PolymerBricksAPI, PolymerBricksAPI_STABLE])