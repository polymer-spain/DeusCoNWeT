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

class NotFoundException(Exception):
	"""NotFound exception"""
	def __init__(self, value):
		self.arg = value
	def __str__(self):
		return repr(self.value)

class RateNotUpdatedException(Exception):
	"""RateNotUpdated exception"""
	def __init__(self, value):
		self.arg = value
	def __str__(self):
		return repr(self.value)

class ComponentAlreadyStoredException(Exception):
	"""RateNotUpdated exception"""
	def __init__(self, value):
		self.arg = value
	def __str__(self):
		return repr(self.value)