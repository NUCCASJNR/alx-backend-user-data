#!/usr/bin/env python3
from typing import List, TypeVar

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def search(cls, attributes: dict = {}) -> List['Person']:
        """ Search all Person objects with matching attributes
        """
        s_class = cls.__name__

        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if getattr(obj, k) != v:
                    return False
            return True

        return list(filter(_search, DATA[s_class].values()))

# Example data (replace this with your actual data source)
DATA = {
    "Person": {
        1: Person("Alice", 30),
        2: Person("Bob", 25),
        3: Person("Charlie", 35),
        12: Person("idan", 30),
    }
}

# Using the search class method to find people with age 30
results = Person.search(attributes={"age": 30})

# Display the results
for person in results:
    print(f"Name: {person.name}, Age: {person.age}")

# Display the first result (if it exists)
if results:
    person = results[-1]
    print(f"Name: {getattr(person, 'name')}, Age: {getattr(person, 'age')}")
else:
    print("No matching person found.")
