# DO NOT RUN DURING PRODUCTION TIME, CSRF IS DISABLED AND THE SERVER IS RESTARTED DURING TESTS AND MAY RESULT IN SECURITY FLAWS.
# This is a script for testing the Bash Buckets Django framework implementation API End-Points.
#
# Why is CSRF disabled during tests?
#	The CSRF token is set via a javascript function during the interaction with the server and is stored as a cookie along with the sessionid.
#	This python script however is not a browser and cannot run javascript to generate the CSRF token,
# 	thus it is easier to just temporarily disable CSRF Protection.
#
# This test file must be run from within the testing directory within the Bash-Buckets root directory. 
# This is so the settings.py can be altered during CSRF disabling and enabling.

# Imported resources
import requests, time, json, sys

# Reused Values
masterToken = str(sys.argv[1]) # Getting super user account token from command link argument
bucketName = 'THE_TEST_BUCKET' # Name of a bucket that will be created during testing
folderName = 'THE_TEST_FOLDER' # Name of a folder that will be created during testing
testFile = open('TEST_FILE.txt', 'rb') # A test file used during upload anf download api calls

# ---------------------------- DISABLE CSRF TOKENS ----------------------------
settings = open('../project/project/settings.py', 'r')
lines = settings.readlines()
lines[34] = "\t#'django.middleware.csrf.CsrfViewMiddleware',\n"

settings = open('../project/project/settings.py', 'w')
settings.writelines(lines)
settings.close()
print("CSRF Disabled for testing.")
time.sleep(3) # Waiting for server to retart after settings change
print("Starting tests...\n")
time.sleep(1)
# -----------------------------------------------------------------------------


# =============================================================================
# |                             TESTING END-POINTS                            |
# =============================================================================

