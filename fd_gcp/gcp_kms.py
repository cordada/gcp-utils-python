"""
GCP KMS (Key Management Service) helpers.

To learn more about:
- KMS service, see https://cloud.google.com/kms/docs/
- KMS objects hierarchy, see https://cloud.google.com/kms/docs/object-hierarchy
- KMS locations, see https://cloud.google.com/kms/docs/locations

In cryptography the terms for encrypted and not-encrypted values/data are
*ciphertext* and *plaintext*, respectively. However, we choose to put these in
layman's terms: *encrypted data* and *plain data*. We do not want to suggest
that the secret to encrypt is text, which is not (it is a bytes sequence), and
"cipher" is not part of an average software developer's vocabulary.


Usage example, in a GCE environment::

    from fd_gcp.auth import get_gce_credentials

    location_grn = compose_location_grn(
        project_id='[PROJECT_ID]',
        location_id='[LOCATION]',
    )

    credentials = get_gce_credentials()
    kms_api_client = create_api_client(credentials)

    key_ring_grn = create_key_ring(
        kms_api_client, location_grn,
        key_ring_id='test-1')
    crypto_key_grn = create_crypto_key(
        kms_api_client, key_ring_grn,
        crypto_key_id='my-crypto-key-1')

    plain_str = "Jürgen loves Ω! ✔ \n\r\t 123"

    plain_data = plain_str.encode(encoding='utf-8', errors='strict')
    encrypted_data = encrypt(kms_api_client, crypto_key_grn, plain_data)
    decrypted_data = decrypt(kms_api_client, crypto_key_grn, encrypted_data)
    decrypted_str = decrypted_data.decode(encoding='utf-8', errors='strict')

    assert plain_str == decrypted_str


.. seealso:

    https://cloud.google.com/kms/docs/reference/libraries
    https://cloud.google.com/kms/docs/how-tos
    https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.html

"""
import base64
import logging
import re
import uuid
from typing import List

import googleapiclient.discovery

from .common import GcpCredentials, GcpResource
from ._http import execute_google_api_client_request


logger = logging.getLogger(__name__)


###############################################################################
# constants
###############################################################################

# note: as of 2018-10-22, we have not found anywhere official the value of this restriction.
# note: as of 2018-10-22, the longest location id is 'northamerica-northeast1' (23 characters).
# https://cloud.google.com/kms/docs/locations
KMS_LOCATION_ID_MAX_LENGTH_ESTIMATION = 48
# TODO: KMS_LOCATION_ID_MAX_LENGTH
# TODO: KMS_LOCATION_ID_REGEX
# TODO: KMS_LOCATION_GRN_MAX_LENGTH
# TODO: KMS_LOCATION_GRN_REGEX

# > [..] regular expression `[a-zA-Z0-9_-]{1,63}`
# https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.html#create
KMS_KEY_RING_ID_MAX_LENGTH = 64
KMS_KEY_RING_ID_REGEX = re.compile(r'^[a-zA-Z0-9_-]{1,63}$')
# TODO: KMS_KEY_RING_GRN_MAX_LENGTH
# TODO: KMS_KEY_RING_GRN_REGEX

# > [..] regular expression `[a-zA-Z0-9_-]{1,63}`
# https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#create
KMS_CRYPTO_KEY_ID_MAX_LENGTH = 64
KMS_CRYPTO_KEY_ID_REGEX = re.compile(r'^[a-zA-Z0-9_-]{1,63}$')
# TODO: KMS_CRYPTO_KEY_GRN_MAX_LENGTH
# TODO: KMS_CRYPTO_KEY_GRN_REGEX

# TODO: KMS_CRYPTO_KEY_VERSION_ID_MAX_LENGTH
# TODO: KMS_CRYPTO_KEY_VERSION_ID_REGEX
# TODO: KMS_CRYPTO_KEY_VERSION_GRN_MAX_LENGTH
# TODO: KMS_CRYPTO_KEY_VERSION_GRN_REGEX

