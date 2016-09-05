from warn import filterwarnings, patch
patch()
from warnings import simplefilter
import warnings



from examples.downstream import consumer
import pytest



def test_2():

    filterwarnings('default', category=DeprecationWarning,
            emodule='examples.dependency')

    with pytest.warns(DeprecationWarning) as record:
        consumer()

    assert len(record) == 2




def test_1():

    filterwarnings('ignore', category=DeprecationWarning,
            emodule='examples.dependency.bar')

    with pytest.warns(DeprecationWarning) as records:
        consumer()
    for r in records.list:
        print('Record :', r.message, 'In file', r.filename)
    assert len(records) == 2




