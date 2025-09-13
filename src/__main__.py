"""Bot Entry Point"""

from asyncio import run
import sys

from src.main import main

if __name__ == '__main__':
    # Only use uvloop on non-Windows systems
    if sys.platform != 'win32':
        try:
            import uvloop
            uvloop.install()
        except ImportError:
            pass
    run(main())
