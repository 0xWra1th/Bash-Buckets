from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Index View For BashBucket API
def index(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\">Hello, Welcome to the <i style=\"color: red\">Bash Bucket</i> cloud storage API!</h2></center></html>")

# Analytics For BashBucket API
def analytics(request):
	return HttpResponse("<html style=\"background-color: black;color: white\"><center><h2 style=\"margin-top:10%\"><i style=\"color: red\">Bash Bucket</i> Instance Server Analytics!</h2><br><h3>Beep, boop...beep!</h3</center></html>")

# List Files/Folders in given bucket if Auth token is valid
def listFiles(request):
	if(request.method == 'POST'):
		data = {
			"status":"Undetermined",
			"list": [
				"cats.txt",
				"dogs.txt",
				"Files (dir)",
			],
		}
		res = JsonResponse(data)
		return res
	else:
		return HttpResponse(status=405)
