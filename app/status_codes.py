

HTTP_200_OK = 200 
# OK; the request has succeeded.

HTTP_201_CREATED = 201  
# Created; indicates that the request has been fulfilled and has resulted in the creation of a new resource.

HTTP_204_NO_CONTENT = 204  
# No Content (DELETE);  the server has successfully processed the request, but there is no content to send in the response.

HTTP_400_BAD_REQUEST = 400  
# Bad Request; the server cannot or will not process the request due to an apparent client error

HTTP_401_UNAUTHORIZED = 401  
# Unauthorized; the request has not been applied because it lacks valid authentication credentials for the target resource.

HTTP_404_NOT_FOUND = 404  
# Not Found; the server cannot find the requested resource.

HTTP_409_CONFLICT = 409
# Conflict; indicates that the request could not be processed because of conflict in the request, such as an edit conflict.

HTTP_500_INTERNAL_SERVER_ERROR = 500  
# Internal Server Error; indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
