import rc_common.config


def new_config_init(path):
    config = rc_common.config.Config.new()
    rc_common.config.save(config, path)
