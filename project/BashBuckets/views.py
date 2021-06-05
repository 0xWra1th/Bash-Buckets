from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from subprocess import check_output
import json

# Index View For BashBucket API
def index(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\">Hello, Welcome to the <i style=\"color: red\">Bash Bucket</i> cloud storage API!</h2></center></html>")

# Analytics For BashBucket API
def analytics(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\"><i style=\"color: red\">Bash Bucket</i> Instance Server Analytics!</h2><br><h3>Beep, boop...beep!</h3</center></html>")

# List Files/Folders in given bucket if Auth token is valid
def listFiles(request):
	if(request.method == 'POST'):
		# Get request body
		body = request.body
		content = json.loads(body)

	# 1) Validate Auth Token (Database)
		# Get token and validate against DB


	# 2) Retrieve folders and files from bucket (Bash -> ls in supplied dir)
		# Get parameters and call script
		dir = str(content['bucket'])+str(content['path'])
		scriptRes = check_output("./scripts/test.sh "+str(dir), shell=True)

	# 3) Return JSON Object
		# Decode Script Response into Individual Files/Folders
		list = scriptRes.split(b'\n')
		x = 0
		for item in list:
			list[x] = str(item.decode('utf-8'))
			x+=1
		list.remove('')
		# Format JSON Response and return
		data = {"list": list}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
