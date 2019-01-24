from unittest import TestCase

from fd_gcp.gcp_kms import (  # noqa: F401
    add_member_to_crypto_key_iam_policy,
    compose_crypto_key_grn, compose_crypto_key_version_grn, compose_key_ring_grn,
    compose_location_grn, compose_project_grn,
    create_api_client, create_crypto_key, create_key_ring,
    decrypt, encrypt,
    get_key_ring_iam_policy,
)


class ResourceGrnFunctionsTestCase(TestCase):

    def test_compose_project_grn(self) -> None:
        self.assertEqual(
            compose_project_grn(
                project_id='fd-secrets-manager-dev-2',
            ),
            'projects/fd-secrets-manager-dev-2'
        )

    def test_compose_location_grn(self) -> None:
        self.assertEqual(
            compose_location_grn(
                project_id='fd-secrets-manager-dev-2',
                location_id='global',
            ),
            'projects/fd-secrets-manager-dev-2/'
            'locations/global'
        )

    def test_compose_key_ring_grn(self) -> None:
        self.assertEqual(
            compose_key_ring_grn(
                project_id='fd-secrets-manager-dev-2',
                location_id='global',
                key_ring_id='dd06b298-e408-43dd-a553-69ad046a9938',
            ),
            'projects/fd-secrets-manager-dev-2/'
            'locations/global/'
            'keyRings/dd06b298-e408-43dd-a553-69ad046a9938'
        )

    def test_compose_crypto_key_grn(self) -> None:
        self.assertEqual(
            compose_crypto_key_grn(
                project_id='fd-secrets-manager-dev-2',
                location_id='global',
                key_ring_id='dd06b298-e408-43dd-a553-69ad046a9938',
                crypto_key_id='004c9cd1-b4bf-4f9e-98e3-8aebcce6a5a0',
            ),
            'projects/fd-secrets-manager-dev-2/'
            'locations/global/'
            'keyRings/dd06b298-e408-43dd-a553-69ad046a9938/'
            'cryptoKeys/004c9cd1-b4bf-4f9e-98e3-8aebcce6a5a0'
        )

    def test_compose_crypto_key_version_grn(self) -> None:
        self.assertEqual(
            compose_crypto_key_version_grn(
                project_id='fd-secrets-manager-dev-2',
                location_id='global',
                key_ring_id='dd06b298-e408-43dd-a553-69ad046a9938',
                crypto_key_id='f9c9ebbd-e1fa-498b-90cf-89adb8662eb2',
                crypto_key_version_id='1',
            ),
            'projects/fd-secrets-manager-dev-2/'
            'locations/global/'
            'keyRings/dd06b298-e408-43dd-a553-69ad046a9938/'
            'cryptoKeys/f9c9ebbd-e1fa-498b-90cf-89adb8662eb2/'
            'cryptoKeyVersions/1'
        )


class OtherFunctionsTestCase(TestCase):

    def test_create_api_client(self) -> None:
        # TODO: implement test
        # create_api_client()
        pass


class ApiOperationsFunctionsTestCase(TestCase):

    def test_create_key_ring(self) -> None:
        # TODO: implement test
        # create_key_ring()
        pass

    def test_create_crypto_key(self) -> None:
        # TODO: implement test
        # create_crypto_key()
        pass

    def test_encrypt(self) -> None:
        # TODO: implement test
        # encrypt()
        pass

    def test_decrypt(self) -> None:
        # TODO: implement test
        # decrypt()
        pass

    def test_add_member_to_crypto_key_iam_policy(self) -> None:
        # TODO: implement test
        # add_member_to_crypto_key_iam_policy()
        pass

    def test_get_key_ring_iam_policy(self) -> None:
        # TODO: implement test
        #
        # service_account_email = 'serviceAccount:test-1@fd-secrets-manager-dev-2.iam.gserviceaccount.com'  # noqa: E501
        # iam_role = 'roles/cloudkms.cryptoKeyEncrypterDecrypter'
        #
        # self.assertListEqual(
        #     get_key_ring_iam_policy(kms_api_client, key_ring_grn),
        #     []
        # )
        #
        # # Add member to key ring IAM policy manually, and check:
        # self.assertListEqual(
        #     get_key_ring_iam_policy(kms_api_client, key_ring_grn),
        #     [{
        #         'role': 'roles/cloudkms.cryptoKeyEncrypterDecrypter',
        #         'members': [
        #             'serviceAccount:test-1@fd-secrets-manager-dev-2.iam.gserviceaccount.com',
        #         ]
        #     }]
        # )
        pass
