import logging

#memcache
from google.appengine.api import memcache

def cache_data(key, model_data):
	#add time and values to memcache
	memcache.set(key, model_data)

def get_cached_data(data_id, MODEL):
	key = data_id
	model_data = memcache.get(key)

	if model_data == None:
		#show error in the console 
		logging.error('DB ID QUERY')

		#datastore query is executed
		model_data = MODEL.get_by_id(int(key))	
		#model_data = model_data

		render_time = time.time()
		reload_time = render_time

		#add time and values to memcache
		memcache.set(key, model_data)
	
	return model_data

def reset_cache():
	memcache.flush_all()