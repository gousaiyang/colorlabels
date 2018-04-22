import sys
import getpass
import colorama

# Deal with Python 2 & 3 compatibility problem.
PY2 = sys.version_info[0] < 3
_input = raw_input if PY2 else input

def color_code(color_number):
    '''Generate an ANSI escape sequence with the given color number.'''
    return '\033[' + str(color_number) + 'm'

# Standard colors.
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
COLOR_RESET = color_code(0) # Reset color settings.
COLOR_NONE = '' # Does not change color.

# Default colors for each kind of label.
default_section_color = BRIGHT_MAGENTA
default_item_color = COLOR_NONE
default_success_color = BRIGHT_GREEN
default_warning_color = BRIGHT_YELLOW
default_error_color = BRIGHT_RED
default_info_color = BRIGHT_CYAN
default_progress_color = BRIGHT_CYAN
default_question_color = BRIGHT_CYAN
default_input_color = BRIGHT_CYAN
default_password_color = BRIGHT_CYAN

# Custom settings of colors for each kind of label.
custom_section_color = None
custom_item_color = None
custom_success_color = None
custom_warning_color = None
custom_error_color = None
custom_info_color = None
custom_progress_color = None
custom_question_color = None
custom_input_color = None
custom_password_color = None

# Default and custom color span settings.
#    0 -> no color
#    1 -> color the mark
#    2 -> color the header
#    3 -> color the whole line
default_color_span = 3
custom_color_span = None

# Default marks for each kind of label.
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

# Default header pattern.
header_pattern = '[%s]'

def _inline_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def _print_label(color, mark, msg, newline=True, reset=True):
    out_string = color + header_pattern % mark + ' ' + str(msg) + (COLOR_RESET if reset else COLOR_NONE)

    if newline:
        print(out_string)
    else:
        _inline_write(out_string)

def _input_label(color, mark, msg):
    _print_label(color, mark, msg, newline=False, reset=False)

    try:
        input_data = _input()
    finally:
        _inline_write(COLOR_RESET)

    return input_data

def section(msg):
    '''Display a section label.'''
    _print_label(default_section_color, default_section_mark, msg)

def item(msg):
    '''Display an item label.'''
    _print_label(default_item_color, default_item_mark, msg)

def success(msg):
    '''Display a success label.'''
    _print_label(default_success_color, default_success_mark, msg)

def warning(msg):
    '''Display a warning label.'''
    _print_label(default_warning_color, default_warning_mark, msg)

def error(msg):
    '''Display an error label.'''
    _print_label(default_error_color, default_error_mark, msg)

def info(msg):
    '''Display an info label.'''
    _print_label(default_info_color, default_info_mark, msg)

def progress(msg):
    '''Display a progress label.'''
    _print_label(default_progress_color, default_progress_mark, msg)

def question(msg):
    '''Display a question label and ask for user input.'''
    return _input_label(default_question_color, default_question_mark, msg)

def input(msg):
    '''Display an input label and ask for user input.'''
    return _input_label(default_input_color, default_input_mark, msg)

def password(msg):
    '''Display a password label and ask for user input.'''
    _print_label(default_password_color, default_password_mark, msg, newline=False)
    return getpass.getpass('')

# Initialize colorama.
colorama.init()
