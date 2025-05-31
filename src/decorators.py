import functools


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result
            except Exception as e:
                error_type = type(e).__name__
                message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"
                _write_log(message, filename)
                raise
        return wrapper
    return decorator


def _write_log(message, filename):
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


if __name__ == "__main__":  # pragma: no cover
    @log(filename="mylog.txt")
    def my_function(x, y):
        return x + y

    @log()
    def fault_function(a, b):
        return a / b

    my_function(1, 2)
    fault_function(1, 0)