# Max size of the data to encrypt with a KMS crypto key.
# > The maximum size depends on the key version's protection_level. For SOFTWARE keys, the plaintext
# > must be no larger than 64KiB. [..]
# https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#encrypt
KMS_ENCRYPTION_PLAIN_DATA_MAX_SIZE = 64 * 1024  # 64 KiB


###############################################################################
# resource GRN functions
###############################################################################

# The object hierarchy is:
#   'projects/[PROJECT_ID]/locations/[LOCATION]/keyRings/[KEY_RING]/cryptoKeys/[KEY]/cryptoKeyVersions/[VERSION]'

def compose_project_grn(
    project_id: str,
) -> str:
    # TODO: validate params individually or the concat result
    return 'projects/{}'.format(
        project_id,
    )


def compose_location_grn(
    project_id: str,
    location_id: str,
) -> str:
    # TODO: validate params individually or the concat result
    return 'projects/{}/locations/{}'.format(
        project_id,
        location_id,
    )


def compose_key_ring_grn(
    project_id: str,
    location_id: str,
    key_ring_id: str,
) -> str:
    # TODO: validate params individually or the concat result
    return 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id,
        location_id,
        key_ring_id,
    )


def compose_crypto_key_grn(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    crypto_key_id: str,
) -> str:
    # TODO: validate params individually or the concat result
    return 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id,
        location_id,
        key_ring_id,
        crypto_key_id,
    )


def compose_crypto_key_version_grn(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    crypto_key_id: str,
    crypto_key_version_id: str,
) -> str:
    # TODO: validate params individually or the concat result
    return 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/{}'.format(
        project_id,
        location_id,
        key_ring_id,
        crypto_key_id,
        crypto_key_version_id,
    )


###############################################################################
# KMS API operations
###############################################################################

def create_api_client(credentials: GcpCredentials) -> GcpResource:
    """Create a KMS API client.

    .. warning:: Auth checks do not happen here.

    """
    api_client = googleapiclient.discovery.build(
        serviceName='cloudkms',
        version='v1',
        credentials=credentials,
    )
    return api_client


###############################################################################
# KMS API operations - key ring
###############################################################################

def create_key_ring(
    api_client: GcpResource,
    location_grn: str,
    key_ring_id: str,
) -> str:
    """
    Create a key ring in the given location.

    .. seealso::
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.html#create

    Code largely based on
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/567ef35/kms/api-client/snippets.py

    :return: key ring GRN

    """
    # TODO: validate param 'key_ring_id'

    request = api_client.projects().locations().keyRings().create(
        parent=location_grn,
        body={},
        keyRingId=key_ring_id,
    )
    response = execute_google_api_client_request(request)
    key_ring_grn: str = response['name']

    return key_ring_grn


###############################################################################
# KMS API operations - crypto key
###############################################################################

def create_crypto_key(
    api_client: GcpResource,
    key_ring_grn: str,
    crypto_key_id: str = None,
) -> str:
    """
    Create a crypto key within a key ring.

    .. seealso::
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#create

    Code largely based on
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/567ef35/kms/api-client/snippets.py

    :return: crypto key GRN

    """
    # TODO: validate param 'crypto_key_id'

    crypto_key_id = crypto_key_id or uuid.uuid4().hex

    request = api_client.projects().locations().keyRings().cryptoKeys().create(
        parent=key_ring_grn,
        body={'purpose': 'ENCRYPT_DECRYPT'},
        cryptoKeyId=crypto_key_id,
    )
    response = execute_google_api_client_request(request)
    crypto_key_grn: str = response['name']

    return crypto_key_grn


