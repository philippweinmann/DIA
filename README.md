# DIA

Reference implementation:

- Small dataset: Time=13523[13s:523ms]
- Big dataset: Time=781809[13m:1s:809ms]

Reference implementation, with Python:

- Small dataset: Time=3506221[0h:58m:26s:221ms]

# Prerequisites:

## Get the big test file (too big to push to gh)

`./setup.sh`

# execute:

`python3 test_core.py args1 args2`

args1: test file
    "0": super small test file
    "1": small test file
    "2": big test file

args2: implementation method
    "0": reference python implementation
    "1": max throughput
    "2": dask implementation

default (no args) is small test file with max throughput implementation.