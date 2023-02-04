import json
from pathlib import Path
from typing import Final, Iterator
from unittest.mock import Mock, patch

import requests

from airg_test.task_one import Page, Swapi, Vehicle

RAW_VEHICLES_PAGE_1: Final[dict] = json.loads(
    Path(r"tests/data/vehicles/page1.json").read_text()
)
RAW_VEHICLES_PAGE_2: Final[dict] = json.loads(
    Path(r"tests/data/vehicles/page2.json").read_text()
)

VEHICLES_PAGE_1: Page[Vehicle] = Page[Vehicle](**RAW_VEHICLES_PAGE_1)
VEHICLES_PAGE_2: Page[Vehicle] = Page[Vehicle](**RAW_VEHICLES_PAGE_2)


def vehicle_endpoint_responses() -> Iterator[Mock]:
    for page in (RAW_VEHICLES_PAGE_1, RAW_VEHICLES_PAGE_2):
        yield Mock(ok=True, json=lambda: page)


def test_swapi_gen_vehicles():
    responses = vehicle_endpoint_responses()
    with patch.object(requests, "get", wraps=lambda endpoint: next(responses)):
        all_expected_vehicles = [*VEHICLES_PAGE_1.results, *VEHICLES_PAGE_2.results]
        all_received_vehicles = list(Swapi.gen_vehicles())
        assert len(all_received_vehicles) == len(all_expected_vehicles)
        assert all_received_vehicles == all_expected_vehicles
