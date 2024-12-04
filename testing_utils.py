from functools import wraps
import time

from datetime import timedelta


# decorator function to measure time taken of fct.
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        formatted_total_time = str(timedelta(seconds=total_time))
        print(f'Function {func.__name__} took {total_time:.4f} seconds to run. Formatted: {formatted_total_time}')
        return result
    return timeit_wrapper