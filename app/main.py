from fastapi import FastAPI, Depends, Query
import uvicorn
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Spimex_Trading_Results
from depends import get_db
from datetime import datetime
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Date
from cache import get_cache, get_key, set_cache


app = FastAPI()


@app.get("/get_last_trading_dates")
async def get_last_trading_dates(
    db: Annotated[AsyncSession, Depends(get_db)], limit: Annotated[int, Query(gt=0)]
):
    cache_key = get_key("get_last_trading_dates", limit)
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data
    result = await db.scalars(
        select(Spimex_Trading_Results.date)
        .group_by(Spimex_Trading_Results.date)
        .order_by(cast(Spimex_Trading_Results.date, Date).desc())
        .limit(limit)
    )
    set_cache(cache_key, result)
    return result.all()


@app.get("/get_dynamics")
async def get_dynamics(
    db: Annotated[AsyncSession, Depends(get_db)],
    oil_id: Annotated[str, Query(max_length=4)],
    delivery_type_id: Annotated[str, Query(max_length=1)],
    delivery_basis_id: Annotated[str, Query(max_length=3)],
    start_date: Annotated[
        str,
        Query(
            regex="^(0[1-9]|[12][0-9]|3[01])[.\-/](0[1-9]|1[0-2])[.\-/]\d{4}$",
            description='Enter date in the format:"dd.mm.yyyy"',
        ),
    ],
    end_date: Annotated[
        str,
        Query(
            regex="^(0[1-9]|[12][0-9]|3[01])[.\-/](0[1-9]|1[0-2])[.\-/]\d{4}$",
            description='Enter date in the format:"dd.mm.yyyy"',
        ),
    ],
):
    cache_key = get_key("get_dynamics", oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data
    result = await db.scalars(
        select(Spimex_Trading_Results).where(
            Spimex_Trading_Results.oil_id == oil_id,
            Spimex_Trading_Results.delivery_type_id == delivery_type_id,
            Spimex_Trading_Results.delivery_basis_id == delivery_basis_id,
            cast(Spimex_Trading_Results.date, Date) <= datetime.strptime(start_date, "%d.%m.%Y").date(),
            cast(Spimex_Trading_Results.date, Date) >= datetime.strptime(end_date, "%d.%m.%Y").date(),
        )
    )
    set_cache(cache_key, result)
    return result.all()


@app.get("/get_trading_results")
async def get_trading_results(
    db: Annotated[AsyncSession, Depends(get_db)],
    oil_id: Annotated[str, Query(max_length=4)],
    delivery_type_id: Annotated[str, Query(max_length=1)],
    delivery_basis_id: Annotated[str, Query(max_length=3)],
):
    cache_key = get_key("get_trading_results", oil_id, delivery_type_id, delivery_basis_id)
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data
    result = await db.scalars(
        select(Spimex_Trading_Results).where(
            Spimex_Trading_Results.oil_id == oil_id,
            Spimex_Trading_Results.delivery_type_id == delivery_type_id,
            Spimex_Trading_Results.delivery_basis_id == delivery_basis_id
        )
    )
    set_cache(cache_key, result)
    return result.all()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
