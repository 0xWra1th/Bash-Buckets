# IMPORTED RESOURCES
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import AppToken, Bucket, User, UserBucket, DownloadCode
from subprocess import CalledProcessError, check_output
from django.core.files.storage import default_storage
import json, magic


# ----------------------------- DISPLAY ANALYTICS -----------------------------
# Analytics For BashBucket API
def analytics(request):
	# Call script with args
	try:
		scriptRes = check_output("./scripts/analytics.sh", shell=True)
		scriptRes = str(scriptRes.decode('utf-8'))

		# Format output into individual stats
		stats = scriptRes.split("@")
		packages = stats[0][11::]
		kernel = stats[1][21::]
		cpu = stats[2].split('\n')[1]
		mem = stats[3]
		storage = stats[4]
		data = {
			'packages': packages,
			'kernel': kernel,
			'cpu': cpu,
			'mem': mem,
			'storage': storage,
		}
	except CalledProcessError:
		res = HttpResponse("Something broke :(", status=500)
		return res
	return render(request, "BashBuckets/analytics.html", data)
	#return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:5%\"><i style=\"color: red\">Bash Bucket</i> Instance Server Analytics!</h2><pre>"+kernel+"</pre><pre>"+cpu+"</pre><pre>"+mem+"</pre><pre>"+storage+"</pre><textarea style=\"height:650px;width:1000px\">"+packages+"</textarea></center></html>")
# -----------------------------------------------------------------------------


# ------------------------------ GET USER TOKEN -------------------------------
# This function returns the user auth token for a given username password pair (Implemented to make testing easier.)

