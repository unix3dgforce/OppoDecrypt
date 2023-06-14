import argparse

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


def CheckExtensions(choices):
    class Action(argparse.Action):
        def __call__(self, parser, namespace, fname, option_string=None):
            if fname.suffix[1:] not in choices:
                parser.error(f"file doesn't end with one of [{choices}]")
            else:
                setattr(namespace, self.dest, fname)
    return Action
