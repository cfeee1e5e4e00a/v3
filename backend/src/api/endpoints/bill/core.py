import json
import numpy as np
from io import BytesIO
from matplotlib import pyplot as plt
from typing import Literal
import numpy as np
from datetime import datetime
from datetime import timedelta
from fpdf import FPDF
from sqlalchemy import select
from influxdb_client import QueryApi
from influxdb_client.client.flux_table import FluxRecord

from src.models import (
    _CENTRAL_WINDOWS_SIZE,
    _FLAT_VOLUME,
    _FLAT_WINDOWS_SIZE,
    _SECOND_FLOOR_FLAT_VOLUME,
    α,
    dQ_to_V,
)
from src.core.db import async_session_factory, get_influx_query
from src.models.bill import Bill, Status
import random

async def create_bill(amount: float, status: Status, user_id: int):
    bill = Bill(amount=amount, status=status, user_id=user_id)
    async with async_session_factory() as session:
        session.add(bill)
        await session.commit()
        return bill.id


async def get_bill(id: int):
    async with async_session_factory() as session:
        query = select(Bill).where(Bill.id == id)
        return (await session.execute(query)).scalars().first()


async def get_user_bills_list(user_id: int):
    async with async_session_factory() as session:
        query = select(Bill).where(Bill.user_id == user_id)
        return (await session.execute(query)).scalars().all()


async def change_bill_status(id: int):
    async with async_session_factory() as session:
        query = select(Bill).where(Bill.id == id)
        bill = (await session.execute(query)).scalars().first()
        bill.status = Status.PAID
        await session.commit()
        return {"bill_id": id}


def stabilization_cost(flat_id: int, dT: np.ndarray, dt: float) -> float:
    return (
        α
        * _FLAT_WINDOWS_SIZE.get(flat_id, _CENTRAL_WINDOWS_SIZE)
        * dt
        * np.where(dT <= 0, 0, dT)
    )


# TODO: Добавить сюда энергопотребление в процентах
def regulation_cost(flat_id: int, T_in: float, T_in_previous: float) -> float:
    divT = T_in / T_in_previous
    divT = np.where(divT < 1, 1.0, divT)
    return dQ_to_V * _FLAT_VOLUME.get(flat_id, _SECOND_FLOOR_FLAT_VOLUME) * np.log(divT)


def _get_millis_from_flux_record(r: FluxRecord) -> float:
    return r.get_time().timestamp()


def day_heats_by_range(
    query_api: QueryApi,
    flat_id: int,
    time_range: tuple[str, str],
    *,
    agg_every: str = "12s",
    agg_fn: Literal["mean", "median", "last"] = "last",
) -> np.ndarray[float]:
    start, stop = time_range
    _itt_querry = f"""from(bucket: "default")\
    |> range(start: {start}, stop: {stop})\
    |> filter(fn: (r) => r["_measurement"] == "temp")\
    |> filter(fn: (r) => r["flat"] == "{flat_id}")\
    |> drop(columns: ["_field", "_measurement", "flat", "host", "topic"])\
    |> aggregateWindow(every: {agg_every}, fn: {agg_fn}, createEmpty: false)"""
    T_out = 24.2
    T_in = query_api.query(_itt_querry)[0]

    t = np.fromiter(map(_get_millis_from_flux_record, iter(T_in)), dtype=np.float64)
    dt = np.diff(t)

    T_in = np.fromiter(map(FluxRecord.get_value, iter(T_in)), dtype=np.float64)
    # NOTE: apply mean by windowsize of 2 elements
    dT = np.convolve(T_in - T_out, [1 / 2, 1 / 2], mode="valid")

    reg_cost = regulation_cost(flat_id, T_in[1:], T_in[:-1])
    stab_cost = stabilization_cost(flat_id, dT, dt)

    # print(f"{reg_cost = }")
    # print(f"{stab_cost = }")

    return reg_cost + stab_cost


def heat_cost(
    query_api: QueryApi,
    flat_id: int,
    time_range: tuple[str, str],
) -> float:
    return np.sum(day_heats_by_range(query_api, flat_id, time_range))


