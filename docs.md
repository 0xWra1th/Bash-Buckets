# API Documentation

## Create a Bucket
#### URL: ```api/createBucket```
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
#### URL: ```api/deleteBucket```
#### _REQUEST_
deleteBucket takes a JSON object in a POST request.<br>
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

## List a users Buckets
#### URL: ```api/listBuckets```
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
