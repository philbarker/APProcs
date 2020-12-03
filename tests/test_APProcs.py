import pytest
from approcs import AP

@pytest.fixture
def empty_AP():
    ap = AP()
    return ap

@pytest.fixture
def ap():
    ap = AP("tests/input/ap_recipe_20200821.csv")
    return ap


def test_init_empty(empty_AP):
    assert empty_AP.metadata == {}
    assert empty_AP.namespaces == {}
    assert empty_AP.statements == []
    assert empty_AP.shapes == []

def test_init(ap):
    assert empty_AP.metadata == {}
#    assert empty_AP.namespaces == {}
#    assert empty_AP.statements == []
#    assert empty_AP.shapes == []
