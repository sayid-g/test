from dataclasses import dataclass
from typing import Optional


@dataclass
class CarInfo:
    car_id: str
    brand: str
    series: str
    year: str
    model: Optional[str] = None
    price: Optional[str] = None
    sales_name: Optional[str] = None
    displacement: Optional[str] = None
    energy_type: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.car_id,
            'brand': self.brand,
            'series': self.series,
            'year': self.year,
            'model': self.model,
            'price': self.price,
            'sales_name': self.sales_name,
            'displacement': self.displacement,
            'energy_type': self.energy_type
        }
    
    def __str__(self):
        return f"CarInfo(id={self.car_id}, brand={self.brand}, series={self.series}, year={self.year})"
