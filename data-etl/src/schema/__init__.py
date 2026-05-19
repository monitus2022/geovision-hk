from dataclasses import dataclass
from typing import Optional


@dataclass
class Building:
    building_name_en: Optional[str]
    building_name_tc: Optional[str]
    top_height: Optional[float]
    base_height: Optional[float]
    geom: str
