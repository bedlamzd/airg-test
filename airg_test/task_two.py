"""
---------------

AirG test task #2
=====================

Create a script to generate a CSV file with random data.

Example output::

    1234, randomstring

Add the ability to pass in command line parameters. Use an argument to pass
in the number of rows to generate.
Add another argument for the filename to use for the CSV file.
"""
import argparse
import csv
import itertools
import random
from os import PathLike
from typing import Iterator


def random_string(length: int = 10) -> str:
    """
    Generate random string. Length of the result is ``(length // 2) * 2``

    >>> random.seed(42)
    >>> random_string()
    '9d79b1a31c'
    >>> random_string(3)
    '06'
    >>> random_string(4)
    'd6bd'
    >>> random_string(15)
    '575268463bb13e'
    """
    return random.randbytes(length // 2).hex()


def make_random_data(n_columns: int = 2) -> list:
    """
    Generate a list of random data where first element is a
    random positive integer less than a 1000 and the rest are
    random ascii letter strings of length 10

    >>> random.seed(42)
    >>> make_random_data()
    [654, '7f31801c06']
    >>> make_random_data(0)
    []
    >>> make_random_data(-1)
    Traceback (most recent call last):
        ...
    ValueError: Number of columns should be positive, got -1
    >>> make_random_data(5)
    [281, '903bb13e39', 'e9c1b823bc', 'a71f3d1aad', 'b3669cbde4']
    """
    if n_columns < 0:
        raise ValueError(f"Number of columns should be positive, got {n_columns}")
    data: Iterator[int | str] = itertools.chain(
        (random.randint(0, 1000),), iter(random_string, "")
    )
    return list(itertools.islice(data, n_columns))


def data_generator(rows: int = 100, columns: int = 10) -> Iterator[list]:
    """
    Generator that yields lists of length ``columns``. Number of lists
    yielded is ``rows``.

    >>> random.seed(42)
    >>> data = data_generator()
    >>> next(data)
    [654, '7f31801c06', 'fb40d6bd46', '903bb13e39', 'e9c1b823bc', 'a71f3d1aad', 'b3669cbde4', '34249d8b16', '69842a976c', 'f3e8220807']
    >>> next(data)
    [95, '8ba8f8373b', 'd1f65e819a', 'b30fcb068f', '2906e732b7', '89d35ea6b3', 'f648818b6b', 'e0cb6e3872', 'ac1dda9647', '8bd536cfde']
    >>> next(data)
    [6, '0b3341c2ce', 'c46edf28b2', '1175306c57', '8993224727', '7bcd1e37f5', 'ee5974c356', 'ed732a1a17', '7dea426118', '8e12e65bd8']

    >>> data = data_generator(rows=1)
    >>> next(data)
    [352, '03ca8d9a43', '7ff59fce0b', 'd0b3cfba75', '853e46891f', '4c1d1ef9ec', '13a1e76014', 'f188528d4b', '32dd53d4a0', '7a4f579ee2']
    >>> next(data)
    Traceback (most recent call last):
        ...
    StopIteration

    >>> data = data_generator(columns=4)
    >>> next(data)
    [882, 'f01c945c93', '2cd33931b4', 'd25dce110b']
    >>> next(data)
    [677, '8e8a573ac5', '4d54154afc', '313f6d14da']
    """
    for _ in range(rows):
        yield make_random_data(columns)


def random_csv(
    file: str | bytes | PathLike[str] | PathLike[bytes],
    rows: int = 100,
    columns: int = 10,
    dialect: str | type[csv.Dialect] | csv.Dialect = "excel",
) -> None:
    """
    Save a random data to a ``file``. ``file`` can be anything that
    builtin ``open`` accepts.

    >>> random.seed(42)
    >>> import tempfile
    >>>
    >>> with tempfile.NamedTemporaryFile() as tfile:
    ...     random_csv(tfile.name)
    ...     with open(tfile.name) as fin:
    ...         reader = csv.reader(fin)
    ...         for row in itertools.islice(reader, 3):
    ...             print(row)
    ['654', '7f31801c06', 'fb40d6bd46', '903bb13e39', 'e9c1b823bc', 'a71f3d1aad', 'b3669cbde4', '34249d8b16', '69842a976c', 'f3e8220807']
    ['95', '8ba8f8373b', 'd1f65e819a', 'b30fcb068f', '2906e732b7', '89d35ea6b3', 'f648818b6b', 'e0cb6e3872', 'ac1dda9647', '8bd536cfde']
    ['6', '0b3341c2ce', 'c46edf28b2', '1175306c57', '8993224727', '7bcd1e37f5', 'ee5974c356', 'ed732a1a17', '7dea426118', '8e12e65bd8']

    >>> class my_dialect(csv.excel):
    ...     delimiter = '|'
    >>>
    >>> with tempfile.NamedTemporaryFile() as tfile:
    ...     random_csv(tfile.name, dialect=my_dialect)
    ...     with open(tfile.name) as fin:
    ...         for row in itertools.islice(fin, 3):
    ...             print(row.strip())
    823|330aac8e5d|cc161e17ca|a2d6026503|b48eb34389|e882a31f74|3da15b5eac|7b39bfbfac|9f021d4395|05e38a61d2
    653|3ff8b6f05f|f791bc1bac|9ec0db3b78|ee0368069e|eb365de2f1|e464b88f53|17364eea9c|4c85ab38a5|e5fd2e10a2
    843|a03cda76e8|1ecb79b34d|788e34a668|6979de1d23|34d99b0bf2|ebbb86094d|a618f5fe7e|6712ba1d18|ccda1b3ce3

    >>> with tempfile.NamedTemporaryFile() as tfile:
    ...     random_csv(tfile.name, rows=2, columns=4)
    ...     with open(tfile.name) as fin:
    ...         reader = csv.reader(fin)
    ...         data = list(reader)
    >>> len(data)
    2
    >>> len(data[0])
    4

    """
    with open(file, "w") as f:
        writer = csv.writer(f, dialect)
        writer.writerows(data_generator(rows, columns))


class Arguments:
    rows: int
    columns: int
    filename: str


def parse_arguments(args: list[str] | None = None) -> Arguments:
    p = argparse.ArgumentParser(description="Create a csv file with random data.")
    p.add_argument(
        "-r",
        "--rows",
        type=int,
        default=10,
        help="Number of rows in resulting file (default: %(default)s)",
    )
    p.add_argument(
        "-c",
        "--columns",
        type=int,
        default=10,
        help="Number of columns in resulting file (default: %(default)s)",
    )
    p.add_argument("filename", type=str, help="Where to save the data", metavar="FILE")
    return p.parse_args(args, namespace=Arguments())


def main() -> None:
    args = parse_arguments()
    random_csv(args.filename, rows=args.rows, columns=args.columns)


if __name__ == "__main__":
    main()
