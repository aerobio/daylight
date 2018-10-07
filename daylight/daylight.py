
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

        :param name: town's name
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
        return self._sun['sunrise'].replace(tzinfo=None)

    @property
    def sunset(self):
        return self._sun['sunset'].replace(tzinfo=None)


def towns():
    """
    Spanish towns
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


start_0 = datetime.timedelta(hours=9)
start_1 = datetime.timedelta(hours=8)
start_2 = datetime.timedelta(hours=7)

finish_0 = datetime.timedelta(hours=16)
finish_1 = datetime.timedelta(hours=15)
finish_2 = datetime.timedelta(hours=14)

day = datetime.timedelta(days=1)

date = datetime.datetime(2019, 1, 1)


m0 = m1 = m2 = e0 = e1 = e2 = 0

for town in towns():
    town.date = date = datetime.datetime(2019,1,1)
    print("{:%Y-%m-%d}  {:%H:%M:%S} - {:%H:%M:%S}  {} - {}".
          format(town.date, town.sunrise, town.sunset, town.region, town.name))

    sr = town.sunrise
    morning_0 = max(0, town.population * (sr - (date + start_0)).total_seconds()/3600)
    morning_1 = max(0, town.population * (sr - (date + start_1)).total_seconds()/3600)
    morning_2 = max(0, town.population * (sr - (date + start_2)).total_seconds()/3600)
    print(morning_0, morning_1, morning_2)
    m0 += morning_0
    m1 += morning_1
    m2 += morning_2

    ss = town.sunset
    evening_0 = max(0, town.population * ((date + finish_0) - ss).total_seconds()/3600)
    evening_1 = max(0, town.population * ((date + finish_1) - ss).total_seconds()/3600)
    evening_2 = max(0, town.population * ((date + finish_2) - ss).total_seconds()/3600)
    print(evening_0, evening_1, evening_2)
    e0 += evening_0
    e1 += evening_1
    e2 += evening_2

print(m0, m1, m2)
print(e0, e1, e2)
