import functools

class RecursionTrace:
    def __init__(self):
        self.calls = {}  # Map call_id -> call_info
        self.events = [] # List of events (start/end)
        self.call_stack = []
        self.next_id = 0

    def reset(self):
        self.calls = {}
        self.events = []
        self.call_stack = []
        self.next_id = 0

    def start_call(self, func_name, args, kwargs):
        call_id = self.next_id
        self.next_id += 1
        parent_id = self.call_stack[-1] if self.call_stack else None
        
        call_info = {
            "id": call_id,
            "parent_id": parent_id,
            "func_name": func_name,
            "args": args,
            "kwargs": kwargs,
            "return_value": None,
            "status": "running"
        }
        self.calls[call_id] = call_info
        self.call_stack.append(call_id)
        
        self.events.append({
            "type": "start",
            "call_id": call_id
        })
        return call_id

    def end_call(self, return_value):
        if not self.call_stack:
            return
        
        call_id = self.call_stack.pop()
        if call_id in self.calls:
            self.calls[call_id]["return_value"] = return_value
            self.calls[call_id]["status"] = "completed"
            
            self.events.append({
                "type": "end",
                "call_id": call_id,
                "return_value": return_value
            })

# Global tracer instance
tracer = RecursionTrace()

def capture_recursion(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracer.start_call(func.__name__, args, kwargs)
        try:
            result = func(*args, **kwargs)
            tracer.end_call(result)
            return result
        except Exception as e:
            tracer.end_call(f"Error: {str(e)}")
            raise e
    return wrapper
