import logging
from functools import wraps

# Setup logger
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # Prepare log messages
        func_name = func.__name__
        pos_params = list(args) if args else "none"
        kw_params = dict(kwargs) if kwargs else "none"

        logger.log(logging.INFO, f"function: {func_name}")
        logger.log(logging.INFO, f"positional parameters: {pos_params}")
        logger.log(logging.INFO, f"keyword parameters: {kw_params}")
        logger.log(logging.INFO, f"return: {result}")
        logger.log(logging.INFO, "-"*50)

        return result
    return wrapper

@logger_decorator
def greet():
    print("Hello, World!")

@logger_decorator
def check_numbers(*args):
    return True

@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

# Mainline code
if __name__ == "__main__":
    greet()
    check_numbers(1, 2, 3, 4)
    return_decorator(name="Alice", role="Developer")