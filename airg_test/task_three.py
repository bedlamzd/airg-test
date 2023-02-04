"""
---------------

AirG test task #3
=================

Write a function to normalize CSV files by converting a pipe-delimited file
into a comma-delimited file.

Your original file will look like this::

    Planet|Manufacturer|Model|Type|Passengers
    Yavin|Ubrikkian" Industries|Sail Barge|sailbarge|500
    Bespin|Bespin Motors|Storm IV, Twin-Pod|repulsorcraft|0
    Kuat|Kuat Drive Yards|AT-ST|walker|0

When you run your script, the output should look like this::

    Planet,Manufacturer,Model,Type,Passengers
    Yavin,"Ubrikkian"" Industries",Sail Barge,sailbarge,500
    Bespin,Bespin Motors,"Storm IV, Twin-Pod",repulsorcraft,0
    Kuat,Kuat Drive Yards,AT-ST,walker,0

It's valid for a comma to be in your input data. You'll need to surround
strings with commas in them with double quotes when writing your output file.

It's also valid for double quote characters to be in your input - you will
need to double up quotes.

BONUS 1:
    Add in the ability to accept command line parameters for:
        - the input delimiter to use ('|' should be the default)
        - the quote character to use (" by default)

BONUS 2:
    Try to automatically detect the delimiter and quote character if they are
    not supplied on the command line.

    If either the delimiter or the quote character are provided, assume the
    other one is the default. But if both are missing, you should try to
    automatically detect them.

    NOTE: This may not work for all files.
"""

import argparse
import csv
from os import PathLike
from typing import Final, Literal

DEFAULT_DELIMITER: Final[Literal["|"]] = "|"
DEFAULT_QUOTECHAR: Final[Literal['"']] = '"'


class Arguments:
    input: str
    output: str
    delimiter: str | None
    quotechar: str | None


def parse_args(args: list[str] | None = None) -> Arguments:
    p = argparse.ArgumentParser(description="Translate csv")
    p.add_argument(
        "-d",
        "--delimiter",
        type=str,
        help=f"Delimiter character in IN_FILE (default: {DEFAULT_DELIMITER})",
    )
    p.add_argument(
        "-q",
        "--quotechar",
        type=str,
        help=f"Quote character in IN_FILE (default: {DEFAULT_QUOTECHAR})",
    )
    p.add_argument("input", type=str, metavar="IN_FILE")
    p.add_argument("output", type=str, metavar="OUT_FILE")
    return p.parse_args(args, Arguments())


def get_dialect(
    file: str | bytes | PathLike[str] | PathLike[bytes],
    delimiter: str | None = None,
    quotechar: str | None = None,
) -> type[csv.Dialect]:
    """
    Construct a ``csv.Dialect`` class from input.

    If both ``delimiter`` and ``quotechar`` are ``None`` then try
    to infer dialect using ``csv.Sniffer`` from first 1024 characters.

    Otherwise use given ``delimiter`` and ``qoutechar``, replacing ``None``
    with default values ``DEFAULT_DELIMITER`` and ``DEFAULT_QUOTECHAR``

    NOTE: returned dialect enables doublequotting (see `csv docs`_)

    .. _csv docs: https://docs.python.org/3.10/library/csv.html#csv.Dialect.doublequote
    """
    should_sniff = delimiter is None and quotechar is None
    if should_sniff:
        sniffer = csv.Sniffer()
        with open(file) as f:
            dialect = sniffer.sniff(f.read(1024))
    else:
        delimiter_ = delimiter or DEFAULT_DELIMITER
        quotechar_ = quotechar or DEFAULT_QUOTECHAR

        class _dialect(csv.excel):
            delimiter = delimiter_
            quotechar = quotechar_

        dialect = _dialect

    dialect.doublequote = True
    return dialect


def translate(
    in_file: str | bytes | PathLike[str] | PathLike[bytes],
    out_file: str | bytes | PathLike[str] | PathLike[bytes],
    in_dialect: type[csv.Dialect],
) -> None:
    """
    Translate ``in_file`` csv using commas (``,``) as delimiters and
    double quotes (``"``) as quote characters and save to ``out_file``.

    ``in_file`` and ``out_file`` accept same objects as builtin ``open``.
    """
    with (
        open(in_file) as fin,
        open(out_file, "w") as fout,
    ):
        reader = csv.reader(fin, dialect=in_dialect)
        writer = csv.writer(fout)
        writer.writerows(reader)


def main() -> None:
    arguments = parse_args()
    dialect = get_dialect(arguments.input, arguments.delimiter, arguments.quotechar)
    translate(arguments.input, arguments.output, dialect)


if __name__ == "__main__":
    main()
