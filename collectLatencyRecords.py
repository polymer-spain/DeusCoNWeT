#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import sys
import httplib
import urllib
import json
import webbrowser
import mixpanel_api
import time
from mixpanel_client import MixpanelQueryClient
# import MixPanel
from mixpanel import Mixpanel
mp = Mixpanel("beaf7fb737ad1263205d560568d63d10")

# We set the date to today
START_DATE = time.strftime("%Y-%m-%d")
END_DATE = START_DATE
# La fecha desde la que has empezado a enviar datos a Mixpanel (se usa para ver si hay algún resultado que pueda estar duplicado)
START_STUDY_DATE = "2016-04-12"

# Send metric results to MixPanel
def sendResults(component_name, experiment_id, experiment_timestamp,tag ,result, event_key):
	global mp
	print ">>> Tag de la comparación: ", tag
	print ">>> Diferencia de latencia: ", result
	print ">>> Envio resultados a Mixpanel..."
	mp.track("1111", 'latencyResult', {
			    'component': component_name,
			    'experiment_id': experiment_id,
			    'experiment_timestamp': experiment_timestamp,
			    'tag': tag,
			    'latency': result,
			    #Unique id of metric calculation
			    'result_id': event_key
			})


# Url para obtener nuevo token de facebook: https://developers.facebook.com/tools/explorer/145634995501895/
def main():
	# Instantiates the Query Client
	query_client = MixpanelQueryClient('862a8448704d584ce149704707a0e4e7', '59bf255504e02918c9dc83eb7640144c')
	
	componentNames = ["instagram-timeline", "facebook-wall", "github-events", "googleplus-timeline", "twitter-timeline"]

	if len(sys.argv) == 2 and sys.argv[1] in componentNames:
		component = sys.argv[1]
		print " ### COMPONENTE ", component, "  ###"
		if component == 'googleplus-timeline':
			# Obtain data from mixpanel
			# First, we obtain data generated from host versions. 
			# The method will return a dict, where the field experiment_id will be the key
			# Then we'll obtain the events generated from the components
			query = 'properties["component"]==\"' + component + '\" and properties["version"]=="host"'
			# It returns a dict with all the experiments done today, sorted by event_id (concatenation of experiment_id and request to the API)
			experiments_events_dict = query_client.get_export(START_DATE,END_DATE, 'latencyMetric', where=query, result_key='event_id')

			# We obtain the events related to the results of the latency metric calculated (we'll check for duplicates later)
			query = 'properties["component"]==\"' + component + '\"'
			latency_records = query_client.get_export(START_STUDY_DATE,END_DATE, 'latencyResult', where=query, result_key='result_id')

			# We iterate over the experiments results (obtained from host version), and obtain each group of events related to a specific API request
			for event_id,eventHost in experiments_events_dict.iteritems():
				request = eventHost["request"]
				# We obtain the group of events related to an especific request to the API, as part of one specific experiment
				query = 'properties["component"]==\"' + component + '\" and properties["version"]!="host" and properties["request"]==\"' + request + '\"'
				event_request_dict = query_client.get_export(START_DATE,END_DATE, 'latencyMetric', where=query, result_key='version')
				# We iterate over the results, a dict that contains an event for each client version (stable, accuracy_defects, latency_defects)
				# For each experiment result obtained in host (a certain request to the G+ API), we obtain the results in the different versions
				for event_version, eventClient in event_request_dict.iteritems():
					print "----------------------------------"
					tag = eventClient["version"] + " vs host"
					# We check for duplicate in latency results
					result_id = eventClient["event_id"] + tag
					if not result_id in latency_records:
						# We calculate the differences and send it back to Mixpanel
						latency = eventClient["requestDuration"] - eventHost["requestDuration"]
						sendResults(component, eventHost["experiment_id"], eventClient['experiment_timestamp'], tag, latency, result_id)
					else:
						print ">>> El experimento " + eventClient["experiment_id"] + " con peticion " + eventClient["request"] + " con la comparacion " + tag + " ya se ha calculado previamente, por lo que no volvemos a enviar los calculos"

		else:
			# Obtain data from mixpanel
			# First, we obtain data generated from host versions. 
			# The method will return a dict, where the field experiment_id will be the key
			# Then we'll obtain the events generated from the components
			query = 'properties["component"]==\"' + component + '\" and properties["version"]=="host"'
			experiments_dict = query_client.get_export(START_DATE,END_DATE, 'latencyMetric', where=query, result_key='experiment_id')
			
			# We obtain the calculated metrics on the same range of time data to check if there is any latency records
			#(and to check later for duplicates) 
			query = 'properties["component"]==\"' + component + '\"'
			latency_records = query_client.get_export(START_STUDY_DATE,END_DATE, 'latencyResult', where=query, result_key='result_id')
			
			for experiment_id, experimentHost in experiments_dict.iteritems():
				# Checks if the actual experiment has been calculated (to not send duplicate results)
				print '------------------------------------------------------------------------------------------'
				print ">>> Id del experimento: ", experimentHost['experiment_id']
				# print experimentHost
				# We obtain the event generated for every component experiment (one by component version) 
				query = 'properties["experiment_id"]==\"' + experimentHost['experiment_id'] + '\" and properties["version"]!="host"'
				component_versions_experiments = query_client.get_export(START_DATE, END_DATE, 'latencyMetric', where=query, result_key='version')
				# We iterate over the events related to versions stable, accuracy_defects, latency_defects 
				for key, experimentClient in component_versions_experiments.iteritems():
					print "---------------------------------------"
					tag = experimentClient["version"] + " vs host"
					# We check for duplicate in latency results
					result_id = experimentClient["experiment_id"] + tag
					if not result_id in latency_records:
						# We calculate the differences and send it back to Mixpanel
						latency = experimentClient["requestDuration"] - experimentHost["requestDuration"]
						sendResults(component, experimentHost["experiment_id"], experimentClient['experiment_timestamp'],tag,latency,result_id)
					else:
						print ">>> El experimento " + experimentClient["experiment_id"] + " con la comparacion " + tag + " ya se ha calculado previamente, por lo que no volvemos a enviar los calculos"
	else:
		print "Wrong parameter"
		# {}: Obligatorio, []: opcional
		print "Usage: collectLatencyRecords.py {facebook-wall|instagram-timeline|github-events|googleplus-timeline|twitter-timeline}"


if __name__ == "__main__":
	main()
