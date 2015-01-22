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
from protorpc import messages

class ComponentBasicInfo(messages.Message):
    """It gives a reduced set of properties about a component stored"""
    name = messages.StringField(1)
    author = messages.StringField(2)
    description = messages.StringField(3)
    nStars = messages.IntegerField(4)
    starRate = messages.FloatField(5)
    nForks = messages.IntegerField(6)
    userRating = messages.FloatField(7)
    componentId = messages.StringField(8)


class ComponentDetails(messages.Message):
    """It gives the significant details about a component stored"""
    name = messages.StringField(1)
    author = messages.StringField(2)
    description = messages.StringField(3)
    nStars = messages.IntegerField(4)
    starRate = messages.FloatField(5)
    nForks = messages.IntegerField(6)
    userRating = messages.FloatField(7)
    componentId = messages.StringField(8)

class ComponentCollection(messages.Message):
    """ Collection of components """
    items = messages.MessageField(ComponentBasicInfo, 1 , repeated=True)

# Message to provide information about the status of the request
# as a try to replace 200x statuses not supported by Cloud Endpoints
class statusMessage(messages.Message):
    status = messages.StringField(1)
    status_code = messages.IntegerField(2)