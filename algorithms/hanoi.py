from .decorators import capture_recursion

@capture_recursion
def tower_of_hanoi(n, source, target, auxiliary):
    if n == 1:
        # Base case: move one disk
        return f"{source}->{target}"
    
    # Move n-1 disks from source to auxiliary
    tower_of_hanoi(n-1, source, auxiliary, target)
    # Move disk n from source to target  
    # (this move happens implicitly between the recursive calls)
    # Move n-1 disks from auxiliary to target
    tower_of_hanoi(n-1, auxiliary, target, source)
    return "Done"
