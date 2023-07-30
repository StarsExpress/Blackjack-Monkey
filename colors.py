
class Colors:
    """Text colors."""

    default = '\033[m'
    red = '\x1b[41m'
    green = '\x1b[42m'
    yellow = '\x1b[43m'


if __name__ == '__main__':
    print(Colors.red + 'Color     ' + '  ' + Colors.default)
    print(Colors.green + 'Color' + Colors.default)
