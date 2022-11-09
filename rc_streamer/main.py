import argparse
import logging
import os
import pathlib
import sys

from aiohttp import web
import tomlkit

from .app import init


def main(args=None, /, *, _conf_path='config.toml'):
    CONF_PATH = os.environ.get(
        f'{__package__.upper()}_CONF',
        _conf_path,
    )
    parser = argparse.ArgumentParser(
        prog=f"{__package__}",
        formatter_class=lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=52),
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count', default=1,
        help="Log loudness"
    )
    parser.add_argument(
        '-H', '--host',
        default='localhost',
        help="Host to listen on",
    )
    parser.add_argument(
        '-P', '--port',
        type=int, default=42069,
        help="Port to listen on"
    )
    parser.add_argument(
        '-c', '--config',
        type=pathlib.Path,
        default=pathlib.Path(CONF_PATH).resolve(),
        metavar='PATH',
        help="Path to config file"
    )
    args = parser.parse_args(args=args)
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(args.verbose, 2)]
    app = init(config=tomlkit.loads(args.config.read_text(encoding='utf-8')))
    logging.basicConfig(level=level)
    args = dict(
        host=args.host,
        port=args.port,
    )
    if level <= 20:
        args['access_log'] = None
    try:
        web.run_app(app, **args)
    except web.GracefulExit:
        pass


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
