import getpass
import itertools
import platform
import sys
import threading
import time

# Deal with Python 2 & 3 compatibility problem.
PY2 = sys.version_info[0] < 3
_input = raw_input if PY2 else input
_main_thread = threading.current_thread()


def color_code(color_number):
    """Generate an ANSI escape sequence with the given color number or description string."""
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
COLOR_RESET = color_code(0)  # Reset color settings in console.
COLOR_NONE = ''  # Does not change color.
CLEAR_LINE = '\r\033[K'  # Erase all characters on the line.

# All label types.
all_labels = ('section', 'item', 'success', 'warning', 'error', 'info',
              'progress', 'plain', 'question', 'input', 'password')

# Default colors for each kind of label.
default_colors = {
    'section': BRIGHT_MAGENTA,
    'item': COLOR_NONE,
    'success': BRIGHT_GREEN,
    'warning': BRIGHT_YELLOW,
    'error': BRIGHT_RED,
    'info': BRIGHT_CYAN,
    'progress': BRIGHT_CYAN,
    'plain': COLOR_NONE,
    'question': BRIGHT_CYAN,
    'input': BRIGHT_CYAN,
    'password': BRIGHT_CYAN,
}

# Custom settings of colors for each kind of label.
custom_colors = {}
for _label_type in all_labels:
    custom_colors[_label_type] = None

# Default and custom color span settings.
#    0 -> no color
#    1 -> color the mark
#    2 -> color the header
#    3 -> color the whole line
default_color_span = 3
custom_color_span = None

# Default marks for each kind of label.
default_marks = {
    'section': '#',
    'item': '*',
    'success': '+',
    'warning': '!',
    'error': '-',
    'info': 'i',
    'progress': '=',
    'plain': '*',
    'question': '?',
    'input': '>',
    'password': '>',
}

# Custom settings of marks for each kind of label.
custom_marks = {}
for _label_type in all_labels:
    custom_marks[_label_type] = None

# Header pattern.
header_pattern = '[{mark}]'

# Default and custom header settings.
default_show_header = True
custom_show_header = None

# Modes of the progress label.
PROGRESS_STATIC = 0
PROGRESS_SPIN = 1
PROGRESS_EXPAND = 2
PROGRESS_MOVE = 3
PROGRESS_DETERMINATE = 4

# Default settings of different progress modes.
default_progress_config = {
    PROGRESS_SPIN: {
        'position': 'mark',
        'interval': 0.1,
        'erase': False
    },
    PROGRESS_EXPAND: {
        'char': '.',
        'width': 3,
        'interval': 1,
        'erase': False
    },
    PROGRESS_MOVE: {
        'char': '.',
        'num': 3,
        'width': 12,
        'style': 'loop',
        'interval': 0.1,
        'erase': False
    },
    PROGRESS_DETERMINATE: {
        'char_done': '=',
        'char_head': '>',
        'char_undone': ' ',
        'width': 40,
        'cleanup': False,
        'erase': False
    }
}


# Internal functions.

# Check whether the color is valid.
def _check_color(color):
    if not isinstance(color, str):
        raise TypeError("'color' should be a string")


# Check whether color span is valid.
def _check_color_span(color_span):
    if not isinstance(color_span, int):
        raise TypeError("'color_span' should be an integer")
    if color_span not in {0, 1, 2, 3}:
        raise ValueError("'color_span' should be one of 0, 1, 2 or 3")


# Check whether the mark is valid.
def _check_mark(mark):
    if not isinstance(mark, str):
        raise TypeError("'mark' should be a string")


# Check whether progress mode is valid.
def _check_progress_mode(mode):
    if mode not in {PROGRESS_STATIC, PROGRESS_SPIN, PROGRESS_EXPAND, PROGRESS_MOVE, PROGRESS_DETERMINATE}:
        raise ValueError('invalid progress mode')


# Check whether a value is one of the acceptable values.
def _check_value_in_list(value, field, valuelist):
    if len(valuelist) < 2:
        raise ValueError('should give at least 2 choices')
    if value not in valuelist:
        raise ValueError('{!r} should be {} or {!r}'.format(field, ', '.join(map(repr, valuelist[:-1])), valuelist[-1]))


