from unittest import TestCase

from fd_gcp.gcp_kms_mock import (
    create_crypto_key, decrypt, encrypt, _generate_fernet_key,
    KMS_ENCRYPTION_PLAIN_DATA_MAX_SIZE,
)


class ApiOperationsFunctionsTestCase(TestCase):

    def test_create_crypto_key(self) -> None:
        key_ring_grn_1 = (
            'projects/fake-project/locations/global/'
            'keyRings/5f99cfca-45f1-4c54-b0c8-d04e06b65ce2')
        key_ring_grn_2 = 'projects/blah/locations/global/keyRings/abc'

        self.assertEqual(
            create_crypto_key(object(), key_ring_grn_1, '75eff8fbfd7e4733804373f61a844be2'),
            'projects/fake-project/locations/global/'
            'keyRings/5f99cfca-45f1-4c54-b0c8-d04e06b65ce2/'
            'cryptoKeys/75eff8fbfd7e4733804373f61a844be2'
        )
        self.assertEqual(
            create_crypto_key(object(), key_ring_grn_2, 'xyz'),
            'projects/blah/locations/global/'
            'keyRings/abc/'
            'cryptoKeys/xyz'
        )

        self.assertRegex(
            create_crypto_key(object(), key_ring_grn_1),
            r'^projects/fake-project/locations/global/'
            r'keyRings/5f99cfca-45f1-4c54-b0c8-d04e06b65ce2/'
            r'cryptoKeys/[a-z0-9]{32}$'
        )
        self.assertRegex(
            create_crypto_key(object(), key_ring_grn_2),
            r'^projects/blah/locations/global/'
            r'keyRings/abc/'
            r'cryptoKeys/[a-z0-9]{32}$'
        )

    def test_encrypt_decrypt(self) -> None:
        crypto_key_grn_1 = (
            'projects/fd-secrets-manager-dev-2/locations/global/'
            'keyRings/dd06b298-e408-43dd-a553-69ad046a9938/'
            'cryptoKeys/75eff8fbfd7e4733804373f61a844be2')
        crypto_key_grn_2 = 'projects/blah/locations/global/keyRings/abc/cryptoKeys/xyz'
        plain_data_1 = b'J\xc3\xbcrgen loves \xce\xa9! \xe2\x9c\x94 \n\r\t 123'
        plain_data_2 = b'SsO8cmdlbiBsb3ZlcyDOqSEg4pyUIAoNCSAxMjM='

        encrypted_data_11 = encrypt(object(), crypto_key_grn_1, plain_data_1)
        decrypted_data_11 = decrypt(object(), crypto_key_grn_1, encrypted_data_11)
        self.assertTrue(isinstance(encrypted_data_11, bytes))
        self.assertNotEqual(encrypted_data_11, plain_data_1)
        self.assertEqual(decrypted_data_11, plain_data_1)

        encrypted_data_12 = encrypt(object(), crypto_key_grn_1, plain_data_2)
        decrypted_data_12 = decrypt(object(), crypto_key_grn_1, encrypted_data_12)
        self.assertTrue(isinstance(encrypted_data_12, bytes))
        self.assertNotEqual(encrypted_data_12, plain_data_2)
        self.assertEqual(decrypted_data_12, plain_data_2)

        encrypted_data_21 = encrypt(object(), crypto_key_grn_2, plain_data_1)
        decrypted_data_21 = decrypt(object(), crypto_key_grn_2, encrypted_data_21)
        self.assertTrue(isinstance(encrypted_data_21, bytes))
        self.assertNotEqual(encrypted_data_21, plain_data_1)
        self.assertEqual(decrypted_data_21, plain_data_1)

        encrypted_data_22 = encrypt(object(), crypto_key_grn_2, plain_data_2)
        decrypted_data_22 = decrypt(object(), crypto_key_grn_2, encrypted_data_22)
        self.assertTrue(isinstance(encrypted_data_22, bytes))
        self.assertNotEqual(encrypted_data_22, plain_data_2)
        self.assertEqual(decrypted_data_22, plain_data_2)

        # The output of all 4 encryption operations is different.
        encrypted_data_set = {
            encrypted_data_11, encrypted_data_12, encrypted_data_21, encrypted_data_22,
        }
        self.assertTrue(len(encrypted_data_set) == 4)

    def test_encrypt_fail_input_size(self) -> None:
        plain_data = b'1' * (KMS_ENCRYPTION_PLAIN_DATA_MAX_SIZE + 1)
        with self.assertRaises(ValueError) as cm:
            encrypt(object(), '', plain_data)
        self.assertEqual(cm.exception.args, ("Size of 'plain_data' exceeds max size.", ))

    def test_encrypt_fail_type(self) -> None:
        with self.assertRaises(TypeError) as cm:
            encrypt(object(), '', 'not bytes')  # type: ignore
        self.assertEqual(cm.exception.args, ("Type of 'plain_data' is not bytes.", ))

    def test__generate_fernet_key_fail_length(self) -> None:
        value = b'1' * 33
        with self.assertRaises(ValueError) as cm:
            _generate_fernet_key(value)
        self.assertEqual(cm.exception.args, ())

    def test__generate_fernet_key_fail_type(self) -> None:
        with self.assertRaises(TypeError) as cm:
            _generate_fernet_key('not bytes')  # type: ignore
        self.assertEqual(cm.exception.args, ())
