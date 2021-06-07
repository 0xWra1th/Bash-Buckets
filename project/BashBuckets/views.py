# IMPORTED RESOURCES
from os import name
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Bucket, User, UserBucket
from subprocess import CalledProcessError, check_output
from django.core.files.storage import default_storage
import json
from django.views.decorators.csrf import csrf_exempt

# ------------------------------- DISPLAY INDEX -------------------------------
# Index View For BashBucket API
def index(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\">Hello, Welcome to the <i style=\"color: red\">Bash Bucket</i> cloud storage API!</h2></center></html>")
# -----------------------------------------------------------------------------

# ----------------------------- DISPLAY ANALYTICS -----------------------------
# Analytics For BashBucket API
def analytics(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\"><i style=\"color: red\">Bash Bucket</i> Instance Server Analytics!</h2><br><h3>Beep, boop...beep!</h3</center></html>")
# -----------------------------------------------------------------------------

# -------------------------------- LIST FILES ---------------------------------
# List Files/Folders in given bucket if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def listFiles(request):
	if(request.method == 'POST'):
		# Get request data
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
			UserBucket.objects.get(user=userObj, bucket=bucketObj)
		except Exception as e:
			res = HttpResponse("UNAUTHORISED: "+str(e), status=401)
			return res


	# 2) Retrieve folders and files from bucket (Bash -> 'ls' in supplied dir)
		# Format Directory String
		if len(path) != 0:
			if path[len(path)-1] == '/':
				if path[0] == '/':
					dir = "buckets/"+bucket+path
				else:
					dir = "buckets/"+bucket+"/"+path
			else:
				if path[0] == '/':
					dir = "buckets/"+bucket+path+"/"
				else:
					dir = "buckets/"+bucket+"/"+path+"/"
		else:
			dir = "buckets/"+bucket+"/"
		
		# Santize Directory (RCE is no joke.)
		if (';' in dir) or ('|' in dir) or ('<' in dir) or ('>' in dir):
			res = HttpResponse("ERROR: Path or Bucket contains illegal characters.", status=400)
			return res

		# Call script with args
		try:
			scriptRes = check_output("./scripts/list_files.sh \""+str(dir)+"\"", shell=True)
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
# -----------------------------------------------------------------------------


# -------------------------------- UPLOAD FILE --------------------------------
# Upload Files in given bucket and path if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def uploadFile(request):
	if(request.method == 'POST'):
		# Get request data
		print(request.POST)
		bucket = request.POST.get('bucket')
		path = request.POST.get('path')
		token = request.POST.get('token')
		file = request.FILES['file']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		try:
			userObj = User.objects.get(token=token)
			bucketObj = Bucket.objects.get(name=bucket)
			UserBucket.objects.get(user=userObj, bucket=bucketObj)
		except Exception as e:
			res = HttpResponse("UNAUTHORISED: "+str(e), status=401)
			return res

	# 2) Save file in bucket
		# Format directory where the file will be saved
		if len(path) != 0:
			if path[len(path)-1] == '/':
				if path[0] == '/':
					dir = "buckets/"+bucket+path
				else:
					dir = "buckets/"+bucket+"/"+path
			else:
				if path[0] == '/':
					dir = "buckets/"+bucket+path+"/"
				else:
					dir = "buckets/"+bucket+"/"+path+"/"
		else:
			dir = "buckets/"+bucket+"/"
		
		# Save file to specified directory
		try:
			default_storage.save(dir+file.name, file)
		except CalledProcessError:
			res = HttpResponse("Invalid path or bucket.", status=400)
			return res

	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success"}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------

