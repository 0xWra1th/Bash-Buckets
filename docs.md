# API Documentation

- [Analytics](#analytics)
- [Get User Auth Token](#get-user-auth-token)
- [Create a Bucket](#create-a-bucket)
- [Delete a Bucket](#delete-a-bucket)
- [List a Users Buckets](#list-a-users-buckets)
- [Create a Folder](#create-a-folder)
- [Delete a Folder](#delete-a-folder)
- [Upload a File](#upload-a-file)
- [Delete a File](#delete-a-file)
- [List Files in a Directory](#list-files-in-a-directory)
- [Create an App Token](#create-an-app-token)
- [Delete an App Token](#delete-an-app-token)
- [List a Users App Tokens](#list-a-users-app-tokens)
- [Create a Download Link](#create-a-download-link)
- [Download File](#download-file)
- [Get User Remaining Storage Quota](#get-user-remaining-storage-quota)

## Analytics
A webpage that displays server system stats. CPU usage, memory usage etc...
#### URL: ```/analytics```
#### _REQUEST_
The analytics page is accessed via a GET request<br>
``` 
EXAMPLE:
    http://example.com/analytics
```

#### _RESPONSE_
A HTML document will be served.<br>

## Get User Auth Token
Get a users auth token by sending a matching username and password pair.
#### URL: ```/api/getUserToken```
#### _REQUEST_
getUserToken takes a JSON object in a POST request.<br>
``` 
data = {
    "username": <Username>,
    "password": <User password>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success",
    "token": <User Auth Token>
}
```

## Create a Bucket
Create bucket makes a new bucket and assigns it to the user identified by the provided token.
#### URL: ```/api/createBucket```
#### _REQUEST_
createBucket takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>,
    "bucket": <Name for new bucket>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## Delete a Bucket
Delete bucket deletes a bucket and it's contents if the token provided is the bucket owners token.
#### URL: ```/api/deleteBucket```
#### _REQUEST_
deleteBucket takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>,
    "bucket": <Name of bucket>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## List a Users Buckets
Get a list of all the buckets owned by a user identified by the provided token.
#### URL: ```/api/listBuckets```
#### _REQUEST_
listBuckets takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
```
 data = {
    "buckets": <Names of the buckets owned by the identified user in a list>
}
```

## Create a Folder
Create a new folder within a specified bucket at a specified path if the token is valid.
#### URL: ```/api/createFolder```
#### _REQUEST_
createFolder takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token or App Token>,
    "bucket": <Name of bucket>,
    "path": <Path to folder>,
    "folder": <Name of folder>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## Delete a Folder
Remove a specified folder and it's contents from a bucket if the token is valid.
#### URL: ```/api/deleteFolder```
#### _REQUEST_
deleteFolder takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token or App Token>,
    "bucket": <Name of bucket>,
    "path": <Path to folder>,
    "folder": <Name of folder>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## Upload a File
Upload a file to a path in a bucket if the token is valid.
#### URL: ```/api/uploadFile```
#### _REQUEST_
uploadFile takes a standard POST request with the following data.<br>
``` 
data = {
    "token": <User Auth Token or App Token>,
    "bucket": <Name of bucket>,
    "path": <Path to directory where the file should be stored>,
    "file": <Name of the file>
}
files = {
    "file": <File data>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## Delete a File
Delete a specified file in a bucket if the token provided is valid.
#### URL: ```/api/deleteFile```
#### _REQUEST_
deleteFile takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token or App Token>,
    "bucket": <Name of bucket>,
    "path": <Path to directory where the file is stored>,
    "filename": <Name of the file>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## List Files in a Directory
Get a list of all the files in a specified directory if the token is valid.
#### URL: ```/api/listFiles```
#### _REQUEST_
listFiles takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token or App Token>,
    "bucket": <Name of bucket>,
    "path": <Path to directory>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
```
 data = {
    "files": <Names of the files within the directory>
}
```

## Create an App Token
Create Token makes a new App Token which can be used to access a single bucket and assigns it to the user and bucket identified by the provided parameters.
#### URL: ```/api/createToken```
#### _REQUEST_
createToken takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>,
    "bucket": <Name of bucket>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success",
    "token": <The new App Token>
}
```

## Delete an App Token
Delete App Token deletes the specified App Token if the user auth token is valid.
#### URL: ```/api/deleteToken```
#### _REQUEST_
deleteToken takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>,
    "apptoken": <App Token>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success"
}
```

## List a Users App Tokens
Get a list of all the App Tokens created by a user identified by the provided user auth token.
#### URL: ```/api/listTokens```
#### _REQUEST_
listTokens takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
```
 data = {
    "tokens": <List of App Tokens created by the identified user in a list>
}
```

## Create a Download Link
Create a one time use download link to a specified file in a bucket if the token provided is a valid User Auth or App Token.
#### URL: ```/api/createLink```
#### _REQUEST_
createLink takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token or App Token>,
    "bucket": <Name of bucket>,
    "path": <Path to directory where the file is stored>,
    "filename": <Name of the file>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
``` 
data = {
    "status": "success",
    "link": <The link to download the file>
}
```

## Download File
File downloads require a link created by the createLink endpoint. This link once visited will provide the file and then the link will be invalidated.
#### URL: ```/api/download?code=...```
#### _REQUEST_
api/download takes a code as a query in the URL during a GET request.<br>
``` 
EXAMPLE:
    http://example.com/api/download?code=f64503da-c708-46cc-9cfa-39ec16aef56f
```

#### _RESPONSE_
The GET request will result in the server returning the file attatched to the code provided.<br>
``` 
    File data on success or appropriate HTTP response status if unsuccessful.
```

## Get User Remaining Storage Quota
Get the storage quota remaining for the user identified by the provided user auth token.
#### URL: ```/api/remainingQuota```
#### _REQUEST_
remainingQuota takes a JSON object in a POST request.<br>
``` 
data = {
    "token": <User Auth Token>
}
```

#### _RESPONSE_
A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.<br>
```
 data = {
    "remaining": <Remaining Quota in Megabytes>
}
```