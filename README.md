# colorlabels

[![PyPI - Downloads](https://pepy.tech/badge/colorlabels)](https://pepy.tech/count/colorlabels)
[![PyPI - Version](https://img.shields.io/pypi/v/colorlabels.svg)](https://pypi.org/project/colorlabels)
[![PyPI - Format](https://img.shields.io/pypi/format/colorlabels.svg)](https://pypi.org/project/colorlabels)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colorlabels.svg)](https://pypi.org/project/colorlabels)
[![PyPI - Status](https://img.shields.io/pypi/status/colorlabels.svg)](https://pypi.org/project/colorlabels)
![License](https://img.shields.io/github/license/gousaiyang/colorlabels.svg)

`colorlabels` is a console message display library for Python. Equipped with various kinds of colorful and semantic labels, it is tailored for message display and interaction in automated scripts (e.g. test scripts, installation scripts and hacker tools).

## Demo

<p><div align="center"><img src="https://raw.githubusercontent.com/gousaiyang/colorlabels/master/img/overview.png" alt="Overview" /></div></p>
<p><div align="center"><img src="https://raw.githubusercontent.com/gousaiyang/colorlabels/master/img/animations.gif" alt="Animations" /></div></p>

```python
import time

import colorlabels as cl

cl.section('Overview of Labels')
cl.success('Good job! All test cases passed!')
cl.warning('Warning! Security update delayed!')
cl.error('Error! Failed to write file!')
cl.info('Server listening on port 8888.')
cl.progress('Downloading package, please wait...')
cl.plain('Nothing interesting.')
choice = cl.question('A new version is present, would you like to update? (Y/N)')

with cl.progress('Downloading...', mode=cl.PROGRESS_SPIN):
    time.sleep(3)

with cl.progress('Downloading ', mode=cl.PROGRESS_DETERMINATE) as p:
    time.sleep(1)
    p.update(0.5, ' 50% (2.5MB/5MB) ETA 1s')
    time.sleep(1)
    p.update(1, ' 100% (5MB/5MB)')
```

## Features

- Various kinds of labels and progress animations. Colorful and semantic.
- Easy to use.
- Customizable.
- Compatible.
  - Works on Unix-like Systems & Windows. (Based on [colorama](https://github.com/tartley/colorama))
  - Works on both Python 2 & 3 (Python 2 may not work well with unicode).

## Installation

Install with pip: `pip install -U colorlabels`

## Documentation

### Concepts

`colorlabels` mimics the famous [Bootstrap](https://getbootstrap.com/) library in Web front-end developing, providing a number of components (called **labels**) to facilitate message display and interaction in automated scripts.

#### Option Layering

In `colorlabels`, most of the configurable options are organized in three layers:

- Default settings
- Runtime global settings (using the module-level function `config()`, apply to the whole running process)
- Per-call settings (setting parameters when calling label printing functions, only apply to this function call)

Runtime global settings can override default settings, and per-call settings can override runtime global settings and default settings.

#### Label

A **label** is a line of message composed of a **header** and its **content**. A header is a **mark** with a pair of brackets.

Here is an anatomy of a label:

<p><div align="center"><img src="https://raw.githubusercontent.com/gousaiyang/colorlabels/master/img/label_anatomy.png" alt="Label Anatomy"/></div></p>

When using `colorlabels`, you will be able to customize a label's mark and color settings. However, the default settings should already look nice under most operating systems and terminals with a dark background.

`colorlabels` provides the following kinds of labels with semantic names: `section`, `item`, `success`, `warning`, `error`, `info`, `progress`, `plain`, `question`, `input` and `password`. The `section`, `item`, `success`, `warning`, `error`, `info` and `plain` labels print a message to the console. The `progress` label can alternatively display some animation. The `question`, `input` and `password` labels prompt for user input. Behaviors of all the labels can be demonstrated by running `demo.py`.

#### Mark and Color

**Marks** and **colors** are carefully selected to visually symbolize the semantic meaning of a label, which makes labels pretty and easy for visual grepping.

A mark is a non-empty string to be enclosed in a pair of brackets to comprise a header. By default all marks for labels are composed of only one character, but you can customize them to contain more than one character, or even emojis if you wish to.

If you prefer labels without headers, you can set the `show_header` option to `False` to remove them.

A color is an [ANSI escape sequence](https://en.wikipedia.org/wiki/ANSI_escape_code) representing color in terminal. `colorlabels` utilizes [`colorama`](https://github.com/tartley/colorama) to achieve cross-platform color printing compatibility. By default all colors for labels only contain the classic and ubiquitous 16 colors (code 30-37, 90-97), but you can customize them to include 8-bit colors and 24-bit colors if you wish to.

The **color_span** option specifies the range that color covers in a label. There are four values for `color_span`:

- 0: does not color any part of the label
- 1: colors only the mark
- 2: colors only the header
- 3: colors the whole label (default)

<p><div align="center"><img src="https://raw.githubusercontent.com/gousaiyang/colorlabels/master/img/color_span.png" alt="Different Color Span"/></div></p>

The default marks and colors for different kinds of labels are as follows:

| Label Type | Default Mark |    Default Color    |
|:----------:|:------------:|:-------------------:|
| `section`  |     `#`      | Bright Magenta (95) |
|   `item`   |     `*`      |      No Color       |
| `success`  |     `+`      |  Bright Green (92)  |
| `warning`  |     `!`      | Bright Yellow (93)  |
|  `error`   |     `-`      |   Bright Red (91)   |
|   `info`   |     `i`      |  Bright Cyan (96)   |
| `progress` |     `=`      |  Bright Cyan (96)   |
|  `plain`   |     `*`      |      No Color       |
| `question` |     `?`      |  Bright Cyan (96)   |
|  `input`   |     `>`      |  Bright Cyan (96)   |
| `password` |     `>`      |  Bright Cyan (96)   |

#### The Progress Label

The progress label supports different modes:

|     Progress Mode      |      Animation       | Determinate |
|:----------------------:|:--------------------:|:-----------:|
|   `PROGRESS_STATIC`    |         None         |     N/A     |
|    `PROGRESS_SPIN`     |       Spinning       |     No      |
|   `PROGRESS_EXPAND`    | Expanding Characters |     No      |
|    `PROGRESS_MOVE`     |  Moving Characters   |     No      |
| `PROGRESS_DETERMINATE` |    Progress Bar      |     Yes     |

The static progress label only prints a message without any animation, just like non-progress labels. Non-static progress labels can be classified as **determinate** and **indeterminate**. A determinate progress label has a concrete progress value (**percentage**) associated with it, and user should notify the progress label to update the percentage value (and alternatively other messages about the progress). An indeterminate progress label does not have a concrete percentage value (we cannot estimate the end of the progress), and user should notify the progress label to stop the animation when the progress ends.

For a detailed list of configurable options regarding progress labels, please refer to the corresponding content in the API Reference part of this documentation.

### API Reference

#### Module-level Functions

> **color_code**(color_number)

Generate an ANSI escape sequence with the given color number or description string.

Arguments:

- color_number: required, `any`, color number or description string

Return: `str`, an ANSI escape sequence

> **config**(**kwargs)

Set up runtime global settings.

Arguments:

- section_color: optional, `str`, runtime global settings of color for `section` labels
- item_color: optional, `str`, runtime global settings of color for `item` labels
- success_color: optional, `str`, runtime global settings of color for `success` labels
- warning_color: optional, `str`, runtime global settings of color for `warning` labels
- error_color: optional, `str`, runtime global settings of color for `error` labels
- info_color: optional, `str`, runtime global settings of color for `info` labels
- progress_color: optional, `str`, runtime global settings of color for `progress` labels
- plain_color: optional, `str`, runtime global settings of color for `plain` labels
- question_color: optional, `str`, runtime global settings of color for `question` labels
- input_color: optional, `str`, runtime global settings of color for `input` labels
- password_color: optional, `str`, runtime global settings of color for `password` labels
- section_mark: optional, `str`, runtime global settings of mark for `section` labels
- item_mark: optional, `str`, runtime global settings of mark for `item` labels
- success_mark: optional, `str`, runtime global settings of mark for `success` labels
- warning_mark: optional, `str`, runtime global settings of mark for `warning` labels
- error_mark: optional, `str`, runtime global settings of mark for `error` labels
- info_mark: optional, `str`, runtime global settings of mark for `info` labels
- progress_mark: optional, `str`, runtime global settings of mark for `progress` labels
- plain_mark: optional, `str`, runtime global settings of mark for `plain` labels
- question_mark: optional, `str`, runtime global settings of mark for `question` labels
- input_mark: optional, `str`, runtime global settings of mark for `input` labels
- password_mark: optional, `str`, runtime global settings of mark for `password` labels
- color_span: optional, `int`, runtime global settings of color span, should be in [0, 1, 2, 3]
- show_header: optional, `bool`, runtime global settings of whether to display headers for labels

Return: `None`

> **section**(msg, **kwargs)

Display a `section` label containing the given message.

Arguments:

- msg: required, `any`, the message content to display
- color: optional, `str`, the color for this label
- mark: optional, `str`, the mark for this label
- color_span: optional, `int`, the color span for this label, should be in [0, 1, 2, 3]
- show_header: optional, `bool`, whether to display header for this label

Return: `None`

> **item**(msg, **kwargs)

Display an `item` label containing the given message.

Arguments: The same as `section()`.

Return: `None`

> **success**(msg, **kwargs)

Display a `success` label containing the given message.

Arguments: The same as `section()`.

Return: `None`

> **warning**(msg, **kwargs)

Display a `warning` label containing the given message.

Arguments: The same as `section()`.

Return: `None`

> **error**(msg, **kwargs)

Display an `error` label containing the given message.

Arguments: The same as `section()`.

Return: `None`

> **info**(msg, **kwargs)

Display an `info` label containing the given message.

Arguments: The same as `section()`.

Return: `None`

> **plain**(msg, **kwargs)

Display a `plain` label containing the given message.

Arguments: The same as `section()`.

Return: `None`

> **question**(msg, **kwargs)

Display a `question` label containing the given message and prompt for user input.

Arguments: The same as `section()`.

Return: `str`, the string that user inputs

> **input**(msg, **kwargs)

Display an `input` label containing the given message and prompt for user input.

Arguments: The same as `section()`.

Return: `str`, the string that user inputs

> **password**(msg, **kwargs)

Display a `password` label containing the given message and prompt for user input. The password will not be echoed on the terminal.

Arguments: The same as `section()`.

Return: `str`, the password that user inputs

> **progress**(msg, mode=PROGRESS_STATIC, **kwargs)

Display a `progress` label containing the given message.

Arguments: Accept all arguments for `section()`. In addition:

- mode: optional, should be one of [`PROGRESS_STATIC`, `PROGRESS_SPIN`, `PROGRESS_EXPAND`, `PROGRESS_MOVE`, `PROGRESS_DETERMINATE`]
- For mode `PROGRESS_SPIN`:
  - position: optional, `str`, the position of spinner, should be one of ['mark', 'tail'], default is 'mark'
  - interval: optional, `float`, the refreshing interval (in seconds), default is 0.1
  - erase: optional, `bool`, whether to erase the whole label when animation finished, default is `False`
- For mode `PROGRESS_EXPAND`:
  - char: optional, `char`, the character to expand, default is '.'
  - width: optional, `int`, the maximum width to expand, default is 3
  - interval: optional, `float`, the refreshing interval (in seconds), default is 1
  - erase: optional, `bool`, whether to erase the whole label when animation finished, default is `False`
- For mode `PROGRESS_MOVE`:
  - char: optional, `char`, the character to move, default is '.'
  - num: optional, `int`, the number of characters to move, default is 3
  - width: optional, `int`, the width of range that characters move in, default is 12
  - style: optional, `str`, the style of moving, can be one of:
    - 'loop': when characters hit the boundary, they will appear at the other boundary in the next cycle (default)
    - 'reflect': when characters hit the boundary, they will be reflected back and alter their moving direction
  - interval: optional, `float`, the refreshing interval (in seconds), default is 0.1
  - erase: optional, `bool`, whether to erase the whole label when animation finished, default is `False`
- For mode `PROGRESS_DETERMINATE`:
  - char_done: optional, `char`, the character to represent done percentage, default is '='
  - char_head: optional, `char`, the character to display at the head of the progress bar, default is '>'
  - char_undone: optional, `char`, the character to represent undone percentage, default is ' '
  - width: optional, `int`, the width of the progress bar, default is 40
  - cleanup: optional, `bool`, whether to remove the progress bar when animation finished (original label message will remain), default is `False`
  - erase: optional, `bool`, whether to erase the whole label when animation finished, default is `False`

Return:

- For mode `PROGRESS_STATIC`, return `None`
- For other modes, return a `ProgressLabel` object

> **newline**()

Print an empty line.

Return: `None`

#### `ProgressLabel` Methods

We recommend using context managers (`with` statements) to manage progress labels with animations, as in our demo, which automatically stop the animation and clean up the side effects whether the progress normally ends or some exceptions occur. However, you may still call the `stop()` method if you want to manually stop the animation.

> **stop**()

Stop progress animation. This is automatically called by the `__exit__()` of the context manager, but you can also manually call it if you wish to.

Arguments: None

Return: `None`

> **update**(percent, text='')

Update progress to the given percentage in determinate mode. You can provide additional text to describe current status.

Arguments:

- percent: required, `float`, the percentage of the progress
- text: optional, `str`, additional text to describe current status, will be appended after the progress bar

Return: `None`
