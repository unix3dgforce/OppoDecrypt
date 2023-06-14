import sys
import yaml
from pathlib import Path
import argparse

from core.interfaces import IBaseExtractService
from core.utils import ExitCode, CheckExtensions
from dependency_injector.wiring import inject, Provide
from containers import ApplicationContainer

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'
__version__ = '1.0.0'


def load_yaml_configuration() -> dict:
    def run_func(loader, node):
        value = loader.construct_scalar(node)
        if '.' in value:
            module_name, fun_name = value.rsplit('.', 1)
        else:
            module_name = '__main__'
            fun_name = value

        try:
            __import__(module_name)
        except ImportError as exc:
            raise

        module = sys.modules[module_name]
        fun = getattr(module, fun_name)

        try:
            return fun()
        except TypeError:
            return fun

    yaml.add_constructor('!func', run_func)

    with open(Path(Path().resolve() / 'config.yml'), 'r') as stream:
        return yaml.full_load(stream)


@inject
def main(service: IBaseExtractService = Provide[ApplicationContainer.extract_service], **kwargs) -> None:
    service.extract(**kwargs)


def create_parser() -> argparse.ArgumentParser:
    _parser = argparse.ArgumentParser(
        prog='OppoDecrypt',
        description=f'OppoDecrypt - command-line tool for extracting partition images from .ofp'
    )

    _parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'OppoDecrypt version [{__version__}]'
    )

    _parser.add_argument(
        'INPUT_FILE',
        type=Path,
        action=CheckExtensions({'ofp'}),
        nargs='?',
    )
    _parser.add_argument(
        'OUTPUT_DIR',
        type=Path,
        nargs='?',
    )

    return _parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    if len(sys.argv) >= 2:
        if not namespace.INPUT_FILE.exists():
            parser.print_help()
            sys.exit(ExitCode.CONFIG)

        container = ApplicationContainer()
        container.configuration.from_dict(load_yaml_configuration())
        container.init_resources()
        container.wire(modules=[sys.modules[__name__]])

        main(**{k.lower(): v for k, v in vars(namespace).items()})
    else:
        parser.print_usage()
        sys.exit(ExitCode.USAGE)

