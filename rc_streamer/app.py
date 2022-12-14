import asyncio
import importlib.resources as resources
import json
import logging

from aiohttp import web

import rc_common.crypt

from .ui import tk_app


routes = web.RouteTableDef()
background_tasks = set()
logger = logging.getLogger('streamer')


async def say(line):
    with resources.as_file(resources.files(__package__)) as pth:
        mimic = str(pth / 'bin' / 'mimic.exe')
        flags = 0x08000000
        proc = await asyncio.create_subprocess_exec(
            mimic,
            "-t",
            line,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            creationflags=flags,
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
    key = app['config'].key
    crypt = rc_common.crypt.from_key(key)
    return crypt.decrypt


def init(argv=None, /, *, config=None):
    app = web.Application()
    app['config'] = config if config is not None else {}
    app['verify'] = verify(app)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    app.add_routes(routes)
    return app
