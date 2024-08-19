from rest_framework.exceptions import APIException


class CantRateYourself(APIException):
    status_code = 403
    default_detail = "You can't rate your own articles"
    default_code = "forbidden"


class UserAlreadyRated(APIException):
    status_code = 400
    default_detail = "You have already rated this article"
    default_code = "bad request"
