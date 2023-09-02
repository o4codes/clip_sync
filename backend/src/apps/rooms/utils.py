import json

from fastapi import BackgroundTasks

from src.apps.rooms import schema
from src.config.dependencies.cache import Cache
from src.libs import utils
from src.libs.websockets import WebSocketEmitter


async def get_client_session(room_session: str = None):
    if room_session:
        room_session_data: dict = json.loads(room_session)
        session_data = await Cache.get(room_session_data.get("invite_code"))
        return session_data


def generate_username(user_agent: str):
    parsed_user_agent = utils.parse_user_agent(user_agent)
    return (
        f"{parsed_user_agent.get('device_brand') or ''} {parsed_user_agent.get('os')}"
    )


def generate_background_tasks(room_id: str, events: list[schema.EventDataDict]):
    tasks = BackgroundTasks()
    for event_data in events:
        tasks.add_task(
            WebSocketEmitter.publish,
            channel=room_id,
            event=event_data.get("event"),
            data=event_data.get("data"),
        )
    return tasks
