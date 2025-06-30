import random

def generate_unique_random_numbers(n):
    if n < 10:
        raise ValueError("n must be at least 10 to generate 10 unique values.")
    return random.sample(range(1, n + 1), 10)

# Example usage:
n = 10  # Replace with your desired upper limit
random_numbers = generate_unique_random_numbers(n)
print(random_numbers)