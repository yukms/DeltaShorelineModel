# Simple Delta Shoreline Model

Interactive web applications for simulating and visualizing shoreline position changes in response to sea-level variations and sediment supply. Built with Streamlit for educational and research purposes.

## 🌊 Models Available

### 1. Simple Box Model (`simplebox.py`)
A basic shoreline evolution model using the fundamental box equation:
```
X(t) = Qs × t / η(t)
```
Where:
- `X(t)` = shoreline position at time t
- `Qs` = sediment supply rate
- `η(t)` = water depth (accommodation space)

### 2. Advanced Slope Model (`advancedbox.py`)
An enhanced model incorporating topset, foreset, and basement slopes for more realistic delta evolution with complex slope relationships.

## ✨ Key Features

### Interactive Controls
- **Synchronized Widgets**: Bidirectional synchronization between sliders and number inputs
- **Scenario Comparison**: Compare two different evolution scenarios side-by-side
- **Collapsible Parameters**: Organized parameter sections for cleaner interface

### Sea Level Forcing
- **Linear Trends**: Constant rate of sea-level change
- **Sinusoidal Components**: Optional short-term and long-term cyclical variations
- **Complex Scenarios**: Combine multiple forcing mechanisms

### Visualization
- **Time Series**: Sea level and shoreline position evolution over time
- **Phase Space**: Shoreline position vs. sea level relationships
- **Multi-perspective**: Three different plot views for comprehensive analysis
- **Interactive Plotly Graphs**: Zoom, pan, and hover for detailed exploration

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Models
```bash
# Simple Box Model
streamlit run simplebox.py

# Advanced Slope Model  
streamlit run advancedbox.py
```

### Online Access
- **Live Demo**: https://shorelinemodel.streamlit.app
- **Repository**: https://github.com/yukms/SimpleDeltaShorelineModel

## 📊 Default Parameters

### Simple Model
- Sediment Supply (Qs): 250
- Simulation Time: 100
- Sea Level Rate (Żdot): 0.3

### Advanced Model
- Topset Slope: 0.01
- Foreset Slope: 0.2
- Basement Slope: 0.05
- Plus all simple model parameters

## 🎓 Educational Applications

- **Coastal Geomorphology**: Understanding shoreline response to environmental changes
- **Sedimentology**: Exploring sediment transport and deposition processes
- **Climate Science**: Investigating sea-level change impacts
- **Numerical Modeling**: Learning basic box model concepts

## 🔬 Research Applications

- **Scenario Testing**: Rapid exploration of different forcing conditions
- **Parameter Sensitivity**: Understanding model response to input variations
- **Conceptual Development**: Building intuition for complex coastal systems
- **Teaching Tool**: Interactive demonstrations for students and colleagues

## 📁 Project Structure

```
SimpleDeltaShorelineModel/
├── simplebox.py          # Simple box model application
├── advancedbox.py        # Advanced slope model application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ Technical Details

- **Framework**: Streamlit for web interface
- **Computation**: NumPy for numerical calculations
- **Visualization**: Plotly for interactive graphs
- **State Management**: Session state for widget synchronization

## 📈 Model Equations

### Simple Box Model
```
X(t) = Qs × t / η(t)
```

### Advanced Slope Model
Incorporates geometric relationships between topset (St), foreset (Sf), and basement (Sb) slopes with constraint validation: `St < Sb < Sf`

---

**Developed for coastal research and education**  
*Explore shoreline dynamics through interactive modeling*
