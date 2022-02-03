#!/usr/bin/env python3

import yaml


def hexint_presenter(dumper, data):
    return dumper.represent_int(hex(data))


yaml.add_representer(int, hexint_presenter)


def yaml_dump(obj):
    return yaml.dump(obj, sort_keys=False, Dumper=yaml.Dumper)


def yaml_load(s):
    return yaml.load(s, Loader=yaml.Loader)
