import unittest

from RC4 import RC4


class TestRC4Funcs(unittest.TestCase):
    def test_encrypt_decrypt(self):
        def runRC4(msg, key):
            rc4 = RC4(key)
            ciphertext = rc4.encrypt(msg)

            rc4 = RC4(key)
            decrypted = rc4.decrypt(ciphertext)
            assert msg == decrypted

        runRC4("test_string".encode("utf-8"),
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        runRC4("much_much_much_much_much_longer_test_string".encode("utf-8"),
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')