# Check whether a value is a positive number.
def _check_positive_number(value, field):
    if not isinstance(value, (int, float)):
        raise TypeError('{!r} should be a number'.format(field))
    if value <= 0:
        raise ValueError('{!r} should be a positive number'.format(field))


# Check whether a value is a character.
def _check_character(value, field):
    if not isinstance(value, str):
        raise TypeError('{!r} should be a string'.format(field))
    if len(value) != 1:
        raise ValueError('{!r} should be one character'.format(field))


# Check whether a value is an integer not less than a given value.
def _check_interger_minimum(value, minimum, field):
    if not isinstance(value, int):
        raise TypeError('{!r} should be an integer'.format(field))
    if value < minimum:
        raise ValueError('{!r} should be at least {}'.format(field, minimum))


# Check whether a value is a valid percentage.
def _check_percent(value, field):
    if not isinstance(value, (int, float)):
        raise TypeError('{!r} should be a number'.format(field))
    if value < 0 or value > 1:
        raise ValueError('{!r} should be in range [0, 1]'.format(field))


# If parameter is present, check whether it is a string, and set config dict with the given key.
def _check_str_and_config_if_present(key, kwargs, target, target_key):
    if key in kwargs:
        value = kwargs[key]
        if not isinstance(value, str):
            raise TypeError('{!r} should be a string'.format(key))
        target[target_key] = value


# Choose the value which will take effect from a list of layered settings.
def _layered_choice(*args):
    if not args:
        raise TypeError('should give at least one choice')

    # Choose the first value which is not None.
    for arg in args:
        if arg is not None:
            return arg

    return None


# Print a string to stdout without appending '\n', and flush stdout.
def _inline_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()


# Display a generic message label.
def _print_label(color, mark, msg, newline=True, reset_color=True, clear_line=True, **kwargs):
    color_span = _layered_choice(kwargs.get('color_span'), custom_color_span, default_color_span)
    show_header = _layered_choice(kwargs.get('show_header'), custom_show_header, default_show_header)
    msg = str(msg)

    _check_color(color)
    _check_color_span(color_span)
    _check_mark(mark)

    if show_header:
        if color_span == 0:  # No color.
            out_string = header_pattern.format(mark=mark) + ' ' + msg
        elif color_span == 1:  # Color the mark.
            out_string = header_pattern.format(mark=color + mark + COLOR_RESET) + ' ' + msg
        elif color_span == 2:  # Color the header.
            out_string = color + header_pattern.format(mark=mark) + COLOR_RESET + ' ' + msg
        else:  # Color the whole line.
            out_string = color + header_pattern.format(mark=mark) + ' ' + msg \
                         + (COLOR_RESET if reset_color else COLOR_NONE)
    else:
        if color_span <= 2:
            out_string = msg
        else:
            out_string = color + msg + (COLOR_RESET if reset_color else COLOR_NONE)

    if clear_line:
        out_string = CLEAR_LINE + out_string

    if newline:
        print(out_string)
    else:
        _inline_write(out_string)


# Display a generic input label.
def _input_label(color, mark, msg, **kwargs):
    _print_label(color, mark, msg, newline=False, reset_color=False, **kwargs)
    try:
        input_data = _input()
    finally:
        _inline_write(COLOR_RESET)  # Ensure color reset.
    return input_data


# Perform the final print of a progress label.
def _progress_final(color, mark, msg, **kwargs):
    if kwargs['erase']:
        _inline_write(CLEAR_LINE)
    else:
        _print_label(color, mark, msg, **kwargs)


