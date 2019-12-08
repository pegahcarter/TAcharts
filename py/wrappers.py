import pandas as pd


def args_to_dtype(dtype):
    ''' Convert arguments in a function to a specific data type, depending on what
        actions will be done with the arguments '''

    def format_args(fn):
        def wrapper(*args, **kwargs):
            args = [dtype(x) if type(x) != dtype else x for x in args]
            return fn(*args, **kwargs)
        return wrapper
    return format_args


def pd_series_to_numpy(fn):
    ''' Convert pandas.Series objects to numpy.array objects.  pd.Series.to_numpy() is
    10x quicker than np.array(pd.Series) '''

    def wrapper(*args, **kwargs):
        args = [pd.Series(x).to_numpy() if type(x) != pd.Series else x.to_numpy() for x in args]
        return fn(*args, **kwargs)
    return wrapper
