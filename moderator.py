import pathlib
import sys
from rc_moderator.app import main

if getattr(sys, 'frozen', False):
    base = sys.executable
else:
    base = __file__

conf_path = pathlib.Path(base).with_name('config.toml')
main(conf_path=conf_path)
