from core.entities.base import Base

from .enums.country import Country
from .enums.visa_type import VisaType


class Visa(Base):
    id: str
    country: Country
    type: VisaType
    period: str
    form_id: str
    consular_fee: float
    price: float
    app_period: str
    proc_days_min: int
    proc_days_max: int
