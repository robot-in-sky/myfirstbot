from core.entities.visas import Visa, VisaType
from core.entities.visas.enums.country import Country


class VisaService:

    def __init__(self) -> None:
        self._visas = [
            Visa(
                id="ind_tour_30d",
                country=Country.IND,
                type=VisaType.TOURIST,
                period="30d",
                form_id="ind_tour",
                consular_fee=25,
                app_period="1d",
                proc_days_min=3,
                proc_days_max=5,
                price=3200,
            ),
            Visa(
                id="ind_tour_1y",
                country=Country.IND,
                type=VisaType.TOURIST,
                period="1y",
                form_id="ind_tour",
                consular_fee=40,
                app_period="1d",
                proc_days_min=3,
                proc_days_max=5,
                price=4600,
            ),
            Visa(
                id="ind_tour_5y",
                country=Country.IND,
                type=VisaType.TOURIST,
                period="5y",
                form_id="ind_tour",
                consular_fee=80,
                app_period="1d",
                proc_days_min=3,
                proc_days_max=5,
                price=8500,
            ),
        ]

    def get_countries(self) -> list[Country]:
        return list({v.country for v in self._visas})

    def get_visas_by_country(self, country: Country) -> list[Visa]:
        return [v for v in self._visas if v.country == country]

    def get_visa(self, id_: str) -> Visa:
        return next(v for v in self._visas if v.id == id_)
