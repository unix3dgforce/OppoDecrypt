import csv
from pathlib import Path
from exceptions import ValidationError

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class SupersImgCompareCsvGuiValidator:
    _suffix = ".csv"
    _search_pattern = "super_"

    def __init__(
            self,
            list_files: list[Path],
            message: str = "Input file is not a valid"
    ) -> None:
        self._list_files = list_files
        self._message = message
        self._search_fields = []

    def validate(self, path: str | Path) -> None:
        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            raise ValidationError(message=self._message)

        if not path.is_file():
            raise ValidationError(message=self._message)

        if path.suffix.lower() != self._suffix:
            raise ValidationError(message=self._message)

        check_names = []
        with open(path, newline='') as fd:
            csv_data = csv.DictReader(fd)

            self._search_fields.extend([item for item in csv_data.fieldnames if item.startswith(self._search_pattern)])

            for item in csv_data:
                check_names.extend([item.get(_, None) for _ in self._search_fields])

            for item in [item.name for item in self._list_files]:
                if item == "super.img":
                    continue

                if item not in check_names:
                    raise ValidationError(message="The selected file does not match")


