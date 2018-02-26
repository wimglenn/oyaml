import sys
from collections import OrderedDict

import yaml as pyyaml


_items = 'viewitems' if sys.version_info < (3,) else 'items'


def map_representer(dumper, data):
    return dumper.represent_dict(getattr(data, _items)())


def map_constructor(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


pyyaml.add_representer(dict, map_representer)
pyyaml.add_representer(OrderedDict, map_representer)


if sys.version_info < (3, 7):
    pyyaml.add_constructor('tag:yaml.org,2002:map', map_constructor)


del map_constructor, map_representer


# Merge PyYAML namespace into ours.
# This allows users a drop-in replacement:
#   import oyaml as yaml
from yaml import *