def encrypt(
    api_client: GcpResource,
    crypto_key_grn: str,
    plain_data: bytes,
) -> bytes:
    """
    Encrypt binary ``plain_data``.

    .. seealso::
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#encrypt

    Code largely based on
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/567ef35/kms/api-client/snippets.py

    """
    # TODO: handle encryption/decryption errors

    if not isinstance(plain_data, bytes):
        raise TypeError("Type of 'plain_data' is not bytes.")
    if len(plain_data) > KMS_ENCRYPTION_PLAIN_DATA_MAX_SIZE:
        raise ValueError("Size of 'plain_data' exceeds max size.")

    plain_data_b64_str = base64.b64encode(plain_data).decode('ascii', errors='strict')

    request = api_client.projects().locations().keyRings().cryptoKeys().encrypt(
        name=crypto_key_grn,
        body={'plaintext': plain_data_b64_str},
    )
    response = execute_google_api_client_request(request)
    encrypted_data_b64_str = response['ciphertext']

    encrypted_data = base64.b64decode(encrypted_data_b64_str.encode('ascii', errors='strict'))

    return encrypted_data


def decrypt(
    api_client: GcpResource,
    crypto_key_grn: str,
    encrypted_data: bytes,
) -> bytes:
    """
    Decrypt binary ``encrypted_data``.

    .. seealso::
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#decrypt

    Code largely based on
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/567ef35/kms/api-client/snippets.py

    """
    # TODO: validate param 'encrypted_data'
    # TODO: handle encryption/decryption errors

    encrypted_data_b64_str = base64.b64encode(encrypted_data).decode('ascii', errors='strict')

    request = api_client.projects().locations().keyRings().cryptoKeys().decrypt(
        name=crypto_key_grn,
        body={'ciphertext': encrypted_data_b64_str},
    )
    response = execute_google_api_client_request(request)
    plain_data_b64_str = response['plaintext']

    plain_data = base64.b64decode(plain_data_b64_str.encode('ascii', errors='strict'))

    return plain_data


###############################################################################
# KMS API operations - crypto key version
###############################################################################

# TODO


###############################################################################
# KMS API operations - IAM policy
###############################################################################

def add_member_to_crypto_key_iam_policy(
    api_client: GcpResource,
    crypto_key_grn: str,
    member: str,
    role: str,
) -> None:
    """
    Add ``member`` with ``role`` to the IAM policy for a crypto key.

    Examples of ``member``:
    - ``user:mike@example.com``
    - ``group:admins@example.com``
    - ``domain:google.com``
    - ``serviceAccount:my-other-app@appspot.gserviceaccount.com``

    Examples of ``role``:
    - ``roles/owner``
    - ``roles/viewer``

    .. seealso::
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#getIamPolicy
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.cryptoKeys.html#setIamPolicy

    Code largely based on
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/567ef35/kms/api-client/snippets.py

    """
    # TODO: validate params 'member', 'role'

    # Get the current IAM policy and add the new member to it.
    policy_request = api_client.projects().locations().keyRings().cryptoKeys().getIamPolicy(
        resource=crypto_key_grn,
    )
    policy_response = execute_google_api_client_request(policy_request)

    bindings: List[dict] = []
    if 'bindings' in policy_response.keys():
        bindings = policy_response['bindings']

    new_binding = {
        'role': role,
        'members': [
            member
        ],
    }
    bindings.append(new_binding)
    policy_response['bindings'] = bindings

    # Set the new IAM Policy.
    request = api_client.projects().locations().keyRings().cryptoKeys().setIamPolicy(
        resource=crypto_key_grn,
        body={'policy': policy_response},
    )
    execute_google_api_client_request(request)


def get_key_ring_iam_policy(
    api_client: GcpResource,
    key_ring_grn: str,
) -> List[dict]:
    """
    Return the IAM policy for a key ring.

    .. seealso::
        https://developers.google.com/resources/api-libraries/documentation/cloudkms/v1/python/latest/cloudkms_v1.projects.locations.keyRings.html#getIamPolicy

    Code largely based on
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/567ef35/kms/api-client/snippets.py

    :return: the list of bindings of the IAM policy for a key ring

    """
    request = api_client.projects().locations().keyRings().getIamPolicy(
        resource=key_ring_grn,
    )
    response = execute_google_api_client_request(request)

    try:
        bindings = response['bindings']  # type: List[dict]
    except KeyError:
        bindings = []
    return bindings
