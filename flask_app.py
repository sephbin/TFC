from flask import Flask
import ghhops_server as hs
import rhino3dm
app = Flask(__name__)
hops = hs.Hops(app)

def cleanDictValues(dictionary):
	# print("cleanDictVal")
	# print(type(dictionary))
	if type(dictionary) == type({}):
		for k,v in dictionary.items():
			# print("\t",type(v))
			if type(v) == type(""):
				dictionary[k] = v.replace("\"","'").replace("\n"," ").replace("ç","c")
			if type(v) == type({}) or type(v) == type([]):
				dictionary[k] = cleanDictValues(v)
	if type(dictionary) == type([]):
		# print("running list")
		for k,v in enumerate(dictionary):
			# print("\t",k,type(v))
			if type(v) == type(""):
				dictionary[k] = v.replace("\"","'").replace("\n"," ").replace("ç","c")
			if type(v) == type({}) or type(v) == type([]):
				dictionary[k] = cleanDictValues(v)
	return dictionary

@hops.component(
	"/requestGet",
	name="requestGet",
	description="requestGet",
	# icon="icons/giraffeGetProject.png",
	inputs = [
		hs.HopsString("url", "U", "url" ),
		hs.HopsString("headers", "H", "headers" ),
	],
	outputs = [
		hs.HopsString("jsonOut", "J", "jsonOut"),
	],
)
def requestGet(url, headers):
	import requests
	import json
	try:
		urls = url.split("|")
		outList = []
		for url_i in urls:
			run = False
			allowedDomains = ['https://api-footprint.techequipt.com.au','https://tgbcalc.com']
			for aD in allowedDomains:
				if url.startswith(aD):
					run = True
			# print("run",run)
			if run:
				cookies_dict = json.loads(headers)
				r = requests.get(url_i, headers=cookies_dict)#cookies=cookies_dict,
				response = r.json()
				# print("response", response, type(response))
				response = cleanDictValues(response)
				# print(response)
				if type(response) == type([]):
					for r in response:
						if type(r) == type({}):
							r["url"] = url_i
					outList = outList+response
				else:
					outList.append(response)
			else:
				return json.dumps({"error":"restricted domain"})
			# return "Hello"
		return outList
	except Exception as e:
		# print("error",e)
		return json.dumps({"error":str(e)})




if __name__ == "__main__":
	app.run()