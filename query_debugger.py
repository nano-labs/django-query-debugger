"""Prints queries executed on you projects along with line traceback."""

from django.db.backends.utils import CursorWrapper
import inspect
from functools import wraps
from django.conf import settings
import os

TOP_DIR = os.path.abspath(os.path.join(settings.BASE_DIR, "../"))


def cprint(string, color):
    """Print a colored line."""
    color_code = {"red": 1, "gray": 0}.get(color, 0)
    print("\033[9%sm%s\033[0m" % (color_code, string))


def add_logger(func, only_here=None, everywhere=False):
    u"""Adiciona o print ao método."""
    @wraps(func)
    def logger(*args, **kwargs):
        u"""Printa de modo amigável todos os requests feitos."""
        _args = list(args)
        _sql = kwargs.get("sql") or _args[1]
        _params = kwargs.get("params") or _args[2]

        try:
            request_line = _sql % _params
        except TypeError:
            request_line = "%s %s" % (_sql, _params)

        indenting = ""
        code_point = inspect.currentframe().f_back
        tracks = []
        while len(tracks) < 10:
            code_point = code_point.f_back
            if not code_point:
                break
            _file_path = code_point.f_code.co_filename
            _file_line_number = code_point.f_lineno

            if _file_path.startswith("/") and not _file_path.startswith(TOP_DIR) and not everywhere:
                continue

            if _file_path not in [i for i, j in tracks]:
                tracks = [(_file_path, _file_line_number)] + tracks

        # if a file is specified but not present then to nothing
        if only_here and not any(p == only_here for p, l in tracks):
            return func(*args, **kwargs)

        if all(
            p.startswith("/") and not _file_path.startswith(TOP_DIR)
            for p, l in tracks
        ) and not everywhere:
            return func(*args, **kwargs)

        for a, l in tracks:
            cprint("%s%s Line: %s" % (indenting, a, l), "gray")
            indenting += "  "

        cprint("%s%s" % (indenting, request_line), "red")
        return func(*args, **kwargs)

    return logger


func = CursorWrapper._execute_with_wrappers
logged_func = add_logger(func)
setattr(CursorWrapper, "_execute_with_wrappers", logged_func)


def here():
    """Only show queries trigged by the file where this import sits."""
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    logged_func = add_logger(func, only_here=filename)
    setattr(CursorWrapper, "_execute_with_wrappers", logged_func)


def everywhere():
    """Show queries trigged by django os external libraries too."""
    logged_func = add_logger(func, everywhere=True)
    setattr(CursorWrapper, "_execute_with_wrappers", logged_func)
