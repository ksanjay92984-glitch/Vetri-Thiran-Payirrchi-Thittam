from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room: str = Field(min_length=2)
    style: str = "Modern"
    items: str = "lights, ceiling fan, storage"

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: str = "Birthday"
    venue: str = "Indoor"

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = "Wedding"
    style: str = "Elegant"
    outfit_color: Optional[str] = None

class Recommendation(BaseModel):
    category: str
    item: str
    estimated_price: float
    platform: str
    reason: str

class PlannerResponse(BaseModel):
    planner: str
    budget: float
    summary: str
    recommendations: List[Recommendation]
