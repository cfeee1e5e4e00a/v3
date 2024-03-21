import datetime
import traceback

from fastapi import Depends, APIRouter, HTTPException
from influxdb_client import QueryApi
from itertools import chain
import asyncio

from sqlalchemy import select, update, delete

from src.core.db import get_influx_query, async_session_factory
from src.models.temp_schedule import TempScheduleEntry
from src.models.user import Role
from src.schemas.influx import SensorData
from src.api.endpoints.auth.core import current_user
from src.api.endpoints.flats import flats_router as router
from src.schemas.schedule import Schedule


@router.post("/{flat}/schedule")
async def set_flat_temp_schedule(
    flat: int,
    user: current_user(),
    schedule: Schedule,
):
    async with async_session_factory() as session:
        await session.execute(
            delete(TempScheduleEntry).where(TempScheduleEntry.flat == flat)
        )
        start_time = datetime.datetime.now()
        prev_offset = 0
        for entry in schedule.entries:
            session.add(
                TempScheduleEntry(
                    flat=flat,
                    start_time=start_time,
                    was_sent=False,
                    start_offset=prev_offset,
                    end_offset=entry.time,
                    target_temp=entry.temp,
                )
            )
            prev_offset = entry.time
        await session.commit()


@router.get("/{flat}/has_schedule")
async def flat_has_schedule(flat: int) -> bool:
    async with async_session_factory() as session:
        res = await session.execute(
            select(TempScheduleEntry).where(TempScheduleEntry.flat == flat)
        )
        return res.scalars().first() is not None


# TODO: remove schedule when selecting other modes
async def remove_schedule(flat: int):
    async with async_session_factory() as session:
        await session.execute(
            delete(TempScheduleEntry).where(TempScheduleEntry.flat == flat)
        )


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
                # TODO: send to mqtt
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
