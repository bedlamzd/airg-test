import csv
import tempfile
from typing import Iterator, NamedTuple, TypeAlias
from unittest.mock import patch

import pytest

from airg_test.task_three import (
    DEFAULT_DELIMITER,
    DEFAULT_QUOTECHAR,
    get_dialect,
    translate,
)

Delimiter: TypeAlias = str
Quotechar: TypeAlias = str


class CsvFile(NamedTuple):
    content: str
    delimiter: Delimiter
    quotechar: Quotechar


piped = CsvFile(
    "one|two|three|four|5\r\none|two|three|four|5\r\none|two|three|four|5\r\n",
    delimiter="|",
    quotechar='"',
)

commas = CsvFile(
    "one,two,three,four,5\r\none,two,three,four,5\r\none,two,three,four,5\r\n",
    delimiter=",",
    quotechar='"',
)

Filename: TypeAlias = str

CsvData: TypeAlias = tuple[Filename, Delimiter, Quotechar]


@pytest.fixture
def csv_data(request) -> Iterator[CsvData]:
    with tempfile.NamedTemporaryFile() as f:
        csv_: CsvFile = request.param
        f.write(csv_.content.encode("utf-8"))
        f.flush()
        yield f.name, csv_.delimiter, csv_.quotechar


@pytest.mark.parametrize(
    "csv_data", (piped, commas), ids=("pipes", "commas"), indirect=True
)
def test_dialect_inference(csv_data: CsvData):
    filename, expected_delimiter, expected_quotechar = csv_data
    sniffer = csv.Sniffer()
    with (
        patch("airg_test.task_three.csv.Sniffer", return_value=sniffer),
        patch.object(sniffer, "sniff", wraps=sniffer.sniff) as sniff_method_mock,
    ):
        dialect = get_dialect(filename)
    sniff_method_mock.assert_called_once()
    assert dialect.delimiter == expected_delimiter
    assert dialect.quotechar == expected_quotechar


delim_quote_pairs = (
    (None, '"'),
    (",", None),
    (",", '"'),
)


@pytest.mark.parametrize(
    "csv_data", (piped, commas), ids=("pipes", "commas"), indirect=True
)
@pytest.mark.parametrize(["delimiter", "quotechar"], delim_quote_pairs)
def test_no_dialect_inference_when_args_given(
    csv_data: CsvData,
    delimiter: str | None,
    quotechar: str | None,
):
    filename, _, _ = csv_data
    sniffer = csv.Sniffer()
    with (
        patch("airg_test.task_three.csv.Sniffer", return_value=sniffer),
        patch.object(sniffer, "sniff", wraps=sniffer.sniff) as sniff_method_mock,
    ):
        dialect = get_dialect(filename, delimiter, quotechar)
    sniff_method_mock.assert_not_called()
    assert dialect.delimiter == (delimiter or DEFAULT_DELIMITER)
    assert dialect.quotechar == (quotechar or DEFAULT_QUOTECHAR)


piped_example = CsvFile(
    (
        "Planet|Manufacturer|Model|Type|Passengers\r\n"
        'Yavin|Ubrikkian" Industries|Sail Barge|sailbarge|500\r\n'
        "Bespin|Bespin Motors|Storm IV, Twin-Pod|repulsorcraft|0\r\n"
        "Kuat|Kuat Drive Yards|AT-ST|walker|0\r\n"
    ),
    delimiter="|",
    quotechar='"',
)

expected_example = CsvFile(
    (
        "Planet,Manufacturer,Model,Type,Passengers\r\n"
        'Yavin,"Ubrikkian"" Industries",Sail Barge,sailbarge,500\r\n'
        'Bespin,Bespin Motors,"Storm IV, Twin-Pod",repulsorcraft,0\r\n'
        "Kuat,Kuat Drive Yards,AT-ST,walker,0\r\n"
    ),
    delimiter=",",
    quotechar='"',
)


@pytest.mark.parametrize(
    ["csv_data", "expected_output"],
    ((piped, commas), (piped_example, expected_example)),
    indirect=("csv_data",),
)
def test_translate(csv_data: CsvData, expected_output: CsvFile):
    in_file, _, _ = csv_data
    with tempfile.NamedTemporaryFile() as out_file:
        dialect = get_dialect(in_file)
        translate(in_file, out_file.name, dialect)
        assert out_file.read().decode("utf-8") == expected_output.content
