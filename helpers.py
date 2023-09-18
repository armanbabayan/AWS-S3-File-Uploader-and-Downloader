import time
from loguru import logger


def timer(function):
    """
    This function takes a function as an argument and
    returns the execution time of that function in seconds.
    :param function: The function to be decorated
    :return: The execution time of the function in seconds
    """
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"Finished {function.__name__!r} in {run_time: .4f} seconds")
        return result
    return wrapper_timer
