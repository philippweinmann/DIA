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

# %%
from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    @abstractmethod
    def method1(self):
        """Method that must be implemented by the subclass."""
        pass

    @abstractmethod
    def method2(self, param):
        """Another method that must be implemented by the subclass."""
        pass

    def concrete_method(self):
        """This is a concrete method that subclasses inherit."""
        print("This is a concrete method in the abstract class.")

# Example of a subclass implementing the abstract methods
class MyConcreteClass(MyAbstractClass):
    def method1(self):
        print("Method1 implemented!")

    def method2(self, param):
        print(f"Method2 implemented with param: {param}")

# Example usage
concrete_instance = MyConcreteClass()
concrete_instance.method1()  # Output: Method1 implemented!
concrete_instance.method2("Hello")  # Output: Method2 implemented with param: Hello
concrete_instance.concrete_method()  # Output: This is a concrete method in the abstract class.

# %%
