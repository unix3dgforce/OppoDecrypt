from Cryptodome.Cipher import AES

from core.models.configuration.CryptoCredential import CryptoCredential

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class Crypto:
    @staticmethod
    def decrypt_aes_cfb(crypto_credential: CryptoCredential, data: bytes):
        return AES.new(crypto_credential.key, AES.MODE_CFB, iv=crypto_credential.iv, segment_size=128).decrypt(data)
