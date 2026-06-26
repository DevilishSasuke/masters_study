from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from warehouse.db import get_db_session
from warehouse.models import Order
from warehouse.schemas import OrderCreate, Order as OrderResponse
from warehouse.routers.items import reduce_item
from prometheus_client import Counter
import logging

orders_created = Counter("orders_created", 
                               "total number of successful orders",
                               labelnames=["item_name"])
orders_failed = Counter("orders_failed", 
                              "total count of failed order creation",
                              labelnames=["reason"])
                                # amount - because of sold out items
                                # nonexist - because of non existing items
orders_deleted = Counter("orders_deleted",
                         "total count of deleted orders")

router = APIRouter(prefix="/orders")
logger = logging.getLogger("warehouse_logger")

@router.get("", response_model=List[OrderResponse])
async def get_all_orders(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Order))
    orders_list = result.scalars().all()

    if not orders_list:
        raise HTTPException(status_code=404, detail="Table doesn't exist")
    return orders_list

@router.get("/{id}", response_model=OrderResponse)
async def get_order_by_id(id: int, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Order).where(Order.id == id))
    db_order = result.scalar_one_or_none()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order doesn't exist")
    return db_order

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Order).where(Order.id == id))
    db_order = result.scalar_one_or_none()

    if not db_order:
        raise HTTPException(status_code=404, detail="order not found, nothing to delete")
    
    await session.delete(db_order)
    await session.commit()

    orders_deleted.inc()
    return {"description": "order was successfully deleted"}

@router.post("", response_model=OrderResponse)
async def create_order(data: OrderCreate, session: AsyncSession = Depends(get_db_session)):
    try:
        await reduce_item(name=data.name, session=session)
    except HTTPException as e:
        if e.status_code == 400: 
            orders_failed.labels(reason="amount").inc()
            logger.warning(f"Attempt to order item that is out of stock: {data.name}",
                       extra={"tags": {
                           "event": "sold_out",
                           "item_name": data.name
                       }})
        if e.status_code == 404: 
            orders_failed.labels(reason="nonexist").inc()
            logger.warning(f"Attempt to order non existing item: {data.name}",
                       extra={"tags": {
                           "event": "non_exist",
                           "item_name": data.name
                       }})
        raise e

    new_order = Order(
        item_name=data.name,
        amount=1
    )

    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    
    orders_created.labels(item_name=data.name).inc()
    logger.info(f"Order was successfully created with item: {data.name}",
                       extra={"tags": {
                           "item_name": data.name
                       }})
    return new_order