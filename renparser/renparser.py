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
@click.argument("script", type=click.File())
def main(script):
    script_content = script.read()
    parser = Lark.open(
        "renpy.lark", parser="lalr", postlex=RenpyIndenter(), rel_to=__file__
    )
    tree = parser.parse(script_content).pretty()
    CONSOLE.print(tree)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
