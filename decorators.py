import main


def log_debug_decorator(func):
    def wrapper(self, *args, **kwargs):
        main.logger.debug(f'Enter {func.__name__}() function')
        res = func(self, *args, **kwargs)
        return res
    return wrapper
