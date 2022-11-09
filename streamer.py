import pathlib
import sys
from rc_streamer.main import main
from rc_streamer.first_run import new_config_init

if getattr(sys, 'frozen', False):
    base = sys.executable
else:
    base = __file__

conf_path = pathlib.Path(base).with_name('config.toml')
if not conf_path.exists():
    new_config_init(conf_path)

main(conf_path=conf_path)
