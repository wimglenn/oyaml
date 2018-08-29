import sys
from collections import OrderedDict

import yaml as pyyaml


_items = 'viewitems' if sys.version_info < (3,) else 'items'


def map_representer(dumper, data):
    return dumper.represent_dict(getattr(data, _items)())


def map_constructor(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


if pyyaml.safe_dump is pyyaml.dump:
    # PyYAML v4.1
    SafeDumper = pyyaml.dumper.Dumper
    DangerDumper = pyyaml.dumper.DangerDumper
    SafeLoader = pyyaml.loader.Loader
    DangerLoader = pyyaml.loader.DangerLoader
else:
    SafeDumper = pyyaml.dumper.SafeDumper
    DangerDumper = pyyaml.dumper.Dumper
    SafeLoader = pyyaml.loader.SafeLoader
    DangerLoader = pyyaml.loader.Loader

pyyaml.add_representer(dict, map_representer, Dumper=SafeDumper)
pyyaml.add_representer(OrderedDict, map_representer, Dumper=SafeDumper)
pyyaml.add_representer(dict, map_representer, Dumper=DangerDumper)
pyyaml.add_representer(OrderedDict, map_representer, Dumper=DangerDumper)


if sys.version_info < (3, 7):
    pyyaml.add_constructor('tag:yaml.org,2002:map', map_constructor, Loader=SafeLoader)
    pyyaml.add_constructor('tag:yaml.org,2002:map', map_constructor, Loader=DangerLoader)


del map_constructor, map_representer


# Merge PyYAML namespace into ours.
# This allows users a drop-in replacement:
#   import oyaml as yaml
from yaml import *
