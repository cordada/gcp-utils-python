from unittest import TestCase

from fd_gcp.exceptions import (  # noqa: F401
    AlreadyExists, AuthError, Error, ResourceNotFound, ResourcePermissionDenied,
    UnrecognizedApiError, UnrecognizedApiHttpError,
    _detect_already_exists, _detect_resource_not_found, _detect_resource_permission_denied,
    process_googleapiclient_http_error,
)


class FunctionsTestCase(TestCase):

    def test__detect_already_exists(self) -> None:
        # TODO: implement test
        # _detect_already_exists()
        pass

    def test__detect_resource_permission_denied(self) -> None:
        # TODO: implement test
        # _detect_resource_permission_denied()
        pass

    def test__detect_resource_not_found(self) -> None:
        # TODO: implement test
        # _detect_resource_not_found()
        pass

    def test_process_googleapiclient_http_error(self) -> None:
        # TODO: implement test
        # process_googleapiclient_http_error()
        pass


class ExceptionsTestCase(TestCase):

    def test_error(self) -> None:
        # TODO: implement test
        # raise Error()
        pass

    def test_auth_error(self) -> None:
        # TODO: implement test
        # raise AuthError()
        pass

    def test_already_exists(self) -> None:
        # TODO: implement test
        # raise AlreadyExists()
        pass

    def test_resource_not_found(self) -> None:
        # TODO: implement test
        # raise ResourceNotFound()
        pass

    def test_resource_permission_denied(self) -> None:
        # TODO: implement test
        # raise ResourcePermissionDenied()
        pass

    def test_unrecognized_api_error(self) -> None:
        # TODO: implement test
        # raise UnrecognizedApiError()
        pass

    def test_unrecognized_api_http_error(self) -> None:
        # TODO: implement test
        # raise UnrecognizedApiHttpError()
        pass