def getUserToken(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		username = content['username']
		password = content['password']

	# 1) Get token from Database
		try:
			user = User.objects.get(username=username)
			if not user.check_password(password):
				res = HttpResponse("ERROR: Username or Password is incorrect.", status=401)
				return res
		except:
			res = HttpResponse("ERROR: Username or Password is incorrect.", status=401)
			return res

	# 2) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success", "token": str(user.token)}
		res = JsonResponse(data)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# -------------------------------- LIST FILES ---------------------------------
# List Files/Folders in given bucket if Auth token is valid

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
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
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
		data = {"files": list}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# -------------------------------- UPLOAD FILE --------------------------------
# Upload File to given bucket and path if Auth token is valid

def uploadFile(request):
	if(request.method == 'POST'):
		# Get request data
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
		dir = formatDirectory(path, bucket)+file.name

		# Santize Directory (RCE is no joke)
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
			res = HttpResponse("ERROR: File name, Path or Bucket contains illegal characters.", status=400)
			return res
		
		# Get owner of bucket as an object
		try:
			bucketObj = Bucket.objects.get(name=bucket)
			userBucketObj = UserBucket.objects.get(bucket=bucketObj)
			buckerOwner = User.objects.get(id=userBucketObj.user_id)
			remaining = getRemainingQuota(buckerOwner)
		except Exception:
			res = HttpResponse("Error while getting remaining storage space of bucket owner!", status=500)
			return res

		# Check if the bucket owner has remaining space in storage quota
		if (remaining-(file.size/1024/1024)) < 0:
			res = HttpResponse("Owner of bucket does insufficient remaining storage space!", status=400)
			return res

		# Save file to specified directory
		try:
			default_storage.save(dir, file)
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
		# Check path and file are not empty strings
		if path == '' and file == '' :
			res = HttpResponse("ERROR: Path and file fields are empty", status=400)
			return res

		# Format directory where the file is currently stored
		dir = formatDirectory(path, bucket)+file
		
		# Santize Input (Don't want people making links to server files...)
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
			res = HttpResponse("ERROR: Path or File name contains illegal characters.", status=400)
			return res

		# Delete file from specified directory
		try:
			default_storage.delete(dir)
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
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
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
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
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
			res = HttpResponse("ERROR: Bucket does not exist"+str(e), status=400)
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
		# Check path and file are not empty strings
		if path == '' and folder == '' :
			res = HttpResponse("ERROR: Path and folder fields are empty", status=400)
			return res

		# Format directory where the Folder is currently stored
		dir = formatDirectory(path, bucket)+folder
		
		# Santize Input (RCE is no joke.)
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
			res = HttpResponse("ERROR: Path or Folder contains illegal characters.", status=400)
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
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
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


# --------------------------- CREATE DOWNLOAD LINK ----------------------------
# Create a one time download link for a file if Auth token is valid

def createLink(request):
	if(request.method == 'POST'):
		# Get request data
		body = request.body
		content = json.loads(body)
		bucket = content['bucket']
		path = content['path']
		file = content['filename']
		token = content['token']

	# 1) Validate Auth Token (Database) | Does user own bucket?
		# Validate token against DB
		valid = validateBucketToken(token, bucket, False)
		if valid != True:
			return valid

	# 2) Prepare link to file in bucket
		# Format directory where the file is currently stored
		dir = formatDirectory(path, bucket)

		# Santize Input (Don't want people making links to server files...)
		illegalChars = [';', '|', '<', '>', './', '&', '"', "'"]
		if any(char in dir for char in illegalChars):
			res = HttpResponse("ERROR: Path or Bucket contains illegal characters.", status=400)
			return res

		# Check if file exists and create DownloadCode record in database
		if default_storage.exists(dir+file):
			try:
				bucketObj = Bucket.objects.get(name=bucket)
				newCode = DownloadCode(bucket=bucketObj,path=dir+file)
				newCode.save()
			except Exception:
				res = HttpResponse("Error: Database error!", status=500)
				return res
		else:
			res = HttpResponse("File does not exist!", status=400)
			return res

	# 3) Return JSON Object
		# Format JSON Response and return
		data = {"status": "success", "link": request.build_absolute_uri("download?code="+str(newCode.code))}
		res = JsonResponse(data, safe=False)
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# ------------------------------ DOWNLOAD FILE --------------------------------
# Download file with onetime code as url query parameter

def download(request):
	if(request.method == 'GET'):
		# Get request data
		code = request.GET.get('code', '')
	
	# 2) Retrieve file associated with code
		# Retrieve path from database
		try:
			codeObj = DownloadCode.objects.get(code=code)
			filePath = codeObj.path
		except Exception:
			res = HttpResponse("Code is invalid!", status=400)
			return res
		
		# Get file from system and Format HTTP Response
		if default_storage.exists(filePath):
			with open(filePath, 'rb') as file:
				mime = magic.Magic(mime=True)
				type = mime.from_file(filePath)
				res = HttpResponse(file.read(), content_type=type)
				res['Content-Disposition'] = 'inline; filename='+filePath.split('/')[len(filePath.split('/'))-1]
		else:
			res = HttpResponse("File does not exist, may have been deleted. Code will be deleted.", status=400)

	# 3) Delete Download code (It is one time use only!)
		codeObj.delete()

	# 4) Return HTTP Response with file
		return res

	else:
		return HttpResponse(status=405)
# -----------------------------------------------------------------------------


# ----------------------------- GET USER QUOTA --------------------------------
# Get the amount of storage space a user has remaining

def remainingQuota(request):
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

	# 2) Get remaining quota from function
		remaining = getRemainingQuota(user)

	# 5) Return HTTP Response with file
		# Format JSON Response and return
		data = {"remaining": remaining}
		res = JsonResponse(data)
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
			res = HttpResponse("ERROR: Token or bucket is invalid.", status=400)
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


# ---------------------------- GET REMAINING QUOTA -----------------------------
def getRemainingQuota(user):
	# 1) Retrieve user quota
		quota = int(user.usage_limit)

	# 2) Get used storage space
		# Get buckets and total size
		total = 0
		buckets = UserBucket.objects.filter(user=user)
		for bucket in buckets:
			bucketObj = Bucket.objects.get(id=bucket.bucket_id)
			# Call script with args and format output into an int
			try:
				scriptRes = check_output("./scripts/size.sh \"buckets/"+bucketObj.name+"\"", shell=True)
				scriptRes = str(scriptRes.decode('utf-8'))
				size = scriptRes.split("\t")[0]
			except CalledProcessError:
				res = HttpResponse("Something broke :(", status=500)
				return res
			# Add to total in KB
			total+=int(size)

		
	# 3) Calculate remaining storage space in megabytes (Converting total to MB) and return
		remaining = quota-(total/1024)
		return remaining
# -----------------------------------------------------------------------------