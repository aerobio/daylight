
import datetime

import astral
import csv


class Town:
    """
    Town location and population
    """

    def __init__(self, name, region, lat, lon, tz, elevation, population):
        """
        Town initialization

        :param name: name
        :param region: country, region, province...
        :param lat: latitude in degrees
        :param lon: longitude in degrees
        :param tz: time zone name
        :param elevation: elevation in metres
        :param population: population
        """
        self._location = astral.Location((name, region, lat, lon, tz, elevation))
        self.population = population
        self._date = datetime.datetime.today()
        self._sun = self._location.sun(local=False)

    @property
    def name(self):
        return self._location.name

    @property
    def region(self):
        return self._location.region

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date
        self._sun = self._location.sun(date, local=False)

    @property
    def sunrise(self):
        return self._sun['sunrise']

    @property
    def sunset(self):
        return self._sun['sunset']


def towns():
    """
    Sequence of Spanish towns
    Data from http://centrodedescargas.cnig.es/CentroDescargas/catalogo.do?Serie=CAANE

    :return: yields a Town object for each town
    """
    with open('spain.csv') as file:
        for row in csv.DictReader(file):
            yield Town(name=row['Municipio'],
                       region=row['Provincia'],
                       lat=float(row['Latitud ETRS89']),
                       lon=float(row['Longitud ETRS89']),
                       tz="CET",
                       elevation=float(row['Altitud']),
                       population=float(row['Altitud']))


for town in towns():
    town.date = date = datetime.datetime.today()
    print("{:%Y-%m-%d}  {:%H:%M:%S} - {:%H:%M:%S}  {} - {}".
          format(date, town.sunrise, town.sunset, town.region, town.name))
