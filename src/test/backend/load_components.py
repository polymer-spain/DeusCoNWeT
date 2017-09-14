#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Copyright 2016 Luis Ruiz Ruiz
    Copyright 2016 Ana Isabel Lopera Martinez
    Copyright 2016 Miguel Ortega Moreno
    Copyright 2016 Juan Francisco Salamanca Carmona

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

""" In this file, the system is fed with the created components by the workgroup
    members to be able to choose between the different versions of them.
    The components are based on different social networks, in this case will be 
    uploaded the ones corresponding to Twitter, Facebook, Google +, Stack Overflow
    and Instagram. There are, for each one, different versions: stable, latency, 
    completeness and refresh time.
"""

import urllib, json
import test_utils
import os
import yaml
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "../../api_handlers/config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

"""
Es necesario cambiar los parametros que van en los atributos y ponerlo como has comentado tu,
con un JSON dumpificado y pasado como script vale?
"""
MODE = os.getenv('VERSION', 'test')

if MODE == 'test':
    uri = "https://" + cfg['domainTest']
else:
    uri = "https://" + cfg['domain']

basepath = "/api/componentes"
request_uri = uri + basepath
test_utils.openConnection(True)
versions_list = ["stable", "accuracy", "latency"]
aux = {"endpoint": ':domain/api/aux/twitterTimeline',
        "language": ':language',
        "access_token": "",
        "secret_token": "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
        "consumer_key": "BOySBn8XHlyYDQiGiqZ1tzllx",
        "consumer_secret": "xeSw5utUJmNOt5vdZZy8cllLegg91vqlzRitJEMt5zT7DtRcHE",
        "component_base": "bower_components/twitter-timeline/static/",
        "count": 200
        }
params = urllib.urlencode({"url": 'https://github.com/JuanFryS/twitter-timeline',
        "component_id": 'twitter-timeline',
        "description": 'Web component to obtain the timeline of Twitter using Polymer',
        "social_network": 'twitter' ,
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "attributes": json.dumps(aux),
        "tokenAttr": 'access_token',
        "img": 'images/components/twitter-logo.png'
        }, doseq=True)

test_utils.make_request("PUT", request_uri, params, 201, None)

aux = {"api_key": "AIzaSyAArT6pflqm1-rj9Nwppuj_4z15FFh4Kis",
        "token": ""
        }
params = urllib.urlencode({"url": 'https://github.com/ailopera/googleplus-timeline',
        "component_id": 'googleplus-timeline',
        "description": 'Web component to obtain the timeline of Google Plus using Polymer',
        "social_network": 'googleplus',
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "predetermined": 'True',
        "attributes": json.dumps(aux),
        "tokenAttr": 'token',
        "img": 'images/components/google-icon.png'
        }, doseq=True)
test_utils.make_request("PUT", request_uri, params, 201, None)

# aux = {"component_directory": 'bower_components/github-events/',
#         "username": ":user",
#         "token": "",
#         "mostrar": 10}
# params = urllib.urlencode({"url": 'https://github.com/Mortega5/github-events',
#         "component_id": 'github-events',
#         "description": 'Web component to obtain the timeline of Github notifications',
#         "social_network": 'github',
#         "input_type": 'None',
#         "output_type": 'tweet',
#         "versions": versions_list,
#         "predetermined": 'True',
#         "attributes": json.dumps(aux),
#         "tokenAttr": 'token',
#         "img": 'images/components/github-icon.png'
#         }, doseq=True)
# test_utils.make_request("PUT", request_uri, params, 201, None)

aux = {"component_directory": 'bower_components/facebook-wall/',
        "access_token": ""}
params = urllib.urlencode({"url": 'https://github.com/Mortega5/facebook-wall',
        "component_id": 'facebook-wall',
        "description": 'Web component to obtain the timeline of Facebook messages using Polymer',
        "social_network": 'facebook',
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "predetermined": 'True',
        "attributes": json.dumps(aux),
        "tokenAttr": 'access_token',
        "img": 'images/components/facebook-icon.png'
        }, doseq=True)
test_utils.make_request("PUT", request_uri, params, 201, None)

aux = {"token": "",
        "component_base": "bower_components/pinterest-timeline-stable/"}
params = urllib.urlencode({"url": 'https://github.com/polymer-spain/DeusCoNWeT/tree/redesign/src/static/bower_components/pinterest-timeline-stable',
        "component_id": 'pinterest-timeline',
        "description": 'Web component to obtain the timeline of Pinterest messages using Polymer',
        "social_network": 'pinterest',
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "predetermined": 'True',
        "attributes": json.dumps(aux),
        "tokenAttr": "token",
        "img": "images/components/pinterest.png"
        }, doseq=True)
test_utils.make_request("PUT", request_uri, params, 201, None)

aux = {"api_key_geocoding": "AIzaSyC3shMTM6dD10MGqty-xugLBUFSCTICeBM",
        "app_key_traffic": "AmWMG90vJ0J9Sh2XhCp-M3AFOXJWAKqlersRRNvTIS4GyFmd3MxxigC4-l0bdvz-"}
params = urllib.urlencode({"url": "https://github.com/Mortega5/traffic-incidents",
        "component_id": 'traffic-incidents',
        "description": 'Web component to know the state of the traffic in a certain city',
        "social_network": '',
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "attributes": json.dumps(aux),
        "predetermined": 'True',
        "img": 'images/components/traffic-incidents-icon.png'
        }, doseq=True)
test_utils.make_request("PUT", request_uri, params, 201, None)

aux = {"app-id": "655f716c02b3f0aceac9e3567cfb46a8"}
params = urllib.urlencode({"url": "https://github.com/Mortega5/open-weather",
        "component_id": 'open-weather',
        "description": 'Web component to know the weather in future days',
        "social_network": '',
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "attributes": json.dumps(aux),
        "predetermined": 'True',
        "img": 'images/components/open-weather-icon.png'
        }, doseq=True)
test_utils.make_request("PUT", request_uri, params, 201, None)

aux = {}
params = urllib.urlencode({"url": 'https://github.com/Mortega5/finance-search',
        "component_id": 'finance-search',
        "description": 'Web component to know the values of shares',
        "social_network": '',
        "input_type": 'None',
        "output_type": 'tweet',
        "versions": versions_list,
        "attributes": json.dumps(aux),
        "predetermined": 'True',
        "img": 'images/components/finance-search-icon.png'
        }, doseq=True)

test_utils.make_request("PUT", request_uri, params, 201, None)
