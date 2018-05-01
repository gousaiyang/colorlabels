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
COLOR_RESET = color_code(0) # Reset color settings in console.
COLOR_NONE = '' # Does not change color.

# Names of all labels.
all_labels = ('section', 'item', 'success', 'warning', 'error', 'info', 'progress', 'plain', 'question', 'input', 'password')

# Default colors for each kind of label.
default_section_color = BRIGHT_MAGENTA
default_item_color = COLOR_NONE
default_success_color = BRIGHT_GREEN
default_warning_color = BRIGHT_YELLOW
default_error_color = BRIGHT_RED
default_info_color = BRIGHT_CYAN
default_progress_color = BRIGHT_CYAN
default_plain_color = COLOR_NONE
default_question_color = BRIGHT_CYAN
default_input_color = BRIGHT_CYAN
default_password_color = BRIGHT_CYAN

# Custom settings of colors for each kind of label.
for _label_name in all_labels:
    globals()['custom_%s_color' % (_label_name)] = None

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
default_plain_mark = '*'
default_question_mark = '?'
default_input_mark = '>'
default_password_mark = '>'

# Custom settings of marks for each kind of label.
for _label_name in all_labels:
    globals()['custom_%s_mark' % (_label_name)] = None

# Header pattern.
header_pattern = '[%s]'

# Default and custom header settings.
default_show_header = True
custom_show_header = None


# Internal functions.

# Check whether the color is valid.
def _check_color(color):
    if not isinstance(color, str):
        raise TypeError("'color' should be a string")

# Check whether color span is valid.
def _check_color_span(color_span):
    if not isinstance(color_span, int):
        raise TypeError("'color_span' should be an integer")

    if color_span not in (0, 1, 2, 3):
        raise ValueError("'color_span' should be one of 0, 1, 2 or 3")

# Check whether the mark is valid.
def _check_mark(mark):
    if not isinstance(mark, str):
        raise TypeError("'mark' should be a string")

# If parameter is present, check whether it is a string, and set global config with the given key.
def _check_str_and_config_if_present(key, kwargs):
    if key in kwargs:
        value = kwargs[key]

        if not isinstance(value, str):
            raise TypeError("'%s' should be a string" % (key))

        globals()['custom_' + key] = value

# Remove a key in a dict if that key exists.
def _dict_remove_key_if_present(d, k):
    if k in d:
        d.pop(k)

# Choose the value which will take effect from a list of layered settings.
def _layered_choice(*args):
    if not args:
        raise ValueError('should give at least one choice')

    # Choose the first value which is not None.
    for arg in args:
        if arg is not None:
            return arg

    return None

# Print a string to stdout without appending '\n' and flush stdout.
def _inline_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()

# Display a generic message label.
def _print_label(color, mark, msg, newline=True, reset=True, **kwargs):
    color_span = _layered_choice(kwargs.get('color_span'), custom_color_span, default_color_span)
    show_header = _layered_choice(kwargs.get('show_header'), custom_show_header, default_show_header)
    msg = str(msg)

    _check_color(color)
    _check_color_span(color_span)
    _check_mark(mark)

    if show_header:
        if color_span == 0: # No color.
            out_string = header_pattern % mark + ' ' + msg
        elif color_span == 1: # Color the mark.
            out_string = header_pattern % (color + mark + COLOR_RESET) + ' ' + msg
        elif color_span == 2: # Color the header.
            out_string = color + header_pattern % mark + COLOR_RESET + ' ' + msg
        else: # Color the whole line.
            out_string = color + header_pattern % mark + ' ' + msg + (COLOR_RESET if reset else COLOR_NONE)
    else:
        if color_span <= 2:
            out_string = msg
        else:
            out_string = color + msg + (COLOR_RESET if reset else COLOR_NONE)

    if newline:
        print(out_string)
    else:
        _inline_write(out_string)

