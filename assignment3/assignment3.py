import logging
import csv
import math

# One-time logger setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        # Log function name
        func_name = func.__name__

        # Positional params
        positional_params = list(args) if args else "none"

        # Keyword params
        keyword_params = dict(kwargs) if kwargs else "none"

        # Call the actual function
        result = func(*args, **kwargs)

        # Log the information
        logger.log(logging.INFO, f"function: {func_name}")
        logger.log(logging.INFO, f"positional parameters: {positional_params}")
        logger.log(logging.INFO, f"keyword parameters: {keyword_params}")
        logger.log(logging.INFO, f"return: {result}")
        logger.log(logging.INFO, "-" * 50)  # separator for readability

        return result
    return wrapper


# Function 1: No parameters, no return
@logger_decorator
def greet():
    print("Hello, World!")


# Function 2: Variable positional arguments, returns True
@logger_decorator
def check_args(*args):
    return True


# Function 3: Variable keyword arguments, returns logger_decorator
@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator


# Mainline code
if __name__ == "__main__":
    greet()
    check_args(1, 2, 3, "test")
    return_decorator(a=10, b="hello")


def type_decorator(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)  # Call the original function
            return type_of_output(x)   # Convert the result to the desired type
        return wrapper
    return decorator


# Function 1: Returns int, but we decorate to convert it to str
@type_decorator(str)
def return_int():
    return 5


# Function 2: Returns string that can't be converted to int
@type_decorator(int)
def return_string():
    return "not a number"


# Mainline
if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)  # Should print "str"

    try:
        y = return_string()
        print("shouldn't get here!")  # Won't execute if ValueError occurs
    except ValueError:
        print("can't convert that string to an integer!")  # Expected outcome

# Read CSV into a list of lists
with open("csv/employees.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)  # Each row is a list of strings

# Create a list of "first_name last_name", skipping the header
names = [row[0] + " " + row[1] for row in data[1:]]  # Skip the first row (header)
print(names)

# Create a new list with only names containing the letter "e"
names_with_e = [name for name in names if "e" in name.lower()]
print(names_with_e)



def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())

        # Build display string
        display = ""
        for ch in secret_word.lower():
            if ch in guesses:
                display += ch
            else:
                display += "_"
        print(display)

        # Check if all letters guessed
        return all(ch in guesses for ch in secret_word.lower())

    return hangman_closure


if __name__ == "__main__":
    # Prompt for secret word
    secret = input("Enter the secret word: ").strip()

    game = make_hangman(secret)

    print("\nLet's play Hangman!\n")
    while True:
        guess = input("Enter a letter: ").strip().lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Please enter a single letter.")
            continue

        if game(guess):
            print(f"🎉 Congratulations! You guessed the word '{secret}'.")
            break

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Equality check
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    # String representation
    def __str__(self):
        return f"Point({self.x}, {self.y})"

    # Euclidean distance
    def distance_to(self, other):
        if isinstance(other, Point):
            return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        raise TypeError("distance_to() requires a Point or Vector instance")


class Vector(Point):
    # Override string representation
    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"

    # Vector addition
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vector to Vector")


if __name__ == "__main__":
    # Demonstrate Point
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print("p1:", p1)
    print("p2:", p2)
    print("p1 == p2?", p1 == p2)
    print("Distance between p1 and p2:", p1.distance_to(p2))

    # Demonstrate Vector
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print("v1:", v1)
    print("v2:", v2)
    v3 = v1 + v2
    print("v1 + v2 =", v3)
    print("Distance between v1 and v3:", v1.distance_to(v3))




