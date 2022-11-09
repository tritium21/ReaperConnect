import pathlib
from rc_moderator.app import main

conf_path = pathlib.Path(__file__).with_name('config.toml')
main(conf_path=conf_path)
