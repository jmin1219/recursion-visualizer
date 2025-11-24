import streamlit as st
import inspect
import time
import streamlit.components.v1 as components
from algorithms import fibonacci, factorial, tower_of_hanoi, tracer
from visualizers import generate_dot
from visualizers.hanoi_viz import get_hanoi_state_at_step

st.set_page_config(page_title="Recursion Visualizer", layout="wide", page_icon="🔄", initial_sidebar_state="expanded")

# --- Educational Content ---
ALGO_INFO = {
    "Fibonacci": {
        "description": "Calculates the nth number in the Fibonacci sequence, where each number is the sum of the two preceding ones.",
        "complexity": "<b>Time:</b> O(2ⁿ) (Exponential) | <b>Space:</b> O(n) (Stack depth)",
        "insight": "Notice how the same values (e.g., fib(2)) are recalculated multiple times. This overlapping subproblems property is why dynamic programming is often preferred.",
        "func": fibonacci
    },
    "Factorial": {
        "description": "Calculates the product of all positive integers less than or equal to n.",
        "complexity": "<b>Time:</b> O(n) (Linear) | <b>Space:</b> O(n) (Stack depth)",
        "insight": "This is a linear recursion. The stack grows linearly with n until the base case (n=0) is reached, then unwinds.",
        "func": factorial
    },
    "Tower of Hanoi": {
        "description": "Moves n disks from a source rod to a target rod using an auxiliary rod, following specific rules.",
        "complexity": "<b>Time:</b> O(2ⁿ) (Exponential) | <b>Space:</b> O(n) (Stack depth)",
        "insight": "The problem is solved by moving n-1 disks to the auxiliary rod, moving the largest disk to the target, and then moving the n-1 disks from auxiliary to target.",
        "func": tower_of_hanoi
    }
}