# Display a generic input label.
def _input_label(color, mark, msg, **kwargs):
    _print_label(color, mark, msg, newline=False, reset=False, **kwargs)

    try:
        input_data = _input()
    finally:
        _inline_write(COLOR_RESET) # Ensure color reset.

    return input_data


# Public functions that users are supposed to call.

def config(**kwargs):
    '''Set up global configuration settings.'''

    # Color span configuration.
    if 'color_span' in kwargs:
        color_span = kwargs['color_span']
        _check_color_span(color_span)
        global custom_color_span
        custom_color_span = color_span

    # Header configuration.
    if 'show_header' in kwargs:
        global custom_show_header
        custom_show_header = bool(kwargs['show_header'])

    # Label colors configuration.
    for label in all_labels:
        _check_str_and_config_if_present(label + '_color', kwargs)

    # Label marks configuration.
    for label in all_labels:
        _check_str_and_config_if_present(label + '_mark', kwargs)

def section(msg, **kwargs):
    '''Display a section label.'''

    color = _layered_choice(kwargs.get('color'), custom_section_color, default_section_color)
    mark = _layered_choice(kwargs.get('mark'), custom_section_mark, default_section_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def item(msg, **kwargs):
    '''Display an item label.'''

    color = _layered_choice(kwargs.get('color'), custom_item_color, default_item_color)
    mark = _layered_choice(kwargs.get('mark'), custom_item_mark, default_item_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def success(msg, **kwargs):
    '''Display a success label.'''

    color = _layered_choice(kwargs.get('color'), custom_success_color, default_success_color)
    mark = _layered_choice(kwargs.get('mark'), custom_success_mark, default_success_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def warning(msg, **kwargs):
    '''Display a warning label.'''

    color = _layered_choice(kwargs.get('color'), custom_warning_color, default_warning_color)
    mark = _layered_choice(kwargs.get('mark'), custom_warning_mark, default_warning_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def error(msg, **kwargs):
    '''Display an error label.'''

    color = _layered_choice(kwargs.get('color'), custom_error_color, default_error_color)
    mark = _layered_choice(kwargs.get('mark'), custom_error_mark, default_error_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def info(msg, **kwargs):
    '''Display an info label.'''

    color = _layered_choice(kwargs.get('color'), custom_info_color, default_info_color)
    mark = _layered_choice(kwargs.get('mark'), custom_info_mark, default_info_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def progress(msg, **kwargs):
    '''Display a progress label.'''

    color = _layered_choice(kwargs.get('color'), custom_progress_color, default_progress_color)
    mark = _layered_choice(kwargs.get('mark'), custom_progress_mark, default_progress_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def plain(msg, **kwargs):
    '''Display a plain label.'''

    color = _layered_choice(kwargs.get('color'), custom_plain_color, default_plain_color)
    mark = _layered_choice(kwargs.get('mark'), custom_plain_mark, default_plain_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, **kwargs)

def question(msg, **kwargs):
    '''Display a question label and ask for user input.'''

    color = _layered_choice(kwargs.get('color'), custom_question_color, default_question_color)
    mark = _layered_choice(kwargs.get('mark'), custom_question_mark, default_question_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    return _input_label(color, mark, msg, **kwargs)

def input(msg, **kwargs):
    '''Display an input label and ask for user input.'''

    color = _layered_choice(kwargs.get('color'), custom_input_color, default_input_color)
    mark = _layered_choice(kwargs.get('mark'), custom_input_mark, default_input_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    return _input_label(color, mark, msg, **kwargs)

def password(msg, **kwargs):
    '''Display a password label and ask for user input.'''

    color = _layered_choice(kwargs.get('color'), custom_password_color, default_password_color)
    mark = _layered_choice(kwargs.get('mark'), custom_password_mark, default_password_mark)
    _dict_remove_key_if_present(kwargs, 'color')
    _dict_remove_key_if_present(kwargs, 'mark')

    _print_label(color, mark, msg, newline=False, **kwargs)
    return getpass.getpass('')

# Initialize colorama.
colorama.init()
