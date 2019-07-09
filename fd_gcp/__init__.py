"""
Fyndata's library of Google Cloud Platform (GCP) utils
======================================================

Among other things, this library makes it easier to interact with some
GCP services or even mock the interaction with them.

Each module that is dedicated to interact with an specific GCP service is named
``gcp_{service_acronym}`` e.g. :mod:`gcp_kms`.

There are other modules for the external users of the library such as
:mod:`exceptions` and :mod:`auth`.


Google Resource Name (GRN)
--------------------------

The terms *resource name* and *resource id* are used extensively in GCP's
documentation and code. Because of the reasons below, for GCP we created an
analogy of AWS' concept of *Amazon Resource Name* (ARN): *Google Resource Name*
(GRN).

- Using the word "name" of X might be misleading since it seems too casual
  and one could easily say "the name of that key ring is ``my-keyring``" but
  that would be wrong: the format of the name of a key ring resource is
  ``projects/[PROJECT_ID]/locations/[LOCATION_ID]/keyRings/[KEY_RING_ID]``.
- It is annoying to have code entities named such as
  ``kms_crypto_key_resource_name`` (unlike ``kms_crypto_key_id``).

"""


__version__ = '0.1.2'
