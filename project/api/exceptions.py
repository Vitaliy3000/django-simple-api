from rest_framework.exceptions import NotAcceptable, NotFound, ParseError


class UserNotFoundFailed(NotFound):
    default_detail = "User not found"


class ResourceDuplicateFailed(ParseError):
    default_detail = "Resource already exists."


class ResourceNotFoundFailed(NotFound):
    default_detail = "Resource not found."


class ResourceQuotaFailed(NotAcceptable):
    default_detail = "Personal quota is finised."


class ResourceMoreNewQuotaFailed(NotAcceptable):
    default_detail = "Personal resources more then new quota."
