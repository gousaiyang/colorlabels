import sys
import getpass
import colorama

PY2 = sys.version_info[0] < 3

colorama.init()

def color_code(color_number):
    return '\033[' + str(color_number) + 'm'

BLACK = color_code(30)
RED = color_code(31)
GREEN = color_code(32)
YELLOW = color_code(33)
BLUE = color_code(34)
MAGENTA = color_code(35)
CYAN = color_code(36)
WHITE = color_code(37)
BRIGHT_BLACK = color_code(90)
BRIGHT_RED = color_code(91)
BRIGHT_GREEN = color_code(92)
BRIGHT_YELLOW = color_code(93)
BRIGHT_BLUE = color_code(94)
BRIGHT_MAGENTA = color_code(95)
BRIGHT_CYAN = color_code(96)
BRIGHT_WHITE = color_code(97)
RESET = color_code(0)

default_section_color = BRIGHT_MAGENTA
default_item_color = ''
default_success_color = BRIGHT_GREEN
default_warning_color = BRIGHT_YELLOW
default_error_color = BRIGHT_RED
default_info_color = BRIGHT_CYAN
default_progress_color = BRIGHT_CYAN
default_question_color = BRIGHT_CYAN
default_input_color = BRIGHT_CYAN
default_password_color = BRIGHT_CYAN

default_section_mark = '#'
default_item_mark = '*'
default_success_mark = '+'
default_warning_mark = '!'
default_error_mark = '-'
default_info_mark = 'i'
default_progress_mark = '='
default_question_mark = '?'
default_input_mark = '>'
default_password_mark = '>'

header_pattern = '[%s]'

_input = raw_input if PY2 else input

def _print_label(color, mark, msg, newline=True, reset=True):
    out_string = color + header_pattern % mark + ' ' + msg + (RESET if reset else '')

    if newline:
        print(out_string)
    else:
        sys.stdout.write(out_string)
        sys.stdout.flush()

def _input_label(color, mark, msg):
    _print_label(color, mark, msg, newline=False, reset=False)

    try:
        input_data = _input()
    finally:
        sys.stdout.write(RESET)
        sys.stdout.flush()

    return input_data

def section(msg):
    _print_label(default_section_color, default_section_mark, msg)

def item(msg):
    _print_label(default_item_color, default_item_mark, msg)

def success(msg):
    _print_label(default_success_color, default_success_mark, msg)

def warning(msg):
    _print_label(default_warning_color, default_warning_mark, msg)

def error(msg):
    _print_label(default_error_color, default_error_mark, msg)

def info(msg):
    _print_label(default_info_color, default_info_mark, msg)

def progress(msg):
    _print_label(default_progress_color, default_progress_mark, msg)

def question(msg):
    return _input_label(default_question_color, default_question_mark, msg)

def input(msg):
    return _input_label(default_input_color, default_input_mark, msg)

def password(msg):
    _print_label(default_password_color, default_password_mark, msg, newline=False)
    return getpass.getpass('')
