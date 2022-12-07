from __future__ import annotations

settings_cases = [
    (
        (
            ("--test",),
            dict(
                action=None,
                nargs=None,
                const=None,
                default=None,
                type=None,
                choices=None,
                required=None,
                help=None,
                metavar=None,
                dest=None,
                cmdline=True,
                file=True,
                group="tst",
                exclusive=False,
            ),
        ),
        {
            "action": None,
            "choices": None,
            "cmdline": True,
            "const": None,
            "default": None,
            "dest": "test",
            "exclusive": False,
            "file": True,
            "group": "tst",
            "help": None,
            "internal_name": "tst_test",
            "metavar": "TEST",
            "nargs": None,
            "required": None,
            "type": None,
            "argparse_args": ("--test",),
            "argparse_kwargs": {
                "action": None,
                "choices": None,
                "const": None,
                "default": None,
                "dest": "tst_test",
                "help": None,
                "metavar": "TEST",
                "nargs": None,
                "required": None,
                "type": None,
            },
        },
    ),
    (
        (
            (
                "-t",
                "--test",
            ),
            dict(
                action=None,
                nargs=None,
                const=None,
                default=None,
                type=None,
                choices=None,
                required=None,
                help=None,
                metavar=None,
                dest=None,
                cmdline=True,
                file=True,
                group="tst",
                exclusive=False,
            ),
        ),
        {
            "action": None,
            "choices": None,
            "cmdline": True,
            "const": None,
            "default": None,
            "dest": "test",
            "exclusive": False,
            "file": True,
            "group": "tst",
            "help": None,
            "internal_name": "tst_test",
            "metavar": "TEST",
            "nargs": None,
            "required": None,
            "type": None,
            "argparse_args": (
                "-t",
                "--test",
            ),
            "argparse_kwargs": {
                "action": None,
                "choices": None,
                "const": None,
                "default": None,
                "dest": "tst_test",
                "help": None,
                "metavar": "TEST",
                "nargs": None,
                "required": None,
                "type": None,
            },
        },
    ),
    (
        (
            ("test",),
            dict(
                action=None,
                nargs=None,
                const=None,
                default=None,
                type=None,
                choices=None,
                required=None,
                help=None,
                metavar=None,
                dest=None,
                cmdline=True,
                file=True,
                group="tst",
                exclusive=False,
            ),
        ),
        {
            "action": None,
            "choices": None,
            "cmdline": True,
            "const": None,
            "default": None,
            "dest": "test",
            "exclusive": False,
            "file": True,
            "group": "tst",
            "help": None,
            "internal_name": "tst_test",
            "metavar": "TEST",
            "nargs": None,
            "required": None,
            "type": None,
            "argparse_args": ("tst_test",),
            "argparse_kwargs": {
                "action": None,
                "choices": None,
                "const": None,
                "default": None,
                "dest": None,
                "help": None,
                "metavar": "TEST",
                "nargs": None,
                "required": None,
                "type": None,
            },
        },
    ),
    (
        (
            ("--test",),
            dict(
                action=None,
                nargs=None,
                const=None,
                default=None,
                type=None,
                choices=None,
                required=None,
                help=None,
                metavar=None,
                dest=None,
                cmdline=True,
                file=True,
                group="",
                exclusive=False,
            ),
        ),
        {
            "action": None,
            "choices": None,
            "cmdline": True,
            "const": None,
            "default": None,
            "dest": "test",
            "exclusive": False,
            "file": True,
            "group": "",
            "help": None,
            "internal_name": "test",
            "metavar": "TEST",
            "nargs": None,
            "required": None,
            "type": None,
            "argparse_args": ("--test",),
            "argparse_kwargs": {
                "action": None,
                "choices": None,
                "const": None,
                "default": None,
                "dest": "test",
                "help": None,
                "metavar": "TEST",
                "nargs": None,
                "required": None,
                "type": None,
            },
        },
    ),
]
