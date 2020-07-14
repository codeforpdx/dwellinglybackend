from pytest import fixture

def dummy_test(x):
    return x.capitalize()

def test_dummy_test():
    assert dummy_test('dwellingly') == 'Dwellingly'