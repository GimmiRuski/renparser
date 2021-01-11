import time

import click
from lark.indenter import Indenter
from lark.lark import Lark
from rich.console import Console

CONSOLE = Console()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class RenpyIndenter(Indenter):
    NL_type = "_NEWLINE"
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 8


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-p", "--profile", is_flag=True)
@click.argument("script", type=click.File())
def main(script, profile):
    script_content = script.read()
    parser = Lark.open(
        "renpy.lark", parser="lalr", postlex=RenpyIndenter(), rel_to=__file__
    )
    if profile:
        start_time = time.time()
    tree = parser.parse(script_content).pretty()
    if profile:
        end_time = time.time()
    CONSOLE.print(tree)
    if profile:
        elapsed_seconds = end_time - start_time
        CONSOLE.print(f"Took {elapsed_seconds} seconds to parse {script.name}")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
