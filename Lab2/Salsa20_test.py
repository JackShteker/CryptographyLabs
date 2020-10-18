import unittest

from Salsa20 import Salsa


class TestSalsaFuncs(unittest.TestCase):
    def test_encrypt_decrypt(self):
        def runSalsa(msg, key):
            salsa = Salsa()
            nonce = b"\x00\x01\x02\x03\x04\x05\x06\x07"
            ciphertext = salsa.encrypt(msg, key, nonce)

            decrypted = salsa.decrypt(ciphertext, key, nonce)
            assert msg == decrypted

        runSalsa("test_string".encode("utf-8"),
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        runSalsa("much_much_much_much_much_longer_test_string".encode("utf-8"),
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')
