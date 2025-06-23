"""
demo_target.py
Originally an intentionally faulty script for the self-healing loop.
It now demonstrates the same functionality without triggering a runtime error.
"""

import math


def safe_divide(a: float, b: float):
    """Safely divide two numbers, returning None on division by zero."""
    try:
        return a / b
    except ZeroDivisionError:
        print("Warning: attempted division by zero. Returning None instead.")
        return None


def run() -> None:
    radius = 5
    print("Circle area:", math.pi * radius ** 2)

    # Previously caused a ZeroDivisionError; now handled safely.
    result = safe_divide(1, 0)
    if result is None:
        print("Division failed, but the script continued execution.")


if __name__ == "__main__":
    run()
