import graphviz

def generate_dot(calls, events, step):
    """
    Generates a Graphviz Digraph for the recursion state at a specific step.
    
    Args:
        calls (dict): Dictionary of call_id -> call_info
        events (list): List of event dictionaries
        step (int): Number of events to process (0 to len(events))
    """
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')
    # Control graph size and responsiveness
    dot.attr(size='10,8')  # Max size in inches
    dot.attr(ratio='fill') # Fill the space
    dot.attr(dpi='70')     # Lower DPI for smaller rendering
    dot.attr(fontsize='10')

    
    # Track state
    active_calls = set()
    completed_calls = set()
    visible_calls = set()
    
    # Replay events
    current_events = events[:step]
    
    last_active_call = None
    
    for event in current_events:
        cid = event["call_id"]
        if event["type"] == "start":
            active_calls.add(cid)
            visible_calls.add(cid)
            last_active_call = cid
        elif event["type"] == "end":
            if cid in active_calls:
                active_calls.remove(cid)
            completed_calls.add(cid)
            last_active_call = cid # The one that just ended is "active" in terms of attention
            
    for cid in visible_calls:
        call = calls[cid]
        
        # Construct Label
        args_str = ", ".join([str(a) for a in call["args"]])
        # Handle kwargs if any (though our algos mostly don't use them)
        if call["kwargs"]:
            kwargs_str = ", ".join([f"{k}={v}" for k, v in call["kwargs"].items()])
            if args_str:
                args_str += ", " + kwargs_str
            else:
                args_str = kwargs_str
                
        label = f"{call['func_name']}({args_str})"
        
        # Add return value if completed AND processed as an end event
        # Note: A call is in completed_calls only if we processed its 'end' event.
        if cid in completed_calls:
            ret = call["return_value"]
            ret_str = str(ret)
            if len(ret_str) > 20:
                ret_str = ret_str[:17] + "..."
            label += f"\nReturn: {ret_str}"
            
        # Styling
        color = "black"
        style = "solid"
        fillcolor = "white"
        fontcolor = "black"
        
        if cid in completed_calls:
            color = "#28a745" # Green
            fillcolor = "#d4edda"
            style = "filled"
        elif cid in active_calls:
            color = "#007bff" # Blue
            fillcolor = "#cce5ff"
            style = "filled"
            
        # Highlight the very last event processed (focus)
        if step > 0 and cid == current_events[-1]["call_id"]:
            penwidth = "3.0"
        else:
            penwidth = "1.0"
            
        dot.node(str(cid), label=label, color=color, style=style, fillcolor=fillcolor, fontcolor=fontcolor, penwidth=penwidth)
        
        # Edge
        pid = call["parent_id"]
        if pid is not None and pid in visible_calls:
            dot.edge(str(pid), str(cid))
            
    return dot
