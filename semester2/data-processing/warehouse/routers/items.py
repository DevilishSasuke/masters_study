from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from warehouse.db import get_db_session
from warehouse.models import Item
from warehouse.schemas import ItemResponse, ItemUpdate
from prometheus_client import Counter
import logging
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

items_added = Counter("items_added",
                      "items added for each item",
                      labelnames=["item_name"])
items_sold = Counter("items_sold",
                        "items sold for each item",
                        labelnames=["item_name"])
items_error_soldout = Counter("items_error_soldout",
                         "amount of errors caused by items amount less than 1")

router = APIRouter(prefix="/items")
logger = logging.getLogger("warehouse_logger")

@router.get("", response_model=List[ItemResponse])
async def get_all_items(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Item))

    items_list = result.scalars().all()
    
    return items_list

@router.get("/{name}", response_model=ItemResponse)
async def get_item(name: str, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Item).where(Item.name == name))
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="This items is not exist")
    return db_item


@router.put("/{name}", response_model=ItemResponse)
async def update_item(name: str, data: ItemUpdate, session: AsyncSession = Depends(get_db_session)):
    with tracer.start_as_current_span("db.get_item") as span:
        span.set_attribute("item.name", name) 
        result = await session.execute(select(Item).where(Item.name == name))
        db_item = result.scalar_one_or_none()
    
    with tracer.start_as_current_span("logic.process_item") as span:
        if db_item:
            span.set_attribute("item.action", "updated")
            span.set_attribute("item.added_amount", data.amount)
            db_item.amount += data.amount
        else:
            span.set_attribute("item.action", "created")
            span.set_attribute("item.initial_amount", data.amount)
            db_item = Item(name=name, amount=data.amount)
            session.add(db_item)

    with tracer.start_as_current_span("db.commit_and_refresh"):
        await session.commit()
        await session.refresh(db_item)

    with tracer.start_as_current_span("metrics.update"):
        items_added.labels(item_name=name).inc(data.amount)
        
    return db_item

@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(name: str, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Item).where(Item.name == name))
    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(status_code=404, detail="item not found, nothing to delete")
    
    await session.delete(db_item)
    await session.commit()

    return {"description": "item was successfully deleted"}

@router.post("/{name}/reduce", response_model=ItemResponse)
async def reduce_item(name: str, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Item).where(Item.name == name))
    db_item = result.scalar_one_or_none()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.amount < 1:
        items_error_soldout.inc()

        raise HTTPException(status_code=400, detail="Item is sold out")
    
    db_item.amount -= 1
    await session.commit()
    await session.refresh(db_item)

    items_sold.labels(item_name=db_item.name).inc()
    return db_item
