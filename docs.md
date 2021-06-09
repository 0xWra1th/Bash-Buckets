# Bash Buckets

## API Documentation

### Buckets
The whole Bash Buckets system is based off of the simple Bucket entity.

Create a Bucket: ```api/createBucket```
    _REQUEST_
    createBucket takes a JSON object in a POST request.
    ``` data = {
        "token": <User Auth Token>,
        "bucket": <Name for new bucket>
    }```

    _RESPONSE_
    A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.
    ``` data = {
        "status": "success"
    }```

Delete a Bucket: ```api/deleteBucket```
    _REQUEST_
    deleteBucket takes a JSON object in a POST request.
    ``` 
    data = {
        "token": <User Auth Token>,
        "bucket": <Name for new bucket>
    }
    ```

    _RESPONSE_
    A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.
    ``` 
    data = {
        "status": "success"
    }
    ```

List a users Buckets: ```api/listBuckets```
    _REQUEST_
    listBuckets takes a JSON object in a POST request.
    ``` 
    data = {
        "token": <User Auth Token>
    }
    ```

    _RESPONSE_
    A JSON object will be returned upon success otherwise the appropriate HTTP status code will be sent if unsuccessful.
    ```
     data = {
        "buckets": <Names of the buckets owned by the identified user in a list>
    }
    ```