async def all_bills():
    async with async_session_factory() as session:
        query = select(Bill)
        return (await session.execute(query)).scalars().all()


async def generate_pdf(bill_id: int):
    def new_pdf():
        price = 1000
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(family="b52", fname="src/FPDF_FONT_DIR/B52.ttf")
        pdf.set_font("b52", size=40)
        pdf.cell(text="Счет на оплату")
        # TODO: Apply heat cost
        # TODO: Apply heat amount
        pdf.multi_cell(
            text=f" Объём потреблённого тепла: {100} \n К оплате: {1000}",
            align="C",
            w=0,
        )
        return pdf.output()

    async with async_session_factory() as session:
        query = select(Bill).where(Bill.id == bill_id)
        bill = (await session.execute(query)).scalars().first()
        bill.pdf = new_pdf()
        await session.commit()
        return bytes(bill.pdf)


def gen_images(Xs, Ys, x_caption, y_caption, label):
    fig = plt.figure()
    plot = fig.subplots()

    plot.plot(Xs, Ys)
    plot.set_xlabel(x_caption)
    plot.set_ylabel(y_caption)
    bio = BytesIO()
    plot.figure.savefig(bio, format="png")
    # plot.
    return bio


async def make_report_user_1_floor(
    room: int, start_date: datetime, end_date: datetime
) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    # pdf.add_font(family='b52', fname='B52.ttf')
    pdf.add_font(family="b52", fname="src/FPDF_FONT_DIR/B52.ttf")
    pdf.set_font("b52", size=20)
    pdf.cell(text=f"Счет на оплату за квартиру {room}", align="C", w=0, ln=1)
    pdf.set_font("b52", size=10)
    pdf.cell(text=f"{start_date} - {end_date}", align="C", w=0, ln=1)
    pdf.cell(text="", align="L", w=0, ln=1, h=10)
    pdf.set_font("b52", size=20)
    pdf.cell(text=f"Объем потребленного тепла: {random.uniform(10.0, 100.0)} кВт", align="L", w=0, ln=1)

    query_api = next(get_influx_query())

    query = f"""from(bucket: "default")\
        |> range(start: {start_date.isoformat().split('+')[0]}Z, stop: {end_date.isoformat().split('+')[0]}Z)
        |> filter(fn: (r) => r["_measurement"] == "temp")\
        |> filter(fn: (r) => r["flat"] == "{room}")\
        |> filter(fn: (r) => r["_field"] == "value")\
        |> sort(columns: ["_time"])\
        """

    data = json.loads(query_api.query(query).to_json())
    Xs = []
    Ys = []
    for i in data:
        Ys.append(i["_value"])
        Xs.append(datetime.fromisoformat(i["_time"]) + timedelta(hours=7))

    consumption_chart = gen_images(
        Xs, Ys, "Дата", "Фактическая температура", "Температура"
    )

    # second chart
    query = f"""from(bucket: "default")\
            |> range(start: {start_date.isoformat().split('+')[0]}Z, stop: {end_date.isoformat().split('+')[0]}Z)
            |> filter(fn: (r) => r["_measurement"] == "set_temp")\
            |> filter(fn: (r) => r["flat"] == "{room}")\
            |> filter(fn: (r) => r["_field"] == "value")\
            |> sort(columns: ["_time"])\
            """
    data = json.loads(query_api.query(query).to_json())
    Xs = []
    Ys = []
    for i in data:
        Ys.append(i["_value"])
        Xs.append(datetime.fromisoformat(i["_time"]) + timedelta(hours=7))
    trend_chart = gen_images(Xs, Ys, "Дата", "Заданная температура", "not used")

    pdf.image(consumption_chart, w=pdf.epw * 0.95)
    pdf.image(trend_chart, w=pdf.epw * 0.95)
    return pdf.output()


if __name__ == "__main__":
    from src.core.db import get_influx_query

    query_api = next(get_influx_query())
    print(
        day_heats_by_range(
            query_api,
            5,
            ("-1h", "-0s"),
        )
    )