# --- Custom CSS ---
st.markdown("""
<style>
    /* Global Typography */
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #2c3e50; }
    
    /* Graph Container */
    div[data-testid="stGraphvizChart"] {
        width: 100%;
        height: 500px;
        overflow: auto;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    div[data-testid="stGraphvizChart"] > svg { 
        max-width: 100%;
        max-height: 100%;
    }

    /* Info Boxes */
    .info-box {
        background-color: #f8f9fa;
        border-left: 5px solid #007bff;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        color: #856404;
    }

    /* Step Explanation */
    .step-explanation {
        background-color: #e8f4f8;
        border-left: 4px solid #17a2b8;
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 4px 4px 0;
        font-size: 1.05em;
    }

    /* Legend */
    .legend-box {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
        font-size: 0.9em;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Code Block - Live Execution View */
    .code-container {
        font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 0.95em;
        line-height: 1.6;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 15px;
        border-radius: 8px;
        overflow-x: hidden;
        overflow-y: auto;
        max-height: 400px;
        border: 1px solid #dee2e6;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .code-line {
        padding: 4px 8px;
        margin: 1px 0;
        border-radius: 4px;
        white-space: pre-wrap;
        word-wrap: break-word;
        transition: background-color 0.2s ease;
    }
    .highlight-line {
        background: linear-gradient(90deg, #fff3cd 0%, #fffbe6 100%);
        font-weight: 600;
        border-left: 4px solid #ff9800;
        padding-left: 12px;
        margin-left: -4px;
        box-shadow: 0 2px 4px rgba(255, 152, 0, 0.1);
        animation: pulseHighlight 0.5s ease;
    }
    @keyframes pulseHighlight {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(2px); }
    }
    .comment-line {
        background: linear-gradient(90deg, #e8f5e9 0%, #f1f8f4 100%);
        color: #1b5e20;
        font-style: italic;
        padding: 4px 8px 4px 20px;
        margin: 1px 0;
        border-left: 4px solid #4caf50;
        margin-left: -4px;
        font-size: 0.9em;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(76, 175, 80, 0.1);
    }
    .comment-line::before {
        content: "💡 ";
        margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔄 Recursion Visualizer")

# --- Sidebar ---
st.sidebar.header("⚙️ Configuration")
algo_name = st.sidebar.selectbox("Select Algorithm", list(ALGO_INFO.keys()))

# Input Parameters
n = 5
if algo_name == "Fibonacci":
    n = st.sidebar.number_input("n (0-10)", min_value=0, max_value=10, value=4)
elif algo_name == "Factorial":
    n = st.sidebar.number_input("n (0-10)", min_value=0, max_value=10, value=5)
elif algo_name == "Tower of Hanoi":
    n = st.sidebar.number_input("Disks (1-5)", min_value=1, max_value=5, value=3)

# Warnings for large inputs
if algo_name == "Fibonacci" and n > 6:
    st.sidebar.warning(f"⚠️ n={n} will generate ~{2*fibonacci(n+1)-1} calls! The graph may be large.")
elif algo_name == "Tower of Hanoi" and n > 4:
    st.sidebar.warning(f"⚠️ {n} disks will require {2**n - 1} moves. The graph will be complex.")

# Run Logic
if st.sidebar.button("▶️ Run Algorithm", type="primary", use_container_width=True):
    # JavaScript to close sidebar
    components.html(
        """
        <script>
            const doc = window.parent.document;
            const buttons = doc.querySelectorAll('button[data-testid="stSidebarCollapseButton"]');
            buttons.forEach(btn => {
                if (btn.getAttribute('aria-expanded') === 'true') {
                    btn.click();
                }
            });
        </script>
        """,
        height=0,
        width=0
    )
    with st.spinner("Running algorithm..."):
        tracer.reset()
        try:
            if algo_name == "Fibonacci":
                fibonacci(n)
            elif algo_name == "Factorial":
                factorial(n)
            elif algo_name == "Tower of Hanoi":
                tower_of_hanoi(n, "A", "C", "B")
                
            st.session_state.trace_calls = tracer.calls
            st.session_state.trace_events = tracer.events
            st.session_state.total_steps = len(tracer.events)
            st.session_state.current_step = 0 
            st.session_state.run_id = f"{algo_name}_{n}"
            time.sleep(0.5) # UX pause
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Navigation Helpers
def first_step(): st.session_state.current_step = 0
def prev_step(): st.session_state.current_step = max(0, st.session_state.current_step - 1)
def next_step(): st.session_state.current_step = min(st.session_state.total_steps, st.session_state.current_step + 1)
def last_step(): st.session_state.current_step = st.session_state.total_steps

# --- Code Highlighting Logic ---
def get_highlighted_code(func, algo_name, event=None, call_info=None):
    source = inspect.getsource(func.__wrapped__ if hasattr(func, "__wrapped__") else func)
    lines = source.split('\n')
    # Remove empty lines at end
    while lines and not lines[-1].strip():
        lines.pop()
        
    highlight_idx = -1
    comment = ""
    
    if event and call_info:
        args = call_info['args']
        n_val = args[0] if args else 0
        
        if algo_name == "Fibonacci":
            # 0: @capture_recursion
            # 1: def fibonacci(n):
            # 2:     if n <= 1:
            # 3:         return n
            # 4:     return fibonacci(n-1) + fibonacci(n-2)
            if event['type'] == 'start':
                highlight_idx = 2 # Corresponds to 'if n <= 1:'
                comment = f"  # n={n_val}, checking base case"
            elif event['type'] == 'end':
                ret_val = event['return_value']
                if n_val <= 1:
                    highlight_idx = 3 # Corresponds to 'return n'
                    comment = f"  # n={n_val}, base case! Returns {ret_val}"
                else:
                    highlight_idx = 4 # Corresponds to 'return fibonacci(n-1) + fibonacci(n-2)'
                    comment = f"  # n={n_val}, returns fib({n_val-1}) + fib({n_val-2}) = {ret_val}"
                
        elif algo_name == "Factorial":
            # 0: @capture_recursion
            # 1: def factorial(n):
            # 2:     if n == 0:
            # 3:         return 1
            # 4:     return n * factorial(n-1)
            if event['type'] == 'start':
                highlight_idx = 2 # Corresponds to 'if n == 0:'
                comment = f"  # n={n_val}, checking base case"
            elif event['type'] == 'end':
                ret_val = event['return_value']
                if n_val == 0:
                    highlight_idx = 3 # Corresponds to 'return 1'
                    comment = f"  # n=0, base case! Returns 1"
                else:
                    highlight_idx = 4 # Corresponds to 'return n * factorial(n-1)'
                    comment = f"  # n={n_val}, returns {n_val} × factorial({n_val-1}) = {ret_val}"
                
        elif algo_name == "Tower of Hanoi":
            # 0: @capture_recursion
            # 1: def tower_of_hanoi(n, source, target, auxiliary):
            # 2:     if n == 1:
            # 3:         return f"{source}->{target}"
            # 4:     
            # 5:     tower_of_hanoi(n-1, source, auxiliary, target)
            # 6:     tower_of_hanoi(n-1, auxiliary, target, source)
            # 7:     return "Done"
            if event['type'] == 'start':
                highlight_idx = 2 # Corresponds to 'if n == 1:'
                source_arg = args[1] if len(args) > 1 else "?"
                target_arg = args[2] if len(args) > 2 else "?"
                comment = f"  # n={n_val}, checking base case"
            elif event['type'] == 'end':
                ret_val = event['return_value']
                if n_val == 1:
                    highlight_idx = 3 # Corresponds to 'return f"{source}->{target}"'
                    source_arg = args[1] if len(args) > 1 else "?"
                    target_arg = args[2] if len(args) > 2 else "?"
                    comment = f"  # n=1, base case! Move disk {source_arg}→{target_arg}"
                else:
                    highlight_idx = 7 # Corresponds to 'return "Done"'
                    comment = f"  # n={n_val}, all recursive moves complete"

    # Build HTML
    html = '<div class="code-container">'
    for i, line in enumerate(lines):
        # Skip decorator if present in source
        if line.strip().startswith('@'):
            continue
            
        class_name = "code-line"
        line_content = line
        
        is_highlighted = (i == highlight_idx)
        
        html += f'<div class="{class_name}{" highlight-line" if is_highlighted else ""}">{line_content}</div>'
        
        # Add comment on a separate line if this line is highlighted
        if is_highlighted and comment:
            html += f'<div class="comment-line">{comment.strip()}</div>'
            
    html += '</div>'
    return html

# --- Main Layout ---
col_info, col_viz = st.columns([4, 6], gap="large")

with col_info:
    # 1. Algorithm Info Card
    info = ALGO_INFO[algo_name]
    st.subheader(f"📘 {algo_name}")
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Description:</strong> {info['description']}<br><br>
        {info['complexity']}
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💡 Key Insight", expanded=False):
        st.info(info['insight'])
    
    # 2. Code Display with Highlight
    st.subheader("💻 Live Code")
    
    current_event = None
    current_call = None
    if "trace_events" in st.session_state and st.session_state.current_step > 0:
        step = st.session_state.current_step
        events = st.session_state.trace_events
        calls = st.session_state.trace_calls
        current_event = events[step - 1]
        current_call = calls[current_event["call_id"]]
        
    code_html = get_highlighted_code(info['func'], algo_name, current_event, current_call)
    st.markdown(code_html, unsafe_allow_html=True)

    # 3. Current Step Explanation
    if "trace_events" in st.session_state and st.session_state.total_steps > 0:
        st.divider()
        st.subheader("⚡ Execution Flow")
        
        step = st.session_state.current_step
        total = st.session_state.total_steps
        
        # Progress Bar
        st.progress(step / total if total > 0 else 0)
        st.caption(f"Step {step} of {total}")

        if step > 0:
            # Narrative generation
            narrative = ""
            if current_event['type'] == 'start':
                narrative = f"<b>Calling</b> <code>{current_call['func_name']}{current_call['args']}</code>"
                if current_call['parent_id'] is not None:
                    parent = calls[current_call['parent_id']]
                    narrative += f"<br><br>Called by <code>{parent['func_name']}{parent['args']}</code> which is currently waiting."
                else:
                    narrative += "<br><br>This is the root call."
            elif current_event['type'] == 'end':
                narrative = f"<b>Returning</b> from <code>{current_call['func_name']}{current_call['args']}</code>"
                narrative += f"<br><br>Result: <code>{current_event['return_value']}</code>"
                if current_call['parent_id'] is not None:
                    parent = calls[current_call['parent_id']]
                    narrative += f"<br><br>Control returns to <code>{parent['func_name']}{parent['args']}</code>."

            st.markdown(f"""
            <div class="step-explanation">
                {narrative}
            </div>
            """, unsafe_allow_html=True)
            
            # Show Tower of Hanoi visual state
            if algo_name == "Tower of Hanoi":
                st.markdown("**Current State:**")
                # Get the initial n value from session state
                initial_n = st.session_state.trace_calls[0]['args'][0]
                hanoi_state = get_hanoi_state_at_step(initial_n, events, calls, step)
                st.markdown(hanoi_state.render_html(), unsafe_allow_html=True)
            
            if step == total:
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Algorithm Completed!</strong><br>
                    All recursive calls have returned.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-box">
                Click <strong>Next ⏩</strong> to start the visualization.
            </div>
            """, unsafe_allow_html=True)

    # 4. Legend
    st.markdown("""
    <div class="legend-box">
        <strong>🎨 Graph Legend</strong><br><br>
        <span style="color: #007bff; font-weight: bold;">● Blue</span> : Active Call (Running/Waiting)<br>
        <span style="color: #28a745; font-weight: bold;">● Green</span> : Completed Call (Returned)<br>
        <span style="color: #6c757d;">● White</span> : Pending Call<br>
        <span style="border: 2px solid black; padding: 0 4px; border-radius: 3px;"><b>Bold</b></span> : Current Focus
    </div>
    """, unsafe_allow_html=True)

