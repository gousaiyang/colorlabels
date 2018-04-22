# colorlabels

![](img/overview.png)

```python
import colorlabels as cl

cl.section('Overview of Labels')
cl.success('Good job! All test cases passed!')
cl.warning('Warning! Security update delayed!')
cl.error('Error! Failed to write file!')
cl.info('Server listening on port 8888.')
cl.progress('Downloading package, please wait...')
choice = cl.question('A new version is present, would you like to update? (Y/N)')
```

## Features

- Provides semantic and colorful labels in console. (Inspired by [@UltimateHackers](https://github.com/UltimateHackers))
- Designed for message display and interaction in automated scripts (e.g. test scripts, installation scripts and hacker tools).
- Easy to use.
- Compatible. (Based on [colorama](https://github.com/tartley/colorama))
  - Windows & Unix-like Systems
  - Python 2 & 3

## Installation

```
pip install colorlabels
```

NOTE: This project is currently under construction.

TODO:

- [ ] Various kinds of progress animation.
- [ ] To be more customizable.
