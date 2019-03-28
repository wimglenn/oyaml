from collections import OrderedDict
from types import GeneratorType

import pytest
from yaml.constructor import ConstructorError
from yaml.representer import RepresenterError

import oyaml as yaml
from oyaml import _std_dict_is_order_preserving


data = OrderedDict([("x", 1), ("z", 3), ("y", 2)])


def test_dump():
    assert yaml.dump(data, default_flow_style=None) == "{x: 1, z: 3, y: 2}\n"


def test_safe_dump():
    assert yaml.safe_dump(data, default_flow_style=None) == "{x: 1, z: 3, y: 2}\n"


def test_dump_all():
    assert (
        yaml.dump_all(documents=[data, {}], default_flow_style=None)
        == "{x: 1, z: 3, y: 2}\n--- {}\n"
    )


def test_dump_and_safe_dump_match():
    mydict = {"x": 1, "z": 2, "y": 3}
    # don't know if mydict is ordered in the implementation or not (but don't care)
    assert yaml.dump(mydict) == yaml.safe_dump(mydict)


def test_safe_dump_all():
    assert (
        yaml.safe_dump_all(documents=[data, {}], default_flow_style=None)
        == "{x: 1, z: 3, y: 2}\n--- {}\n"
    )


def test_load():
    loaded = yaml.load("{x: 1, z: 3, y: 2}")
    assert loaded == {"x": 1, "z": 3, "y": 2}


def test_safe_load():
    loaded = yaml.safe_load("{x: 1, z: 3, y: 2}")
    assert loaded == {"x": 1, "z": 3, "y": 2}


def test_load_all():
    gen = yaml.load_all("{x: 1, z: 3, y: 2}\n--- {}\n")
    assert isinstance(gen, GeneratorType)
    ordered_data, empty_dict = gen
    assert empty_dict == {}
    assert ordered_data == data


@pytest.mark.skipif(_std_dict_is_order_preserving, reason="requires old dict impl")
def test_loads_to_ordered_dict():
    loaded = yaml.load("{x: 1, z: 3, y: 2}")
    assert isinstance(loaded, OrderedDict)


@pytest.mark.skipif(not _std_dict_is_order_preserving, reason="requires new dict impl")
def test_loads_to_std_dict():
    loaded = yaml.load("{x: 1, z: 3, y: 2}")
    assert not isinstance(loaded, OrderedDict)
    assert isinstance(loaded, dict)


@pytest.mark.skipif(_std_dict_is_order_preserving, reason="requires old dict impl")
def test_safe_loads_to_ordered_dict():
    loaded = yaml.safe_load("{x: 1, z: 3, y: 2}")
    assert isinstance(loaded, OrderedDict)


@pytest.mark.skipif(not _std_dict_is_order_preserving, reason="requires new dict impl")
def test_safe_loads_to_std_dict():
    loaded = yaml.safe_load("{x: 1, z: 3, y: 2}")
    assert not isinstance(loaded, OrderedDict)
    assert isinstance(loaded, dict)


class MyOrderedDict(OrderedDict):
    pass


def test_subclass_dump():
    data = MyOrderedDict([("x", 1), ("y", 2)])
    assert "!!python/object/apply:test_oyaml.MyOrderedDict" in yaml.dump(data)
    with pytest.raises(RepresenterError, match="cannot represent an object"):
        yaml.safe_dump(data)


def test_anchors_and_references():
    text = """
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
    """
    expected_load = {
        "defaults": {
            "all": {"product": "foo"},
            "development": {"product": "foo", "profile": "bar"},
        },
        "development": {
            "platform": {"host": "baz", "product": "foo", "profile": "bar"}
        },
    }
    assert yaml.load(text) == expected_load


def test_omap():
    text = """
        Bestiary: !!omap
          - aardvark: African pig-like ant eater. Ugly.
          - anteater: South-American ant eater. Two species.
          - anaconda: South-American constrictor snake. Scaly.
    """
    expected_load = {
        "Bestiary": (
            [
                ("aardvark", "African pig-like ant eater. Ugly."),
                ("anteater", "South-American ant eater. Two species."),
                ("anaconda", "South-American constrictor snake. Scaly."),
            ]
        )
    }
    assert yaml.load(text) == expected_load


def test_omap_flow_style():
    text = "Numbers: !!omap [ one: 1, two: 2, three : 3 ]"
    expected_load = {"Numbers": ([("one", 1), ("two", 2), ("three", 3)])}
    assert yaml.load(text) == expected_load


def test_merge():
    text = """
        - &CENTER { x: 1, y: 2 }
        - &LEFT { x: 0, y: 2 }
        - &BIG { r: 10 }
        - &SMALL { r: 1 }
        
        # All the following maps are equal:
        
        - # Explicit keys
          x: 1
          y: 2
          r: 10
          label: center/big
        
        - # Merge one map
          << : *CENTER
          r: 10
          label: center/big
        
        - # Merge multiple maps
          << : [ *CENTER, *BIG ]
          label: center/big
        
        - # Override
          << : [ *BIG, *LEFT, *SMALL ]
          x: 1
          label: center/big
    """
    data = yaml.load(text)
    assert len(data) == 8
    center, left, big, small, map1, map2, map3, map4 = data
    assert center == {"x": 1, "y": 2}
    assert left == {"x": 0, "y": 2}
    assert big == {"r": 10}
    assert small == {"r": 1}
    expected = {"x": 1, "y": 2, "r": 10, "label": "center/big"}
    assert map1 == expected
    assert map2 == expected
    assert map3 == expected
    assert map4 == expected


def test_unhashable_error_context():
    with pytest.raises(ConstructorError, match=r".*line.*column.*"):
        yaml.safe_load("{foo: bar}: baz")
