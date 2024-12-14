import itertools

def generate_combinations(array_length, max_ones):
    result = set()
    for num_ones in range(1, max_ones + 1):
        for indices in itertools.combinations(range(array_length), num_ones):
            array = [0] * array_length
            for index in indices:
                array[index] = 1
            result.add(tuple(array))
    return result

# Example usage
array_length = 4
max_ones = 3
combinations = generate_combinations(array_length, max_ones)
