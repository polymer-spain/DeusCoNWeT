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
uri = "htpps://centauro.ls.fi.upm.es"
basepath = "/api/componentes"
request_uri = uri + basepath
params = urllib.urlencode({'url': 'https://github.com/JuanFryS/twitter-timeline',
        'component_id': 'twitter-timeline',
        'description': 'Web component to obtain the timeline of Twitter using Polymer',
        'social_network': 'twitter' ,
        'input_type': 'None',
        'output_type': 'tweet',
        'versions': ['stable', 'accuracy', 'latency']
        })
        test_utils.make_request("PUT", request_uri, params, 201, None)