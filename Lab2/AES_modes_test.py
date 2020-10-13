import unittest

from AES_modes import AESmodes


class TestAESModes(unittest.TestCase):
    def test_ecb_encrypt_decrypt(self):
        def runECB(msg, key):
            aes = AESmodes(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
            ciphertext = aes.encrypt(msg, key, "ecb")

            aes = AESmodes(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
            decrypted = aes.decrypt(ciphertext, key, "ecb")
            assert msg == decrypted

        runECB("test_string".encode("utf-8"),
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        runECB("much_much_much_much_much_longer_test_string".encode("utf-8"),
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')
