import datetime
import json
from io import BytesIO
from math import log2, e
from matplotlib import pyplot as plt

from fpdf import FPDF
from sqlalchemy import select
from src.core.db import async_session_factory, get_influx_query
from src.models.bill import Bill, Status

type m2 = float
type m3 = float

α = 20  # window heat transfer coef
dQ_to_V = 350.722  # heat per logarifmic ration of temperatures per volume

_SIDE_WINDOWS_SIZE: m2 = 0.0093
_CENTRAL_WINDOWS_SIZE: m2 = 0.0057
_FLAT_WINDOWS_SIZE: dict[int, m2] = {
    1: _SIDE_WINDOWS_SIZE,
    2: _CENTRAL_WINDOWS_SIZE,
    3: _SIDE_WINDOWS_SIZE,
    4: _SIDE_WINDOWS_SIZE,
    5: _CENTRAL_WINDOWS_SIZE,
    6: _SIDE_WINDOWS_SIZE,
}

_SECOND_FLOOR_FLAT_VOLUME: m3 = 0.002
_FIRST_FLOOR_FLAT_VOLUME: m3 = 0.00225
_FLAT_VOLUME: dict[int, m3] = {
    1: _SECOND_FLOOR_FLAT_VOLUME,
    2: _SECOND_FLOOR_FLAT_VOLUME,
    3: _SECOND_FLOOR_FLAT_VOLUME,
    4: _FIRST_FLOOR_FLAT_VOLUME,
    5: _FIRST_FLOOR_FLAT_VOLUME,
    6: _FIRST_FLOOR_FLAT_VOLUME,
}


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


def stabilization_cost(flat_id: int, dT: float, dt: float) -> float:
    return α * _FLAT_WINDOWS_SIZE.get(flat_id, _CENTRAL_WINDOWS_SIZE) * dt * max(0.0, dT)


def regulation_cost(flat_id: int, T_in: float, T_in_previous: float) -> float:
    return (
        dQ_to_V
        * _FLAT_VOLUME.get(flat_id, _SECOND_FLOOR_FLAT_VOLUME)
        * log2(T_in / T_in_previous)
        / log2(e)
    )


def heating_cost(start, end):
    pass

async def all_bills():
    async with async_session_factory() as session:
        query = select(Bill)
        return (await session.execute(query)).scalars().all()


async def generate_pdf(bill_id: int):
    def new_pdf():
        price = 1000
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(family='b52',fname='src/FPDF_FONT_DIR/B52.ttf')
        pdf.set_font('b52', size=40)
        pdf.cell(text='Счет на оплату')
        pdf.multi_cell(text=f" Объём потреблённого тепла: {100} \n К оплате: {1000}",
                       align='C', w=0)
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
    plot.figure.savefig(bio, format='png')
    # plot.
    return bio

async def make_report_user_1_floor(room: int, start_date: datetime.datetime, end_date: datetime.datetime) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    # pdf.add_font(family='b52', fname='B52.ttf')
    pdf.add_font(family='b52', fname='src/FPDF_FONT_DIR/B52.ttf')
    pdf.set_font('b52', size=40)
    pdf.cell(text=f'Счет на оплату за квартиру {room}', align='C', w=0, ln=1)
    pdf.set_font('b52', size=20)
    pdf.cell(text=f'{start_date} - {end_date}', align='C', w=0, ln=1)
    pdf.cell(text='', align='L', w=0, ln=1, h=10)
    pdf.set_font('b52', size=25)
    pdf.cell(text=f'Объем потребленного тепла: <UNKNOWN> кВт', align='L', w=0, ln=1)
    #графики заданного и текущего тренда

    query_api = next(get_influx_query())

    query = f"""from(bucket: "default")\
        |> range(start: {start_date.isoformat().split('+')[0]}Z, stop: {end_date.isoformat().split('+')[0]}Z)
        |> filter(fn: (r) => r["_measurement"] == "temp")\
        |> filter(fn: (r) => r["flat"] == "{room}")\
        |> filter(fn: (r) => r["_field"] == "value")\
        |> sort(columns: ["_time"])\
        """


    # print(query)

    # first chart
    data = json.loads(query_api.query(query).to_json())
    Xs = []
    Ys = []
    for i in data:
        Ys.append(i['_value'])
        Xs.append(datetime.datetime.fromisoformat(i['_time'])+datetime.timedelta(hours=7))
    # print(data)

    consumption_chart = gen_images(Xs, Ys, 'Дата', 'Фактическая температура', 'Температура')

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
        Ys.append(i['_value'])
        Xs.append(datetime.datetime.fromisoformat(i['_time']) + datetime.timedelta(hours=7))
    trend_chart = gen_images(Xs, Ys, 'Дата', 'Заданная температура', 'not used')


    # url = f'http://grafana.cfeee1e5e4e00a.ru:3000/render/d-solo/e6808168-29f4-4aca-854e-88948c406ff9/billing?orgId=1&from=1711005732627&to=1711027332627&theme=light&panelId=1&width=1000&height=500&tz=Asia%2FTomsk'
    pdf.image(consumption_chart, w=pdf.epw*0.95)
    pdf.image(trend_chart, w=pdf.epw * 0.95)
    return pdf.output()
