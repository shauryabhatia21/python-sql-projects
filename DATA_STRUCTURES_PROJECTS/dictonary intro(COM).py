"""
Dictionary is another data structure in Python that stores data in
key-value pairs.
- Each key contains a corresponding value
- Keys cannot be duplicate
- Values can be duplicate
"""

a1 = {}  # will generate blank dictionary
a1 = {1: 'abc', 2: 'a1', 3: 'a2'}
# Here 1, 2, 3 are the keys
# and 'abc', 'a1', 'a2' are the values

print("Full dictionary:", a1)
print("Keys:", a1.keys())      # will give list of keys
print("Values:", a1.values())  # will give list of values
print("Items:", a1.items())    # will give both key and value pairs

for x in a1.keys():
    print('Roll no is', x)
    print('Name is', a1[x])
    print('=' * 50)

for x, y in a1.items():
    print('Roll no is', x)
    print('Name is', y)

a1[2] = 'mahima'   # if key exists, will change its value
a1[22] = 'rajeev'  # if key does not exist, will generate new key

print("Updated dictionary:", a1)
