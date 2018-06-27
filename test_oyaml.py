import sys
from collections import OrderedDict
from types import GeneratorType

import pytest

import oyaml as yaml


data = OrderedDict([('x', 1), ('z', 3), ('y', 2)])


def test_dump():
    assert yaml.dump(data) == '{x: 1, z: 3, y: 2}\n'


def test_safe_dump():
    assert yaml.safe_dump(data) == '{x: 1, z: 3, y: 2}\n'


def test_dump_all():
    assert yaml.dump_all(documents=[data, {}]) == '{x: 1, z: 3, y: 2}\n--- {}\n'


def test_dump_and_safe_dump_match():
    mydict = {'x': 1, 'z': 2, 'y': 3}
    # don't know if mydict is ordered in the implementation or not (but don't care)
    assert yaml.dump(mydict) == yaml.safe_dump(mydict)


def test_safe_dump_all():
    assert yaml.safe_dump_all(documents=[data, {}]) == '{x: 1, z: 3, y: 2}\n--- {}\n'


def test_load():
    loaded = yaml.load('{x: 1, z: 3, y: 2}')
    assert loaded == {'x': 1, 'z': 3, 'y': 2}


def test_load_all():
    gen = yaml.load_all('{x: 1, z: 3, y: 2}\n--- {}\n')
    assert isinstance(gen, GeneratorType)
    ordered_data, empty_dict = gen
    assert empty_dict == {}
    assert ordered_data == data


@pytest.mark.skipif(sys.version_info >= (3,7), reason="requires python3.6-")
def test_loads_to_ordered_dict():
    loaded = yaml.load('{x: 1, z: 3, y: 2}')
    assert isinstance(loaded, OrderedDict)


@pytest.mark.skipif(sys.version_info < (3,7), reason="requires python3.7+")
def test_loads_to_std_dict():
    loaded = yaml.load('{x: 1, z: 3, y: 2}')
    assert not isinstance(loaded, OrderedDict)
    assert isinstance(loaded, dict)


class MyOrderedDict(OrderedDict):
    pass


@pytest.mark.skipif(yaml.pyyaml.__version__ >= '4', reason="requires PyYAML version < 4")
def test_subclass_dump_pyyaml3():
    data = MyOrderedDict([('x', 1), ('y', 2)])
    assert '!!python/object/apply:test_oyaml.MyOrderedDict' in yaml.dump(data)
    with pytest.raises(yaml.pyyaml.representer.RepresenterError) as cm:
        yaml.safe_dump(data)
    assert str(cm.value) == "cannot represent an object: MyOrderedDict([('x', 1), ('y', 2)])"


@pytest.mark.skipif(yaml.pyyaml.__version__ < '4', reason="requires PyYAML version >= 4")
def test_subclass_dump_pyyaml4():
    data = MyOrderedDict([('x', 1), ('y', 2)])
    assert '!!python/object/apply:test_oyaml.MyOrderedDict' in yaml.danger_dump(data)
    with pytest.raises(yaml.pyyaml.representer.RepresenterError) as cm:
        yaml.dump(data)
    assert str(cm.value) == "('cannot represent an object', MyOrderedDict([('x', 1), ('y', 2)]))"


def test_anchors_and_references():
    text = '''
        defaults:
          all: &all
            product: foo
          development: &development
            <<: *all
            profile: bar

        development:
          platform:
            <<: *development
            host: baz
    '''
    expected_load = {
        'defaults': {
            'all': {
                'product': 'foo',
            },
            'development': {
                'product': 'foo',
                'profile': 'bar',
            },
        },
        'development': {
            'platform': {
                'host': 'baz',
                'product': 'foo',
                'profile': 'bar',
            },
        },
    }
    assert yaml.load(text) == expected_load
