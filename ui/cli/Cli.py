from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator

from core.filters import ChoicePartitionsFilter
from core.interfaces import IUserInterface
from core.models import PayloadModel
from core.models.super import MetadataPartitionModel
from core.utils import Utils
from core.validators import SupersImgCompareCsvValidator

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class Cli(IUserInterface):

    def launch_confirmation(self, message: str, payload: PayloadModel, forced: bool = False) -> bool:
        if payload.input_file is None or forced:
            return inquirer.confirm(message=message, default=True).execute()
        else:
            return True

    def get_super_map_path(self, input_files: list[Path], default_path: Path = None) -> Path:
        return inquirer.filepath(
            message="Enter super_map.csv file path",
            validate=SupersImgCompareCsvValidator(list_files=input_files, message="Input file is not a valid"),
            only_files=True,
            mandatory=True,
            filter=lambda result: Path(result).resolve()
        ).execute()

    def choice_build_configuration(self, input_files: list[Path], default_path: Path = None) -> list[Path]:
        csv_records = Utils.parse_csv_file(self.get_super_map_path(input_files, default_path))

        return inquirer.select(
            message="Select build:",
            choices=[
                Choice(
                    value=[item for item in input_files if item.name in record.images],
                    name=f"{index}. [0x{record.id:02X}] {record.name}",
                    enabled=False
                )for index, record in enumerate(csv_records)],
            multiselect=False,
            vi_mode=True,
            transformer=lambda result: f"{result} selected",
        ).execute()

    def choice_extraction_partitions(self, partitions: list[MetadataPartitionModel]) -> list[MetadataPartitionModel]:
        choices = [Choice(value=partitions, name="All", enabled=True)]
        choices.extend([
            Choice(
                value=item,
                name=item.name[:-2] if item.name.endswith(("_a", "_b")) else item.name,
                enabled=False
            ) for item in partitions if item.num_extents != 0])

        return inquirer.checkbox(
            message="Select extract partitions:",
            choices=choices,
            height=len(choices),
            validate=lambda result: len(result) >= 1,
            mandatory=True,
            filter=ChoicePartitionsFilter(),
            vi_mode=True,
            transformer=lambda result: f"{result} selected",
        ).execute()

    def get_custom_extract_folder(self, output_folder: Path) -> Path:
        return inquirer.filepath(
            message="Enter extract folder",
            default=output_folder.__str__(),
            validate=PathValidator(is_file=False, is_dir=True, message="Input is not a dir"),
            only_directories=True,
            mandatory=True,
            filter=lambda result: Path(result).resolve()
        ).execute()
