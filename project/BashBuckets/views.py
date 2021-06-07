# IMPORTED RESOURCES
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import AppToken, Bucket, User, UserBucket
from subprocess import CalledProcessError, check_output
from django.core.files.storage import default_storage
import json, uuid
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
		valid = validateBucketToken(token, bucket, False)
		if valid != True:
			return valid


	# 2) Retrieve folders and files from bucket (Bash -> 'ls' in supplied dir)
		# Format Directory String
		dir = formatDirectory(path, bucket)
		
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
# Upload File to given bucket and path if Auth token is valid

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
		valid = validateBucketToken(token, bucket, False)
		if valid != True:
			return valid

	# 2) Save file in bucket
		# Format directory where the file will be saved
		dir = formatDirectory(path, bucket)
		
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


# -------------------------------- DELETE FILE --------------------------------
# Delete File in a given bucket and path if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def deleteFile(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		path = content['path']
		file = content['filename']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateBucketToken(token, bucket, False)
		if valid != True:
			return valid

	# 2) Delete file from bucket
		# Format directory where the file is currently stored
		dir = formatDirectory(path, bucket)
		
		# Delete file from specified directory
		try:
			default_storage.delete(dir+file)
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


# ------------------------------- CREATE FOLDER -------------------------------
# Create a new folder in a given bucket and path if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def createFolder(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		path = content['path']
		folder = content['folder']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateBucketToken(token, bucket, False)
		if valid != True:
			return valid

	# 2) Create new folder in bucket
		# Format directory where the folder is to be created
		dir = formatDirectory(path, bucket)+folder

		# Santize Input (RCE is no joke.)
		if (';' in dir) or ('|' in dir) or ('<' in dir) or ('>' in dir):
			res = HttpResponse("ERROR: Path or Bucket contains illegal characters.", status=400)
			return res

		# Call script with args
		try:
			check_output("./scripts/create_folder.sh \""+str(dir)+"\"", shell=True)
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


# ------------------------------- CREATE BUCKET -------------------------------
# Create a new bucket if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def createBucket(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateUser(token)
		if type(valid) is HttpResponse:
			return valid
		else:
			userObj = valid[1]

	# 2) Create new bucket
		# Format directory of new bucket
		dir = "buckets/"+bucket
		
		# Santize Input (RCE is no joke.)
		if (';' in dir) or ('|' in dir) or ('<' in dir) or ('>' in dir):
			res = HttpResponse("ERROR: Path or Bucket contains illegal characters.", status=400)
			return res

		# Call script with args
		try:
			check_output("./scripts/create_folder.sh \""+str(dir)+"\"", shell=True)
		except CalledProcessError:
			res = HttpResponse("Invalid bucket name.", status=400)
			return res

	# 3) Add new bucket and userbucket to database
		bucketObj = Bucket(name=bucket)
		bucketObj.save()
		UserBucket(user=userObj, bucket=bucketObj).save()

	# 4) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success"}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# ----------------------------- CREATE APP TOKEN ------------------------------
# Create a new app token that allows for bucket read/write permissions

# FOR TESTING ONLY
@csrf_exempt

