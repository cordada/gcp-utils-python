"""
Authentication and authorization utilities.

"""
import logging

import google.auth.compute_engine
import google.auth.credentials
import google.auth.exceptions

from . import exceptions
from .common import GcpCredentials

# Make sure package 'cryptography' is available for 'google.auth', which prefers that lib instead
#   of falling back (silently) to package 'rsa' (pure Python).
#   https://github.com/googleapis/google-auth-library-python/blob/v1.5.1/google/auth/crypt/rsa.py#L19
try:
    import google.auth.crypt._cryptography_rsa
except ImportError as exc:  # pragma: no cover
    msg = "Package 'cryptography' is required for optimum performance of 'google.auth'."
    raise ImportError(msg) from exc


logger = logging.getLogger(__name__)


def get_env_default_credentials() -> GcpCredentials:
    """
    Return the default credentials for the current GCP environment.

    .. warning:: if the env var ``GOOGLE_APPLICATION_CREDENTIALS`` is set, then
        the returned value might correspond to something else.

    """
    try:
        credentials, _ = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError as exc:
        raise exceptions.AuthError from exc
    return credentials


def get_env_project_id() -> str:
    """
    Return the project ID of the current GCP environment.

    .. warning:: if the env var ``GOOGLE_APPLICATION_CREDENTIALS`` is set, then
        the returned value might correspond to something else.

    """
    try:
        _, project_id = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError as exc:
        raise exceptions.AuthError from exc
    if not isinstance(project_id, str):
        raise exceptions.Error("Unexpected Google Auth lib response.", project_id)

    return project_id


def get_gce_credentials(service_account_email: str = None) -> GcpCredentials:
    """
    Return credentials provided by Compute Engine service account.

    .. warning:: This function does not attempt to authenticate or verify that
        the ``service_account_email`` does indeed exist. It will return a
        credentials object anyway.

    A Compute Engine instance may have multiple service accounts.

    `Google's Auth Library for Python docs`_ say:

       "Applications running on Compute Engine, Container Engine, or the
       App Engine flexible environment can obtain credentials provided by
       Compute Engine service accounts."

    .. _Google's Auth Library for Python docs:
         https://google-auth.readthedocs.io/en/latest/user-guide.html#compute-engine-container-engine-and-the-app-engine-flexible-environment

    """
    service_account_email = service_account_email or 'default'
    return google.auth.compute_engine.Credentials(service_account_email)


def load_credentials_from_file(filename: str) -> GcpCredentials:
    credentials, _ = google.auth._default._load_credentials_from_file(filename)
    return credentials
