"""
---------------------

AirG test task #1
======================

Write a script to connect to the following API "https://swapi.dev/api/vehicles/".
Retrieve the JSON data, and list the first 5 unique manufacturers.
"""
from typing import Final, Generic, Iterable, Iterator, TypeVar

import requests
from pydantic import BaseModel, Extra, HttpUrl, validator
from pydantic.generics import GenericModel


class Vehicle(BaseModel):
    manufacturer: list[str]

    @validator("manufacturer", pre=True)
    def split_manufacturer(cls, manufacturer: str | Iterable[str]) -> list[str]:
        if isinstance(manufacturer, str):
            return manufacturer.split(",")
        return list(manufacturer)

    class Config:
        extra = Extra.ignore


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    count: int
    next: HttpUrl | None
    previous: HttpUrl | None
    results: list[T]


class Swapi:
    ROOT: Final[str] = "https://swapi.dev/api"
    VEHICLES: Final[str] = f"{ROOT}/vehicles"

    @classmethod
    def gen_vehicles(cls) -> Iterator[Vehicle]:
        endpoint: str | None = cls.VEHICLES
        while endpoint is not None:
            res = requests.get(endpoint)
            assert res.ok, f"Something went wrong, {res!r}"
            page = Page[Vehicle](**res.json())
            yield from page.results
            endpoint = page.next


def unique_manufacturers(n: int = 5) -> None:
    manufacturers = set()
    for vehicle in Swapi.gen_vehicles():
        if len(manufacturers) >= n:
            break
        manufacturers.update(vehicle.manufacturer)
    print(manufacturers)


if __name__ == "__main__":
    unique_manufacturers()