def createToken(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateUser(token)
		if type(valid) is HttpResponse:
			return valid

	# 2) Validate bucket and add new token to database
		try:
			bucketObj = Bucket.objects.get(name=bucket)
			newTok = AppToken(bucket=bucketObj)
			newTok.save()
		except Exception as e:
			res = HttpResponse("ERROR: Bucket does not exist"+str(e), status=401)
			return res
		
	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success", "token": newTok.token}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# ------------------------------- DELETE FOLDER -------------------------------
# Delete Folder in a given bucket and path if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def deleteFolder(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		path = content['path']
		folder = content['folder']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateBucketToken(token, bucket, False)
		if valid != True:
			return valid

	# 2) Delete Folder from bucket
		# Format directory where the Folder is currently stored
		dir = formatDirectory(path, bucket)
		dir = dir+folder
		
		# Santize Input (RCE is no joke.)
		if (';' in dir) or ('|' in dir) or ('<' in dir) or ('>' in dir):
			res = HttpResponse("ERROR: Path or Bucket contains illegal characters.", status=400)
			return res
		
		# Call script with args
		try:
			check_output("./scripts/delete_dir.sh \""+str(dir)+"\"", shell=True)
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


# ------------------------------- DELETE BUCKET -------------------------------
# Delete a given Bucket if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def deleteBucket(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateBucketToken(token, bucket, True)
		if valid != True:
			return valid

	# 2) Delete Bucket
		# Format directory where the Bucket is currently stored
		dir = "buckets/"+bucket

		# Santize Input (RCE is no joke.)
		if (';' in dir) or ('|' in dir) or ('<' in dir) or ('>' in dir):
			res = HttpResponse("ERROR: Path or Bucket contains illegal characters.", status=400)
			return res
		
		# Call script with args
		try:
			check_output("./scripts/delete_dir.sh \""+str(dir)+"\"", shell=True)
		except CalledProcessError:
			res = HttpResponse("Invalid path or bucket.", status=400)
			return res
		
		# Delete Bucket, UserBucket and AppTokens records from database
		bucketObj = Bucket.objects.get(name=bucket)
		UserBucket.objects.get(bucket=bucketObj).delete()
		for tok in AppToken.objects.filter(bucket=bucketObj):
			tok.delete()
		bucketObj.delete()

	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success"}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# ------------------------------- LIST BUCKETS --------------------------------
# List User or App Token Buckets

# FOR TESTING ONLY
@csrf_exempt

def listBuckets(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		token = content['token']

	# 1) Determine if token is User or App and Get Buckets
		userToken = True
		try:
			userObj = User.objects.get(token=token)
		except Exception as e:
			userToken = False
		
		try:
			tokenObj = AppToken.objects.get(token=token)
		except Exception as e:
			res = HttpResponse("Invalid Token!", status=401)
		
		if userToken:
			buckets = UserBucket.objects.filter(user=userObj)
		else:
			buckets = Bucket.objects.get(id=tokenObj.bucket_id)

	# 2) Format Buckets into a list
		list = []
		if userToken:
			for bucket in buckets:
				list.append(Bucket.objects.get(id=bucket.bucket_id).name)
		else:
			list.append(buckets.name)

	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"buckets": list}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# -------------------------------- DELETE TOKEN -------------------------------
# Delete an App Token if Auth token is valid

# FOR TESTING ONLY
@csrf_exempt

def deleteToken(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		apptoken = content['apptoken']
		token = content['token']

	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateUser(token)
		if type(valid) is HttpResponse:
			return valid


	# 2) Delete App Token
		try:
			print("HERE")
			AppToken.objects.get(token=apptoken).delete()
		except Exception:
			res = HttpResponse("Invalid App Token!", status=401)
			return res

	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success"}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# -------------------------------- LIST TOKENS --------------------------------
# List App Tokens for User

# FOR TESTING ONLY
@csrf_exempt

def listTokens(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		token = content['token']
	
	# 1) Validate Auth Token (Database)
		# Validate token against DB
		valid = validateUser(token)
		if type(valid) is HttpResponse:
			return valid
		user = valid[1]

	# 2) Retrieve and Format Tokens into a list
		buckets = UserBucket.objects.filter(user=user)
		list = []
		for bucket in buckets:
			for tok in AppToken.objects.filter(bucket=Bucket.objects.get(id=bucket.bucket_id)):
				list.append(tok.token)

	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"tokens": list}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# ---------------------------- VALIDATE BUCKET TOKEN --------------------------
def validateBucketToken(token, bucket, UserOnly):
	# Validate token against DB
	# Is the operation allowed via app token or only user tokens?
	if UserOnly:
		try:
			userObj = User.objects.get(token=token)
			bucketObj = Bucket.objects.get(name=bucket)
			UserBucket.objects.get(user=userObj, bucket=bucketObj)
			return True
		except Exception as e:
			res = HttpResponse("UNAUTHORISED: User token or bucket invalid!", status=401)
			return res
	else:
		# Check if token is a user token
		try:
			userObj = User.objects.get(token=token)
			bucketObj = Bucket.objects.get(name=bucket)
			UserBucket.objects.get(user=userObj, bucket=bucketObj)
			return True
		except Exception as e:
			pass

		# Check if token is an app token
		try:
			bucketObj = Bucket.objects.get(name=bucket)
			AppToken.objects.get(token=token, bucket=bucketObj)
			return True
		except Exception as e:
			res = HttpResponse("ERROR: Token or bucket is invalid.", status=401)
			return res
# -----------------------------------------------------------------------------


# -------------------------------- VALIDATE USER ------------------------------
def validateUser(token):
	# Validate token against DB
	try:
		user = User.objects.get(token=token)
		return True, user
	except Exception as e:
		res = HttpResponse("UNAUTHORISED: "+str(e), status=401)
		return res
# -----------------------------------------------------------------------------


# ------------------------------ FORMAT DIRECTORY -----------------------------
def formatDirectory(path, bucket):
	# Format directory where the folder is to be created
		if len(path) != 0:
			if path[len(path)-1] == '/':
				if path[0] == '/':
					return "buckets/"+bucket+path
				else:
					return "buckets/"+bucket+"/"+path
			else:
				if path[0] == '/':
					return "buckets/"+bucket+path+"/"
				else:
					return "buckets/"+bucket+"/"+path+"/"
		else:
			return "buckets/"+bucket+"/"
# -----------------------------------------------------------------------------