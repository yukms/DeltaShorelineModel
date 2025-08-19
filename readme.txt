# Simple Shoreline & Sea Level Box Model

This model provides an interactive web app (using Streamlit) to simulate and visualize shoreline position changes in response to sea-level variations and sediment supply.

## Features
- **Scenario Comparison:** Compare two different shoreline evolution scenarios side-by-side.
- **Sea Level Forcing:** Combine linear and sinusoidal (short-term and long-term) sea-level changes.
- **Sediment Supply:** Adjust sediment supply (Qs) for each scenario.
- **Visualization:** View time vs. sea level, time vs. shoreline position, and shoreline position vs. sea level using interactive Plotly graphs.

## How it works
- The shoreline position is calculated using a simple box model:
  - `X = (Qs * t) / eta` (where eta is the water depth, Qs is sediment supply, t is time)
  - The model prevents division by zero or negative eta.
- Users can adjust all parameters in the web UI and instantly see the results.

## Usage
1. Install requirements: `pip install -r requirements.txt`
2. Run the app: `streamlit run simplebox.py`
3. Open the provided local URL in your browser.

---
This tool is useful for teaching, scenario exploration, and basic research on shoreline response to sea-level change.

https://shorelinemodel.streamlit.app

