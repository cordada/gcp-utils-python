import logging

import google.auth.exceptions
import googleapiclient.errors
import googleapiclient.http
import httplib2

from . import exceptions


logger = logging.getLogger(__name__)


def execute_google_api_client_request(
    request: googleapiclient.http.HttpRequest,
) -> httplib2.Response:
    try:
        response = request.execute()
    except google.auth.exceptions.GoogleAuthError as exc:
        raise exceptions.AuthError from exc
    except googleapiclient.errors.HttpError as exc:
        new_exc = exceptions.process_googleapiclient_http_error(exc)
        raise new_exc from exc
    except googleapiclient.errors.Error as exc:
        raise exceptions.UnrecognizedApiError from exc

    return response
