from typing import Optional, Annotated

# function params


def get_full_name(first_name: str, last_name: str):
    return f"{first_name.title()}  {last_name.title()}"


def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


full_name = get_full_name('john', 'doe')

# List


def upper_case_list(list: list[str]):
    for string in list:
        return string.upper()

# Dictionaries


def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name.capitalize())
        print(item_price)


process_items({
    "banana": 12.20,
    "apple": 1.2,
})

# Union -> int | str OU Union[str, int]


def string_or_int(value: int | str):
    return value

# Optional / None -> imported on top
# Optional[Something] is a shortcut for Union[Something, None]
# Python 10 uses de | sintax, not de Union or Optional -> clearer and simpler


def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hello, {name}")
    else:
        print("Hello, stranger")


def say_hi_python10(name: str | None = None):
    if name is not None:
        print(f"Hello, {name}. Python 10 sintax!")
    else:
        print("Hello, stranger. Python 10 sintax!")


class Person:
    def __init__(self, name: str):
        self.name = name


def person_name(one_person: Person):  # must be a INSTANCE of Person
    return one_person.name.title()


person01 = Person('Stephen')
person_name(person01)


# metadata - Annotated

def func_with_metadata(name: Annotated[str, 'some metadata']):
    return name.capitalize()
