# 🔄 Recursion Visualizer

Interactive web application for visualizing recursive algorithm execution, built with Streamlit.

## Features
- **Three Algorithms**: Fibonacci, Factorial, Tower of Hanoi
- **Step-by-step Execution**: Navigate through each recursive call
- **Call Tree Visualization**: See the recursion structure with Graphviz
- **Educational Content**: Complexity analysis and algorithm insights

## Video Demo
[![Recursion Visualizer Demo](https://img.youtube.com/vi/_8Pm7Zqw6us/maxresdefault.jpg)](https://youtu.be/_8Pm7Zqw6us)
*Click the image above to watch the demo video.*


## Installation
```bash
# Clone repository
git clone https://github.com/jmin1219/recursion-visualizer.git
cd recursion-visualizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Graphviz system dependency
brew install graphviz  # macOS
# or: apt-get install graphviz  # Linux
```

## Usage
```bash
streamlit run app.py
```

## Project Structure
```
recursion_visualizer/
├── app.py              # Main Streamlit application
├── algorithms/         # Recursive algorithm implementations
│   ├── decorators.py   # Recursion tracing decorator
│   ├── fibonacci.py
│   ├── factorial.py
│   └── hanoi.py
└── visualizers/        # Graph generation
    └── call_tree.py    # Graphviz tree builder
```

## Technologies
- **Streamlit** - Web framework
- **Graphviz** - Graph visualization
- **Python 3.10+** - Core language