with col_viz:
    st.subheader("🌳 Call Tree")
    
    if "trace_events" in st.session_state:
        # Navigation
        c1, c2, c3, c4, c5 = st.columns([1, 1, 4, 1, 1])
        
        # Disable logic
        is_start = st.session_state.current_step == 0
        is_end = st.session_state.current_step == st.session_state.total_steps
        
        with c1: st.button("⏮️", on_click=first_step, disabled=is_start, help="First Step", use_container_width=True)
        with c2: st.button("⏪", on_click=prev_step, disabled=is_start, help="Previous Step", use_container_width=True)
        with c3: st.slider("Timeline", 0, st.session_state.total_steps, key="current_step", label_visibility="collapsed")
        with c4: st.button("⏩", on_click=next_step, disabled=is_end, help="Next Step", use_container_width=True)
        with c5: st.button("⏭️", on_click=last_step, disabled=is_end, help="Last Step", use_container_width=True)

        # Graph
        dot = generate_dot(st.session_state.trace_calls, st.session_state.trace_events, st.session_state.current_step)
        st.graphviz_chart(dot, use_container_width=True)
        
    else:
        # Improved Empty State
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 12px; border: 1px solid #dee2e6; margin-top: 20px;">
            <h2 style="color: #2c3e50; margin-bottom: 15px;">👋 Welcome to Recursion Visualizer</h2>
            <p style="font-size: 1.1em; color: #6c757d; max-width: 600px; margin: 0 auto 30px auto;">
                Recursion can be tricky to visualize. This tool helps you build a mental model by showing the 
                <strong>call stack</strong> and <strong>execution tree</strong> in real-time.
            </p>
            <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
                <div style="background: white; padding: 15px 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <span style="font-size: 1.5em;">🔢</span><br><strong>Fibonacci</strong>
                </div>
                <div style="background: white; padding: 15px 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <span style="font-size: 1.5em;">❗</span><br><strong>Factorial</strong>
                </div>
                <div style="background: white; padding: 15px 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <span style="font-size: 1.5em;">🗼</span><br><strong>Hanoi</strong>
                </div>
            </div>
            <p style="margin-top: 30px; color: #007bff; font-weight: 500;">
                👈 Select an algorithm from the sidebar to get started!
            </p>
        </div>
        """, unsafe_allow_html=True)
