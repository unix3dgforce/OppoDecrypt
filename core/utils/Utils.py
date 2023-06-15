import hashlib
import io
from pathlib import Path
from typing import BinaryIO

from core.models.enums.HashAlgorithmEnum import HashAlgorithmEnum
from exceptions import UtilsNoSupportedHashAlgorithmError, UtilsFileNotFoundError

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class Utils:
    @staticmethod
    def de_obfuscate_qualcomm(data, mask):
        def rol(x, n, bits=32):
            n = bits - n
            m = (2 ** n) - 1
            mask_bits = x & m
            return (x >> n) | (mask_bits << (bits - n))

        ret = bytearray()
        for i in range(0, len(data)):
            v = rol((data[i] ^ mask[i]), 4, 8)
            ret.append(v)
        return ret

    @staticmethod
    def mtk_header_shuffle(data, header_key=b"geyixue", header_size=0x6C) -> bytearray:
        key = bytearray(header_key)
        data = bytearray(data)
        for index in range(0, header_size):
            k = key[(index % len(key))]
            h = ((((data[index]) & 0xF0) >> 4) | (16 * ((data[index]) & 0xF)))
            data[index] = k ^ h

        return data

    @staticmethod
    def read_chunk(fd: BinaryIO, length: int, buffer_size=4096):
        if length < buffer_size:
            buffer_size = length

        while length > 0:
            chunk = fd.read(buffer_size)
            yield chunk

            length -= buffer_size

            if buffer_size > length:
                buffer_size = length

    @staticmethod
    def validate_checksum(checksum: str, dst: Path, algorithm: HashAlgorithmEnum) -> bool:
        match algorithm:
            case HashAlgorithmEnum.Md5:
                alg = hashlib.md5()
            case HashAlgorithmEnum.Sha256:
                alg = hashlib.sha256()
            case _:
                raise UtilsNoSupportedHashAlgorithmError()

        if not dst or not dst.exists():
            raise UtilsFileNotFoundError(dst)

        with open(dst, 'rb') as fd:
            for read_bytes in [0x40000, dst.stat().st_size]:
                fd.seek(io.SEEK_SET)
                for chunk in Utils.read_chunk(fd, read_bytes):
                    alg.update(chunk)

                if checksum == alg.hexdigest():
                    return True

        return False


