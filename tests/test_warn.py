from warn import filterwarnings, patch
patch()
import warnings



from examples.downstream import consumer
import pytest



def test_0():


    with pytest.warns(DeprecationWarning) as record:
        warnings.simplefilter('ignore')
        filterwarnings('default', category=DeprecationWarning,
            emodule='examples.dependency')
        consumer()

    assert len(record) == 2




def test_1():


    with pytest.warns(DeprecationWarning) as records:
        warnings.simplefilter('ignore')
        print('warnings.warn is ', warnings.warn.__module__)
        print('filters', warnings.filters)
        filterwarnings('default', category=DeprecationWarning,
            emodule='examples.dependency')
        filterwarnings('ignore', category=DeprecationWarning,
            emodule='examples.dependency.bar')
        consumer()

    for r in records.list:
        print('Record :', r.message, 'In file', r.filename)
    assert len(records) == 1




