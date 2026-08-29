from pydantic import BaseModel, Field
from typing import Optional, List

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    idea: str = Field(min_length=3, max_length=4000)
    budget: Optional[float] = Field(default=None, ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=6)

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    idea: Optional[str] = Field(default=None, min_length=3, max_length=4000)
    budget: Optional[float] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, min_length=3, max_length=6)

class CalculatorItem(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)

class CalculatorRequest(BaseModel):
    items: List[CalculatorItem]
    shipping: float = Field(default=0, ge=0)
    tax_percent: float = Field(default=0, ge=0, le=100)
    budget: Optional[float] = Field(default=None, ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=6)

class RegionRequest(BaseModel):
    country: str = Field(min_length=2, max_length=80)
    region: Optional[str] = Field(default=None, max_length=120)
