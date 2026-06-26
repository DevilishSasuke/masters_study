from pydantic import BaseModel, ConfigDict, Field

class ItemResponse(BaseModel):
    name: str
    amount: int

    model_config = ConfigDict(from_attributes=True)

class Item(ItemResponse):
    id: int

class ItemUpdate(BaseModel):
    amount: int = Field(..., ge=1)
    
class Order(BaseModel):
    id: int
    item_name: str
    amount: int

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    name: str