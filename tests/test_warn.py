from warn import filterwarnings, patch
patch()
from warnings import simplefilter
import warnings



from examples.downstream import consumer
import pytest



def test_0():

    filterwarnings('default', category=DeprecationWarning,
            emodule='examples.dependency')

    print(warnings.warn.__module__)

    with pytest.warns(DeprecationWarning) as record:
        consumer()

    assert len(record) == 2




