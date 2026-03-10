"""Cross-platform colour handling for terminal output"""

import sys

# Try to use colorama for Windows support
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback to manual ANSI enabling on Windows
    if sys.platform.startswith("win"):
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                new_mode = mode.value | 0x0004
                kernel32.SetConsoleMode(h, new_mode)
        except Exception:
            pass

    # Define ANSI colour codes
    class _Fore:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[39m'

    class _Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'
        RESET_ALL = '\033[0m'

    Fore = _Fore()
    Style = _Style()

    # Print warning only once
    print("Note: Install 'colorama' for better Windows support: pip install colorama")


def init_colours():
    """Initialize colour support (call at program start)"""
    # This function exists to ensure colours are initialized
    # colorama.init() is already called in the import try block
    pass