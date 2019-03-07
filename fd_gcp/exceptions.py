"""
Exceptions that may be exposed to the users of this library.

"""
import logging
import re
from typing import Optional

import googleapiclient.errors
import httplib2


logger = logging.getLogger(__name__)


class Error(Exception):

    """
    Base class for Google/GCP errors.

    """

    def __repr__(self) -> str:
        return str(self)


class AuthError(Error):

    """
    Google/GCP authentication or authorization error.

    """


class ResourcePermissionDenied(Error):

    """
    Permission denied on a resource.

    For ``HttpError`` exception with "reason":
        "Permission '<permission>' denied for resource '<resource>'."

    """

    def __init__(self, resource: str = None, permission: str = None) -> None:
        """Constructor.

        :param resource: a resource's ID, GRN or some other identifier
        :param permission: a permission's ID, GRN or some other identifier

        """
        self.resource = resource
        self.permission = permission

    def __str__(self) -> str:
        resource_str = self.resource or 'unkwnown'
        permission_str = self.permission or 'unkwnown'

        return "Permission '{permission}' denied for resource '{resource}'.".format(
            resource=resource_str,
            permission=permission_str,
        )


class ResourceNotFound(Error):

    """
    Resource Not Found error.

    For ``HttpError`` exception with "reason":
        "<resource_type> <resource> not found."

    .. warning::
        It might happen that the resource does exist but with the request's
        credentials it is not accessible.

    """

    def __init__(self, resource: str = None) -> None:
        """Constructor.

        :param resource: a resource's ID, GRN or some other identifier

        """
        self.resource = resource

    def __str__(self) -> str:
        resource_str = self.resource or 'unkwnown'

        return "Resource '{resource}' not found.".format(resource=resource_str)


class AlreadyExists(Error):

    """
    Something already exists.

    """

    def __init__(self, what: str) -> None:
        self.what = what

    def __str__(self) -> str:
        return "{what} already exists.".format(what=self.what)


class UnrecognizedApiError(Error):

    """
    Unrecognized Google API ``Error``.

    """

    def __str__(self) -> str:
        return "Unrecognized Google API error."


class UnrecognizedApiHttpError(UnrecognizedApiError):

    """
    Unrecognized Google API ``HttpError``.

    """

    def __init__(self, exc: googleapiclient.errors.HttpError) -> None:
        self.response: httplib2.Response = exc.resp
        self.response_content: bytes = exc.content
        self.request_uri: str = exc.uri
        self.error_reason = "unknown error reason"

        try:
            self.error_reason = exc._get_reason().strip()
        except Exception:
            pass

    def __str__(self) -> str:
        return "Unrecognized Google API HTTP error: {error_reason}.".format(
            error_reason=self.error_reason)


def process_googleapiclient_http_error(
    exc: googleapiclient.errors.HttpError,
) -> Exception:

    new_exc = None
    new_exc = new_exc or _detect_resource_permission_denied(exc)
    new_exc = new_exc or _detect_resource_not_found(exc)
    new_exc = new_exc or _detect_already_exists(exc)

    # TODO: add more cases as they are detected.
    # new_exc = new_exc or _detect_xyz(exc)

    new_exc = new_exc or UnrecognizedApiHttpError(exc)

    return new_exc


def _detect_resource_permission_denied(
    exc: googleapiclient.errors.HttpError,
) -> Optional[Exception]:
    new_exc = None

    try:
        exc_reason = exc._get_reason().strip()
        re_pattern = re.compile(
            r"^Permission '(?P<permission>[a-zA-Z0-9\.]*)' denied for resource '(?P<resource>.*)'\."
        )
        re_match = re_pattern.match(exc_reason)

        if re_match:
            resource = None
            permission = None
            try:
                permission = re_match.group('permission')
            except IndexError:
                pass
            try:
                resource = re_match.group('resource')
            except IndexError:
                pass
            new_exc = ResourcePermissionDenied(resource, permission)
    except Exception:
        pass

    return new_exc


def _detect_resource_not_found(
    exc: googleapiclient.errors.HttpError,
) -> Optional[Exception]:
    new_exc = None

    try:
        exc_reason = exc._get_reason().strip()
        re_pattern = re.compile(r"^(?P<resource_type>[a-zA-Z0-9_]+) (?P<resource>.+) not found\.")
        re_match = re_pattern.match(exc_reason)

        if re_match:
            try:
                resource = re_match.group('resource')
            except IndexError:
                resource = 'some resource'
            new_exc = ResourceNotFound(resource)
    except Exception:
        pass

    return new_exc


def _detect_already_exists(
    exc: googleapiclient.errors.HttpError,
) -> Optional[Exception]:
    new_exc = None

    try:
        exc_reason = exc._get_reason().strip()
        re_pattern = re.compile(r"^(?P<what>.*) already exists\.")
        re_match = re_pattern.match(exc_reason)

        if re_match:
            try:
                what = re_match.group('what')
            except IndexError:
                what = 'something'
            new_exc = AlreadyExists(what)
    except Exception:
        pass

    return new_exc
