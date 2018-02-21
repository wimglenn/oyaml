import sys
from collections import OrderedDict

import yaml as pyyaml


_viewitems = 'viewitems' if sys.version_info < (3,) else 'items'


def _representer(dumper, data):
    return dumper.represent_dict(getattr(data, _viewitems)())


def _constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


pyyaml.add_representer(dict, _representer)
pyyaml.add_representer(OrderedDict, _representer)


if sys.version_info < (3, 7):
    pyyaml.add_constructor(pyyaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _constructor)


# Merge PyYAML namespace into ours.
# This allows users a drop-in replacement:
#   import oyaml as yaml
from yaml import *
