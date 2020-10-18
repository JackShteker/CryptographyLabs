import unittest

from AES_modes import AESmodes


class TestAESModes(unittest.TestCase):
    def test_all(self):
        def test_mode(mode):
            def runMode(msg, key, mode):
                aes = AESmodes(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
                ciphertext = aes.encrypt(msg, key, mode)

                aes = AESmodes(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
                decrypted = aes.decrypt(ciphertext, key, mode)
                assert msg == decrypted, msg.hex() + "\n" + decrypted.hex()

            runMode("test_string".encode("utf-8"),
                   b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F',
                    mode)

            runMode("much_much_much_much_much_longer_test_string".encode("utf-8"),
                   b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F',
                    mode)

        test_mode("cbc")
        test_mode("ecb")
        test_mode("ofb")
        test_mode("ctr")
        test_mode("cfb")
