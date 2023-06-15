import io
import shutil
import struct
from pathlib import Path
from typing import BinaryIO

from core.interfaces import IExtractor, ILogService
from core.models import OfpMtkConfiguration, CryptoCredential
from core.utils import Crypto, Utils
from exceptions import MtkExtractorUnsupportedCryptoSettingsError

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'

HEADER_SIZE = 0x6C
ENTRY_SIZE = 0x60


class Header:
    def __init__(self, buffer):
        fmt = "46sQ4s7s5sH32sH"
        (
            self.name,
            self._unknown,
            self._reserved,
            self.cpu,
            self.flash_type,
            self.entries_count,
            self.info,
            self.crc
        ) = struct.unpack(fmt, buffer[0:struct.calcsize(fmt)])

        self.name = self._clean_string_value(self.name)
        self.cpu = self._clean_string_value(self.cpu)
        self.info = self._clean_string_value(self.info)
        self.flash_type = self._clean_string_value(self.flash_type)

    @staticmethod
    def _clean_string_value(data: bytes) -> str:
        return data.replace(b"\x00", b"").decode('utf-8')


class Entry:
    def __init__(self, buffer):
        fmt = "32sQQQ32sQ"
        (
            self.name,
            self.start_position,
            self.size,
            self.crypto_size,
            self.filename,
            self.crc
        ) = struct.unpack(fmt, buffer[0:struct.calcsize(fmt)])

        self.name = self._clean_string_value(self.name)
        self.filename = self._clean_string_value(self.filename)

    @staticmethod
    def _clean_string_value(data: bytes) -> str:
        return data.replace(b"\x00", b"").decode('utf-8')


class MtkExtractor(IExtractor):
    def __init__(self, configuration: dict[str, any], logger: ILogService):
        self._configuration = OfpMtkConfiguration(**configuration)
        self._logger = logger
        self._crypto_config: CryptoCredential | None = None

    @staticmethod
    def _get_entries(fd: BinaryIO, header: Header, file_size: int):
        result = []
        fd.seek(file_size - HEADER_SIZE - header.entries_count * ENTRY_SIZE, io.SEEK_SET)

        data = Utils.mtk_header_shuffle(fd.read(header.entries_count * ENTRY_SIZE), header_size=header.entries_count * ENTRY_SIZE)

        for entries in range(0, header.entries_count):
            entry = Entry(data[entries * ENTRY_SIZE: (entries * ENTRY_SIZE) + ENTRY_SIZE])
            result.append(entry)

        return result

    def _find_crypto_config(self, fd: BinaryIO) -> None:
        fd.seek(io.SEEK_SET)
        crypto_data = fd.read(HEADER_SIZE)
        for crypto_credential in self._configuration.keys:
            data = Crypto.decrypt_aes_cfb(crypto_credential, crypto_data)

            if data[:3] == b"MMM":
                self._crypto_config = crypto_credential
                return

        raise MtkExtractorUnsupportedCryptoSettingsError

    def _extract(self, fd: BinaryIO, output_dir: Path, file_size):
        self._find_crypto_config(fd)
        fd.seek(-HEADER_SIZE, io.SEEK_END)
        header = Header(Utils.mtk_header_shuffle(fd.read(HEADER_SIZE)))

        for entry in self._get_entries(fd, header, file_size):
            self._logger.information(f"Extracting {entry.filename}")
            self._write_to_file(fd, entry, output_dir)

    def _write_to_file(self, fd: BinaryIO, entry: Entry, output_dir: Path):
        fd.seek(entry.start_position, io.SEEK_SET)
        with open(output_dir / entry.filename, "wb") as out:
            if entry.crypto_size > 0:
                crypto_data = fd.read(entry.crypto_size)
                if entry.crypto_size % 16 != 0:
                    crypto_data += b"\x00" * (16 - (entry.crypto_size % 16))

                data = Crypto.decrypt_aes_cfb(self._crypto_config, crypto_data)
                out.write(data[:entry.crypto_size])
                entry.size -= entry.crypto_size

            for chunk in Utils.read_chunk(fd, entry.size):
                out.write(chunk)

    def extract(self, input_file: Path, output_dir: Path) -> None:
        self._logger.information("Run Mtk extractors")

        if output_dir.exists():
            shutil.rmtree(output_dir)

        output_dir.mkdir(parents=True)
        file_size = input_file.stat().st_size

        with open(input_file, 'rb') as fd:
            self._extract(fd, output_dir, file_size)

        self._logger.information(f'Extract successfully')
