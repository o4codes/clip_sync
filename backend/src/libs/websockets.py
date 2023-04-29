from enum import Enum
from typing import Any, Dict, Optional

import httpx
from decouple import config
from pydantic import BaseModel, Field

from . import exceptions


class WebsocketEvents(str, Enum):
    DEVICE_CONNECTED = "DEVICE_CONNECTED"
    DEVICE_DISCONNECTED = "DEVICE_DISCONNECTED"
    DEVICE_PUBLISH = "DEVICE_PUBLISH"


class WebSocketEmitter:
    """
    Serves as a wrapper for interfacing with centrifugo.
    It is used to publish events to websocket connection.
    """

    HOST = "0.0.0.0"
    PORT = config("CENTRIFUGO_PORT")
    CHANNEL_PREFIX = "$"

    def __init__(self) -> None:
        self.address = f"https://{self.HOST}:{self.PORT}/api"
        self.api_key = config("CENTRIFUGO_API_KEY")

        self.headers = {
            "Content-type": "application/json",
            "Authorization": "apikey " + self.api_key,
        }

    async def _send_command(self, data: Dict[str, Any]) -> Dict[int, Any]:
        """
        Connects to the Centrifugo server and sends command to execute via Centrifugo Server API.

        Args:
            data (Dict[int, Any]): The command to be sent to Centrifugo

        Raises:
            RequestException: There was an ambiguous exception that occurred while handling the request

        Returns:
            Dict[int, Any]: The response from Centrifugo after executing the command sent
        """

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self.address, json=data, headers=self.headers
                )
                return {"status_code": response.status_code, "message": response.json()}
        except httpx.RequestError as error:
            raise httpx.RequestError(error) from error

    async def publish(
        self,
        channel: str,
        event: WebsocketEvents,
        data: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Publish data into a channel.

        Args:
            channel (str): The name of the channel to publish to
            event (Events): Event enum obj associated with the data being published
            data (Dict[str, str]): Custom JSON data to publish into the room

        Returns:
            Dict[str, Any]: The formatted response after executing the command sent
        """
        data_publish = {
            "event": event.value,
            "data": data,
        }

        socket_data = {
            "method": "publish",
            "params": {
                "channel": f"{self.CHANNEL_PREFIX}{channel}",
                "data": data_publish,
            },
        }
        try:
            response = await self._send_command(socket_data)
        except httpx.RequestError:
            raise exceptions.InternalServerException("Error on websocket publish")
        else:
            if response and response.get("status_code") == 200:
                return data_publish
            raise exceptions.InternalServerException("Websocket Failure")


websocket_emitter = WebSocketEmitter()
