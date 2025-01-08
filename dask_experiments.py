# %%
import dask
from dask import delayed
from testing_utils import timeit
import time

# Define a simple function to square a number
def square(x):
    time.sleep(1)
    return x ** 2

@timeit
def compute_parallel():
    # Wrap each computation with dask.delayed
    delayed_results = [delayed(square)(i) for i in range(10)]

    # Compute all results in parallel
    results = dask.compute(*delayed_results)

    print("Squared Results:", results)

compute_parallel()

# %%
@timeit
def compute_sequential():
    results = [square(i) for i in range(10)]
    print("Squared Results:", results)

compute_sequential()