# Thread for progress animations in indeterminate modes.
# We should take care of clearing excessive characters.
def _progress_print_thread(label, **kwargs):
    if label.mode == PROGRESS_SPIN:
        spin_gen = itertools.cycle('-\\|/')
    elif label.mode == PROGRESS_EXPAND:
        dots_gen = itertools.cycle(range(1, kwargs['width'] + 1))
    elif label.mode == PROGRESS_MOVE:
        direction = True
        buf = kwargs['char'] * kwargs['num'] + ' ' * (kwargs['width'] - kwargs['num'])

    msg = str(label.msg)

    while not label.stopped:
        if not _main_thread.is_alive():
            return

        if label.mode == PROGRESS_SPIN:
            if kwargs['position'] == 'mark':
                _print_label(label.color, next(spin_gen), msg, newline=False, **kwargs)
            else:
                _print_label(label.color, label.mark, msg + next(spin_gen), newline=False, **kwargs)
        elif label.mode == PROGRESS_EXPAND:
            _print_label(label.color, label.mark, msg + kwargs['char'] * next(dots_gen), newline=False, **kwargs)
        elif label.mode == PROGRESS_MOVE:
            _print_label(label.color, label.mark, msg + '[' + buf + ']', newline=False, **kwargs)
            if direction:
                buf = buf[-1] + buf[:-1]
            else:
                buf = buf[1:] + buf[0]
            if kwargs['style'] == 'reflect' and kwargs['char'] in {buf[0], buf[-1]}:
                direction = not direction

        time.sleep(kwargs['interval'])

    _progress_final(label.color, label.mark, msg, **kwargs)


class ProgressLabel:
    def __init__(self, mode, color, mark, msg, **kwargs):
        config = default_progress_config[mode].copy()
        config.update(kwargs)

        if mode == PROGRESS_SPIN:
            _check_value_in_list(config['position'], 'position', ('mark', 'tail'))
            _check_positive_number(config['interval'], 'interval')
        elif mode == PROGRESS_EXPAND:
            _check_character(config['char'], 'char')
            _check_interger_minimum(config['width'], 2, 'width')
            _check_positive_number(config['interval'], 'interval')
        elif mode == PROGRESS_MOVE:
            _check_character(config['char'], 'char')
            if config['char'] == ' ':
                raise ValueError("'char' cannot be space")
            _check_interger_minimum(config['num'], 1, 'num')
            _check_interger_minimum(config['width'], 2, 'width')
            if config['num'] >= config['width']:
                raise ValueError("'num' should be less than 'width'")
            _check_value_in_list(config['style'], 'style', ('loop', 'reflect'))
            _check_positive_number(config['interval'], 'interval')
        elif mode == PROGRESS_DETERMINATE:
            _check_character(config['char_done'], 'char_done')
            _check_character(config['char_head'], 'char_head')
            _check_character(config['char_undone'], 'char_undone')
            _check_interger_minimum(config['width'], 0, 'width')

        self.mode = mode
        self.color = color
        self.mark = mark
        self.msg = msg

        if mode in {PROGRESS_SPIN, PROGRESS_EXPAND, PROGRESS_MOVE}:
            self.print_thread = threading.Thread(target=_progress_print_thread, args=(self,), kwargs=config)
            self.stopped = False
            self.print_thread.start()
        elif mode == PROGRESS_DETERMINATE:
            self.config = config
            self.update(0)

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.stop()

    def update(self, percent, text=''):
        """Update progress to the given percentage in determinate mode.
        You can provide additional text to describe current status."""

        if self.mode != PROGRESS_DETERMINATE:
            raise TypeError('cannot update progress in indeterminate mode')

        _check_percent(percent, 'percent')

        if not isinstance(text, str):
            raise TypeError("'text' should be a string")

        num_total = self.config['width']
        if num_total:
            num_done = int(round(num_total * percent))
            if num_done < num_total:
                bar = self.config['char_done'] * num_done + self.config['char_head'] + \
                      self.config['char_undone'] * (num_total - num_done - 1)
            else:
                bar = self.config['char_done'] * num_total

            bar = '[' + bar + ']'
        else:
            bar = ''

        msg = str(self.msg)
        _print_label(self.color, self.mark, msg + bar + text, newline=False, **self.config)

    def stop(self):
        """Stop progress animation."""

        if self.mode in {PROGRESS_SPIN, PROGRESS_EXPAND, PROGRESS_MOVE}:
            if not self.stopped:
                self.stopped = True
                self.print_thread.join()
        elif self.mode == PROGRESS_DETERMINATE:
            if not self.config['erase'] and not self.config['cleanup']:
                _inline_write('\n')
            else:
                _progress_final(self.color, self.mark, self.msg, **self.config)


