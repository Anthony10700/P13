import json
import logging
import websockets
from django.contrib.auth import get_user_model
from . import models, router
from .utils import get_user_from_session, get_dialogs_with_user

logger = logging.getLogger('chat_public-dialog')
ws_connections = {}


async def fanout_message(connections, payload):
    """
    Distributes payload (message) to all connected ws clients
    """
    for conn in connections:
        try:
            await conn.send(json.dumps(payload))
        except Exception as e:
            logger.debug('could not send', e)


async def new_messages_handler(stream):
    """
    Saves a new chat message to db and distributes msg to connected users
    """
    while True:
        packet = await stream.get()
        session_id = packet.get('session_key')
        msg = packet.get('message')
        username_opponent = packet.get('username')
        if session_id and msg and username_opponent:
            user_owner = await get_user_from_session(session_id)
            if user_owner:
                user_opponent = get_user_model().objects.get(
                    username=username_opponent)

                dialog = get_dialogs_with_user(user_owner, user_opponent)
                if len(dialog) > 0:
                    msg = models.Message.objects.create(
                        dialog=dialog[0],
                        sender=user_owner,
                        text=packet['message'],
                        read=False
                    )
                    packet['created'] = msg.get_formatted_create_datetime()
                    packet['sender_name'] = msg.sender.username
                    packet['message_id'] = msg.id
                    connections = []
                    if (user_owner.username,
                            user_opponent.username) in ws_connections:
                        connections.append(
                            ws_connections[
                                (user_owner.username,
                                 user_opponent.username)])
                    if (user_opponent.username,
                            user_owner.username) in ws_connections:
                        connections.append(ws_connections[
                            (user_opponent.username, user_owner.username)])
                    else:
                        opponent_connections = list(
                            filter(lambda x: x[0] == user_opponent.username,
                                   ws_connections))
                        opponent_connections_sockets = [
                            ws_connections[i] for i in opponent_connections]
                        connections.extend(opponent_connections_sockets)
                    if user_opponent.username == "chat_user_all":
                        connections = []
                        for con in ws_connections:
                            if con[1] == "chat_user_all":
                                connections.append(ws_connections[con])
                    await fanout_message(connections, packet)
                else:
                    pass
            else:
                pass
        else:
            pass


async def main_handler(websocket, path):
    """
    An Asyncio Task is created for every new websocket client connection
    that is established. This coroutine listens to messages from the connected
    client and routes the message to the proper queue.

    This coroutine can be thought of as a producer.
    """

    path = path.split('/')
    username = path[2]
    session_id = path[1]
    user_owner = await get_user_from_session(session_id)
    if user_owner:
        user_owner = user_owner.username
        ws_connections[(user_owner, username)] = websocket

        try:
            while websocket.open:
                data = await websocket.recv()
                if not data:
                    continue
                logger.debug(data)
                try:
                    await router.MessageRouter(data)()
                except Exception as e:
                    logger.error('could not route msg', e)

        except websockets.exceptions.InvalidState:
            pass
        finally:
            del ws_connections[(user_owner, username)]
    else:
        logger.info("Got invalid session_id attempt to connect " + session_id)
