from os import name
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Bucket, User, UserBucket
from subprocess import CalledProcessError, check_output
import json
from django.views.decorators.csrf import csrf_exempt

# Index View For BashBucket API
def index(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\">Hello, Welcome to the <i style=\"color: red\">Bash Bucket</i> cloud storage API!</h2></center></html>")

# Analytics For BashBucket API
def analytics(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\"><i style=\"color: red\">Bash Bucket</i> Instance Server Analytics!</h2><br><h3>Beep, boop...beep!</h3</center></html>")

# List Files/Folders in given bucket if Auth token is valid
#######################
#   FOR TESTING ONLY  #
@csrf_exempt
#######################
def listFiles(request):
	if(request.method == 'POST'):
		# Get request body
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		path = content['path']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		try:
			userObj = User.objects.get(token=token)
			bucketObj = Bucket.objects.get(name=bucket)
			userbucketObj = UserBucket.objects.get(user=userObj, bucket=bucketObj)
		except Exception as e:
			res = HttpResponse("UNAUTHORISED: "+str(e), status=401)
			return res


	# 2) Retrieve folders and files from bucket (Bash -> 'ls' in supplied dir)
		# Call script with args
		dir = bucket+path
		try:
			scriptRes = check_output("./scripts/test.sh "+str(dir), shell=True)
		except CalledProcessError:
			res = HttpResponse("Invalid path or bucket.", status=400)
			return res

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