# Public functions that users are supposed to call.

def config(**kwargs):
    """Set up runtime global settings."""

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
        _check_str_and_config_if_present(label + '_color', kwargs, custom_colors, label)

    # Label marks configuration.
    for label in all_labels:
        _check_str_and_config_if_present(label + '_mark', kwargs, custom_marks, label)


def _print_label_of_type(label_type, msg, **kwargs):
    color = _layered_choice(kwargs.pop('color', None), custom_colors[label_type], default_colors[label_type])
    mark = _layered_choice(kwargs.pop('mark', None), custom_marks[label_type], default_marks[label_type])
    _print_label(color, mark, msg, **kwargs)


def section(msg, **kwargs):
    """Display a section label containing the given message."""
    _print_label_of_type('section', msg, **kwargs)


def item(msg, **kwargs):
    """Display an item label containing the given message."""
    _print_label_of_type('item', msg, **kwargs)


def success(msg, **kwargs):
    """Display a success label containing the given message."""
    _print_label_of_type('success', msg, **kwargs)


def warning(msg, **kwargs):
    """Display a warning label containing the given message."""
    _print_label_of_type('warning', msg, **kwargs)


def error(msg, **kwargs):
    """Display an error label containing the given message."""
    _print_label_of_type('error', msg, **kwargs)


def info(msg, **kwargs):
    """Display an info label containing the given message."""
    _print_label_of_type('info', msg, **kwargs)


def progress(msg, mode=PROGRESS_STATIC, **kwargs):
    """Display a progress label containing the given message."""
    color = _layered_choice(kwargs.pop('color', None), custom_colors['progress'], default_colors['progress'])
    mark = _layered_choice(kwargs.pop('mark', None), custom_marks['progress'], default_marks['progress'])
    _check_progress_mode(mode)
    if mode == PROGRESS_STATIC:
        return _print_label(color, mark, msg, **kwargs)
    return ProgressLabel(mode, color, mark, msg, **kwargs)


def plain(msg, **kwargs):
    """Display a plain label containing the given message."""
    _print_label_of_type('plain', msg, **kwargs)


def question(msg, **kwargs):
    """Display a question label containing the given message and prompt for user input."""
    color = _layered_choice(kwargs.pop('color', None), custom_colors['question'], default_colors['question'])
    mark = _layered_choice(kwargs.pop('mark', None), custom_marks['question'], default_marks['question'])
    return _input_label(color, mark, msg, **kwargs)


def input(msg, **kwargs):
    """Display an input label containing the given message and prompt for user input."""
    color = _layered_choice(kwargs.pop('color', None), custom_colors['input'], default_colors['input'])
    mark = _layered_choice(kwargs.pop('mark', None), custom_marks['input'], default_marks['input'])
    return _input_label(color, mark, msg, **kwargs)


def password(msg, **kwargs):
    """Display a password label containing the given message and prompt for user input."""
    color = _layered_choice(kwargs.pop('color', None), custom_colors['password'], default_colors['password'])
    mark = _layered_choice(kwargs.pop('mark', None), custom_marks['password'], default_marks['password'])
    _print_label(color, mark, msg, newline=False, **kwargs)
    return getpass.getpass('')


def newline():
    """Print an empty line."""
    _inline_write('\n')


if platform.system() == 'Windows':  # Initialize colorama on Windows.
    import colorama
    colorama.init()


__all__ = ['color_code', 'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
           'BRIGHT_BLACK', 'BRIGHT_RED', 'BRIGHT_GREEN', 'BRIGHT_YELLOW', 'BRIGHT_BLUE', 'BRIGHT_MAGENTA',
           'BRIGHT_CYAN', 'BRIGHT_WHITE', 'COLOR_RESET', 'PROGRESS_STATIC', 'PROGRESS_SPIN', 'PROGRESS_EXPAND',
           'PROGRESS_MOVE', 'PROGRESS_DETERMINATE', 'config', 'section', 'item', 'success', 'warning', 'error',
           'info', 'progress', 'plain', 'question', 'input', 'password', 'newline']
