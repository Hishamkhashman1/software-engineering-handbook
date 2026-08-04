import copy

a = [[1,2,3],[4,5]]
#b = a
#b = a.copy()
b = copy.deepcopy(a)

b[0].append(4)

#print (b)
#print (a)

def test_items(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items

# Exercise 1 — Generate Even Numbers
#
# Write a function called:
#
# generate_even(limit)
#
# Requirements:
#
# It should generate only even numbers.
# Starting from 0.
# Until limit.
# Use a generator.
# Do not return a list.
#
# I want to be able to do:
#
# for n in generate_even(10):
#     print(n)
#
# Output:
#
# 0
# 2
# 4
# 6
# 8
# 10
# Rules
# Don't Google.
# Don't worry if you don't remember yield.
# Just write what you think it should look like.
#
# When you're done, paste the code here and we'll discuss it together.
#
# Then we'll make it progressively harder:
#
# Fibonacci generator
# Read a huge log file lazily
# Simulate a paginated API
# Build a generator that streams AI responses (very close to what LLMs do)
#
def generate_even(limit):
    for n in range(limit):
        if n % 2 == 0:
            yield n

for n in generate_even(10):
    print(n)

def generate_even_numbers(limit_1):
    even_list = []

    for n in range(limit_1):
        if n % 2 == 0:
            even_list.append(n)
    return even_list

print (generate_even_numbers(10))


def decorator(func):
    def wrapper():
        print("I said hola como estas")
        print("she said")
        func()
    return wrapper

@decorator
def test_hello():
    print("こんにちは")

#test_hello()

print(test_hello)