try:
# --------------------------------- INDEX TEST --------------------------------
	url = "http://127.0.0.1:8000/"
	r = requests.post(url)
	if(r.status_code == 200):
		print("\u001b[42m PASS: Index \u001b[0m")
	else:
		print("\u001b[41m FAIL: Index \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------- ANALYTICS TEST ------------------------------
	url = "http://127.0.0.1:8000/analytics"
	r = requests.post(url)
	if(r.status_code == 200):
		print("\u001b[42m PASS: Analytics \u001b[0m")
	else:
		print("\u001b[41m FAIL: Analytics \u001b[0m")
# -----------------------------------------------------------------------------

# ----------------------------- CREATE BUCKET TEST ----------------------------
	url = "http://127.0.0.1:8000/api/createBucket"
	data = {"token": masterToken, "bucket": bucketName}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Create Bucket \u001b[0m")
		else:
			print("\u001b[41m FAIL: Create Bucket \u001b[0m")
	else:
		print("\u001b[41m FAIL: Create Bucket -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ----------------------------- CREATE FOLDER TEST ----------------------------
	url = "http://127.0.0.1:8000/api/createFolder"
	data = {"token": masterToken, "bucket": bucketName, "path": "", "folder": folderName}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Create Folder \u001b[0m")
		else:
			print("\u001b[41m FAIL: Create Folder \u001b[0m")
	else:
		print("\u001b[41m FAIL: Create Folder -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------ UPLOAD FILE TEST -----------------------------
	url = "http://127.0.0.1:8000/api/uploadFile"
	files = {'file': testFile}
	data = {"token": masterToken, "bucket": bucketName, "path": folderName, "file": testFile}
	r = requests.post(url, files=files, data=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Upload File \u001b[0m")
		else:
			print("\u001b[41m FAIL: Upload File \u001b[0m")
	else:
		print("\u001b[41m FAIL: Upload File -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------- LIST FILES TEST -----------------------------
	url = "http://127.0.0.1:8000/api/listFiles"
	data = {"token": masterToken, "bucket": bucketName, "path": folderName}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('files' in resData):
			print("\u001b[42m PASS: List Files \u001b[0m")
		else:
			print("\u001b[41m FAIL: List Files \u001b[0m")
	else:
		print("\u001b[41m FAIL: List Files -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------ LIST BUCKETS TEST ----------------------------
	url = "http://127.0.0.1:8000/api/listBuckets"
	data = {"token": masterToken}
	r = requests.post(url, json=data)
	resData = json.loads(r.text)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('buckets' in resData):
			print("\u001b[42m PASS: List Buckets \u001b[0m")
		else:
			print("\u001b[41m FAIL: List Buckets \u001b[0m")
	else:
		print("\u001b[41m FAIL: List Buckets -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------ CREATE TOKEN TEST ----------------------------
	url = "http://127.0.0.1:8000/api/createToken"
	data = {"token": masterToken, "bucket": bucketName}
	r = requests.post(url, json=data)
	resData = json.loads(r.text)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('token' in resData):
			appToken = resData['token']
			print("\u001b[42m PASS: Create Token \u001b[0m")
		else:
			print("\u001b[41m FAIL: Create Token \u001b[0m")
	else:
		print("\u001b[41m FAIL: Create Token -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------- LIST TOKENS TEST ----------------------------
	url = "http://127.0.0.1:8000/api/listTokens"
	data = {"token": masterToken}
	r = requests.post(url, json=data)
	resData = json.loads(r.text)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('tokens' in resData):
			print("\u001b[42m PASS: List Tokens \u001b[0m")
		else:
			print("\u001b[41m FAIL: List Tokens \u001b[0m")
	else:
		print("\u001b[41m FAIL: List Tokens -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------


# ------------------------------ DELETE TOKEN TEST ----------------------------
	url = "http://127.0.0.1:8000/api/deleteToken"
	data = {"token": masterToken, "apptoken": appToken}
	r = requests.post(url, json=data)
	resData = json.loads(r.text)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Delete Token \u001b[0m")
		else:
			print("\u001b[41m FAIL: Delete Token \u001b[0m")
	else:
		print("\u001b[41m FAIL: Delete Token -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------- CREATE LINK TEST ----------------------------
	url = "http://127.0.0.1:8000/api/createLink"
	data = {"token": masterToken, "bucket": bucketName, "path": folderName, "filename": testFile.name}
	r = requests.post(url, json=data)
	resData = json.loads(r.text)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('link' in resData):
			downloadLink = resData['link']
			uploadSuccess = True
			print("\u001b[42m PASS: Create Link \u001b[0m")
		else:
			print("\u001b[41m FAIL: Create Link \u001b[0m")
	else:
		print("\u001b[41m FAIL: Create Link -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------ DOWNLOAD FILE TEST ---------------------------
	if uploadSuccess:
		r = requests.get(downloadLink)
		if r.status_code == 200:
			print("\u001b[42m PASS: Download File \u001b[0m")
		else:
			print("\u001b[41m FAIL: Download File -> "+str(r.status_code)+" \u001b[0m")
	else:
		print("\u001b[33m UNTESTED: Download File -> Upload must PASS for Download to be tested \u001b[0m")
# -----------------------------------------------------------------------------

# ------------------------------- DELETE FILE TEST ----------------------------
	url = "http://127.0.0.1:8000/api/deleteFile"
	data = {"token": masterToken, "bucket": bucketName, "path": folderName, "filename": testFile.name}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Delete File \u001b[0m")
		else:
			print("\u001b[41m FAIL: Delete File \u001b[0m")
	else:
		print("\u001b[41m FAIL: Delete File -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ----------------------------- DELETE FOLDER TEST ----------------------------
	url = "http://127.0.0.1:8000/api/deleteFolder"
	data = {"token": masterToken, "bucket": bucketName, "path": "", "folder": folderName}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Delete Folder \u001b[0m")
		else:
			print("\u001b[41m FAIL: Delete Folder \u001b[0m")
	else:
		print("\u001b[41m FAIL: Delete Folder -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ----------------------------- DELETE BUCKET TEST ----------------------------
	url = "http://127.0.0.1:8000/api/deleteBucket"
	data = {"token": masterToken, "bucket": bucketName}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('status' in resData):
			print("\u001b[42m PASS: Delete Bucket \u001b[0m")
		else:
			print("\u001b[41m FAIL: Delete Bucket \u001b[0m")
	else:
		print("\u001b[41m FAIL: Delete Bucket -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

# ---------------------------- GET USER QUOTA TEST ----------------------------
	url = "http://127.0.0.1:8000/api/remainingQuota"
	data = {"token": masterToken}
	r = requests.post(url, json=data)
	if r.status_code == 200:
		resData = json.loads(r.text)
		if('remaining' in resData):
			print("\u001b[42m PASS: Get User Quota \u001b[0m")
		else:
			print("\u001b[41m FAIL: Get User Quota \u001b[0m")
	else:
		print("\u001b[41m FAIL: Get User Quota -> "+str(r.status_code)+" \u001b[0m")
# -----------------------------------------------------------------------------

except:
	print("\u001b[41m===========================================================================================\u001b[0m")
	print("\u001b[41m|\u001b[0m ERROR: Could not connect to server, make sure an instance is running on your localhost. \u001b[41m|\u001b[0m")
	print("\u001b[41m===========================================================================================\u001b[0m")
# =============================================================================
# |                              TESTING COMPLETE!                            |
# =============================================================================


# --------------------------- RE-ENABLE CSRF TOKENS ---------------------------
settings = open('../project/project/settings.py', 'r')
lines = settings.readlines()
lines[34] = "\t'django.middleware.csrf.CsrfViewMiddleware',\n"

settings = open('../project/project/settings.py', 'w')
settings.writelines(lines)
print("\nCSRF Re-enabled.")
settings.close()
# -----------------------------------------------------------------------------