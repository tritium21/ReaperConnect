import asyncio
import base64
import importlib.resources as resources
import json
import logging

from aiohttp import web
import nacl.secret
import nacl.exceptions

from .ui import tk_app


routes = web.RouteTableDef()
background_tasks = set()
logger = logging.getLogger()


async def say(line):
    with resources.as_file(resources.files(__package__)) as pth:
        mimic = str(pth / 'bin' / 'mimic.exe')
        proc = await asyncio.create_subprocess_exec(
            mimic,
            "-t",
            line,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await proc.wait()


@routes.post('/say')
async def say_handler(request):
    data = await request.post()
    if (body := data.get('body')) is None or (line := request.app['verify'](body)) is None:
        raise web.HTTPBadRequest(body=json.dumps({'status': '400', 'reason': 'Missing or malformed body'}))
    logger.info(f"Said: {line}")
    task = asyncio.create_task(say(line))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return web.json_response({'status': 200})


async def on_startup(app):
    app['UI'] = app.loop.create_task(tk_app())


async def on_shutdown(app):
    try:
        app['UI'].exception()
    except asyncio.InvalidStateError:
        pass


def verify(app):
    key = app['config'].get('key')
    if key is None:
        return lambda x: x
    key = base64.b64decode(key)
    box = nacl.secret.SecretBox(key)

    def inner(message):
        message = base64.b64decode(message)
        try:
            return box.decrypt(message).decode('utf-8')
        except nacl.exceptions.CryptoError:
            return None
    return inner


def init(argv=None, /, *, config=None):
    app = web.Application()
    app['config'] = config if config is not None else {}
    app['verify'] = verify(app)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    app.add_routes(routes)
    return app
