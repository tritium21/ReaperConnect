import logging
import pathlib
import sys

from aiohttp import web

from .app import init
from rc_common.config import load


def main(args=None, /, *, conf_path='config.toml'):
    config = load(pathlib.Path(conf_path).resolve())
    logging.basicConfig(level=logging.INFO)
    args = dict(
        app=init(config=config),
        host=config.streamer.host,
        port=config.streamer.port,
        access_log=None
    )
    web.run_app(**args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
