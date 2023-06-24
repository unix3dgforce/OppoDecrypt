from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from core.validators import SupersImgCompareCsvValidator

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class Cli:
    @staticmethod
    def get_super_map_path(input_files: list[Path]) -> Path:
        return inquirer.filepath(
            message="Enter super_map.csv file path",
            validate=SupersImgCompareCsvValidator(list_files=input_files, message="Input file is not a valid"),
            only_files=True,
            filter=lambda result: Path(result).resolve()
        ).execute()

    @staticmethod
    def get_choice_build_configuration(choices: list[Choice]) -> list[Path]:
        return inquirer.select(
            message="Select build:",
            choices=choices,
            multiselect=False,
            transformer=lambda result: f"{result} selected",
        ).execute()
