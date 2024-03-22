import datetime
import traceback

from fastapi import Depends, APIRouter, HTTPException
from influxdb_client import QueryApi
from itertools import chain
import asyncio

from sqlalchemy import select, update, delete

from src.api.endpoints.flats.core import notify_device_target_flat_temperature, notify_device_schedule_segment, \
    get_latest_flat_temperature
from src.core.db import get_influx_query, async_session_factory
from src.models.temp_schedule import TempScheduleEntry





# TODO: remove schedule when selecting other modes
async def remove_schedule(flat: int):
    async with async_session_factory() as session:
        await session.execute(
            delete(TempScheduleEntry).where(TempScheduleEntry.flat == flat)
        )


async def get_schedule_entries(flat: int) -> list[TempScheduleEntry]:
    async with async_session_factory() as session:
        res = await session.execute(select(TempScheduleEntry).where(TempScheduleEntry.flat == flat).order_by(TempScheduleEntry.end_offset.asc()))
        return res.scalars().all()


async def get_current_segment(flat: int) -> TempScheduleEntry | None:
    entries = await get_schedule_entries(flat)
    for entry in entries[::-1]:
        if entry.was_sent and entry.start_time + datetime.timedelta(seconds=entry.start_offset) < datetime.datetime.now() < entry.start_time + datetime.timedelta(seconds=entry.end_offset):
            return entry
    return None

async def process_room_schedule_call_this_once_every_second_for_every_room(room: int):
    # print('Processing room', room, id(asyncio.get_running_loop()))
    async with async_session_factory() as session:
        # print('With session')
        query = (
            select(TempScheduleEntry)
            .where(TempScheduleEntry.flat == room)
            .order_by(TempScheduleEntry.end_offset.asc())
        )
        res = await session.execute(query)
        entries: list[TempScheduleEntry] = list(res.scalars().all())
        # print(room, entries)
        for entry in entries:
            if entry.was_sent:
                continue
            if datetime.datetime.now() > entry.start_time + datetime.timedelta(
                seconds=entry.start_offset
            ):
                notify_device_schedule_segment(room, entry)
                print(
                    f"[TS] Activating entry for flat {room}: s={entry.start_offset} e={entry.end_offset} tt={entry.target_temp}"
                )

                entry.was_sent = True
                break
        if entries:
            last_entry = entries[-1]
            if (
                last_entry.was_sent
                and datetime.datetime.now()
                > last_entry.start_time
                + datetime.timedelta(seconds=last_entry.end_offset)
            ):
                print(f"[TS] Dropping schedule for flat {room}")
                await session.execute(
                    delete(TempScheduleEntry).where(TempScheduleEntry.flat == room)
                )
                # set flat to prev value
                temp = get_latest_flat_temperature(room)
                notify_device_target_flat_temperature(room, temp)

        await session.commit()


async def start_scheduler_loop():
    print("Starting loop")
    try:
        while True:
            await asyncio.sleep(1)
            for room in range(1, 7):
                await process_room_schedule_call_this_once_every_second_for_every_room(
                    room
                )
    except Exception:
        traceback.print_exc()
