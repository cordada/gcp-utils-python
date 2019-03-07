"""
A mock version of module :mod:`.gcp_kms`.

The code in this module does not make any external requests.

"""
import base64
import uuid

import cryptography.fernet

from .gcp_kms import GcpCredentials, GcpResource  # noqa: F401
from .gcp_kms import (  # noqa: F401
    compose_crypto_key_grn,
    compose_crypto_key_version_grn,
    compose_key_ring_grn,
    compose_location_grn,
    compose_project_grn,
)
from .gcp_kms import (  # noqa: F401
    KMS_LOCATION_ID_MAX_LENGTH_ESTIMATION,
    KMS_KEY_RING_ID_MAX_LENGTH,
    KMS_KEY_RING_ID_REGEX,
    KMS_CRYPTO_KEY_ID_MAX_LENGTH,
    KMS_CRYPTO_KEY_ID_REGEX,
    KMS_ENCRYPTION_PLAIN_DATA_MAX_SIZE,
)


###############################################################################
# KMS API operations - crypto key
###############################################################################

def create_crypto_key(
    api_client: object,
    key_ring_grn: str,
    crypto_key_id: str = None,
) -> str:
    """
    Create a crypto key (mock) within a key ring.

    Useful for mocking :func:`.gcp_kms.create_crypto_key`.

    :return: crypto key GRN

    """
    # TODO: see TODOs in '.gcp_kms.create_crypto_key'

    crypto_key_id = crypto_key_id or uuid.uuid4().hex
    crypto_key_grn = '{}/cryptoKeys/{}'.format(
        key_ring_grn,
        crypto_key_id,
    )

    return crypto_key_grn


def encrypt(
    api_client: object,
    crypto_key_grn: str,
    plain_data: bytes,
) -> bytes:
    """
    Encrypt binary ``plain_data`` locally, without using GCP KMS.

    Useful for mocking :func:`.gcp_kms.encrypt`.

    """
    if not isinstance(plain_data, bytes):
        raise TypeError("Type of 'plain_data' is not bytes.")
    if len(plain_data) > KMS_ENCRYPTION_PLAIN_DATA_MAX_SIZE:
        raise ValueError("Size of 'plain_data' exceeds max size.")

    fernet_key_input = crypto_key_grn[-32:].encode(encoding='ascii')
    fernet_key = _generate_fernet_key(fernet_key_input)

    f = cryptography.fernet.Fernet(fernet_key)
    encrypted_data: bytes = f.encrypt(plain_data)

    return encrypted_data


def decrypt(
    api_client: object,
    crypto_key_grn: str,
    encrypted_data: bytes,
) -> bytes:
    """
    Decrypt binary ``encrypted_data``locally, without using GCP KMS.

    Useful for mocking :func:`.gcp_kms.decrypt`.

    """
    fernet_key_input = crypto_key_grn[-32:].encode(encoding='ascii')
    fernet_key = _generate_fernet_key(fernet_key_input)

    f = cryptography.fernet.Fernet(fernet_key)
    plain_data: bytes = f.decrypt(encrypted_data)

    return plain_data


###############################################################################
# internal helpers
###############################################################################

def _generate_fernet_key(value: bytes) -> bytes:
    # Based on 'cryptography.fernet.Fernet.generate_key'.
    if not isinstance(value, bytes):
        raise TypeError
    if len(value) != 32:
        raise ValueError
    return base64.urlsafe_b64encode(value)
