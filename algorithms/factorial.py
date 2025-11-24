from .decorators import capture_recursion

@capture_recursion
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
