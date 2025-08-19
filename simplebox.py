import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------------
# Model Function Definition
# ----------------------
def shoreline_location(Qs, eta, t):
    """Shoreline location box model (eta is calculated externally)"""
    # Ensure X=0 at t=0 and prevent division by zero or negative eta
    X = np.zeros_like(t, dtype=float)
    valid_mask = (eta > 0) & (t > 0)
    if np.any(valid_mask):
        X[valid_mask] = (Qs * t[valid_mask]) / eta[valid_mask]
    return X

# ----------------------
# UI Helper Function
# ----------------------
def create_input_widget(label, min_val, max_val, default_val, step, key, help_text=""):
    """Creates a compact widget with a label, number input, and slider."""
    st.markdown(f"**{label}**")
    if not help_text:
        help_text = f"Range: {min_val} to {max_val}"
    
    c1, c2 = st.columns([0.4, 0.6])
    with c1:
        num_input = st.number_input(
            label, min_value=min_val, max_value=max_val, value=default_val,
            step=step, key=f"{key}_num", label_visibility="collapsed", help=help_text
        )
    with c2:
        slider_val = st.slider(
            label, min_value=min_val, max_value=max_val, value=num_input,
            step=step, key=f"{key}_slider", label_visibility="collapsed"
        )
    return slider_val

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(layout="wide")
st.title("🌊 Shoreline & Sea Level Box Model: Scenario Comparison")
st.markdown("""
Create complex sea-level scenarios by combining Linear and optional Sinusoidal components.
Analyze the resulting shoreline changes from three different perspectives.
""")

# --- Input Columns ---
col1, col2 = st.columns(2)

def scenario_controls(scenario_num):
    """Creates all input controls for one scenario."""
    st.header(f"Scenario {scenario_num}")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        Qs = create_input_widget("Sediment Supply (Qs)", 10, 500, 100 if scenario_num == 1 else 120, 10, f"Qs{scenario_num}")
    with row1_col2:
        tmax = create_input_widget("Simulation Time (t)", 10, 500, 200, 10, f"tmax{scenario_num}")

    with st.expander("Sea Level Change Parameters", expanded=True):
        Z0 = create_input_widget("Initial Water Depth (Z0)", 1.0, 100.0, 10.0, 0.5, f"Z0{scenario_num}")
        Zdot = create_input_widget("Linear Rate (Zdot)", -1.0, 10.0, 2.0 if scenario_num == 1 else 2.5, 0.1, f"Zdot{scenario_num}")
        
        st.markdown("---")
        enable_s1 = st.checkbox("Enable Sinusoid 1 (Short-term)", value=False, key=f"enable_s1_{scenario_num}")
        A1, P1 = 0.0, 0
        if enable_s1:
            s1_col1, s1_col2 = st.columns(2)
            with s1_col1:
                A1 = create_input_widget("Amplitude (A1)", 0.0, 10.0, 1.0, 0.1, f"A1{scenario_num}")
            with s1_col2:
                P1 = create_input_widget("Period (P1)", 1, 100, 10, 1, f"P1{scenario_num}")

        st.markdown("---")
        enable_s2 = st.checkbox("Enable Sinusoid 2 (Long-term)", value=False, key=f"enable_s2_{scenario_num}")
        A2, P2 = 0.0, 0
        if enable_s2:
            s2_col1, s2_col2 = st.columns(2)
            with s2_col1:
                A2 = create_input_widget("Amplitude (A2)", 0.0, 50.0, 5.0, 0.5, f"A2{scenario_num}")
            with s2_col2:
                P2 = create_input_widget("Period (P2)", 50, 500, 100, 10, f"P2{scenario_num}")
            
    return Qs, tmax, Z0, Zdot, enable_s1, A1, P1, enable_s2, A2, P2

with col1:
    Qs1, tmax1, Z01, Zdot1, enable_s1_1, A1_1, P1_1, enable_s2_1, A2_1, P2_1 = scenario_controls(1)

with col2:
    Qs2, tmax2, Z02, Zdot2, enable_s1_2, A1_2, P1_2, enable_s2_2, A2_2, P2_2 = scenario_controls(2)

# --- Options ---
st.divider()
opt_col1, opt_col2 = st.columns(2)
with opt_col1:
    plot_on_single_graph = st.checkbox("Plot on a single graph", value=False)
with opt_col2:
    align_axes = st.checkbox("Unify X/Y axis ranges", value=True, disabled=plot_on_single_graph)
st.divider()

# ----------------------
# Calculation
# ----------------------
t1 = np.linspace(0, tmax1, 500)
linear1 = Zdot1 * t1
sinusoid1_1 = A1_1 * np.sin(2 * np.pi * t1 / P1_1) if enable_s1_1 and P1_1 > 0 else np.zeros_like(t1)
sinusoid2_1 = A2_1 * np.sin(2 * np.pi * t1 / P2_1) if enable_s2_1 and P2_1 > 0 else np.zeros_like(t1)
eta1 = Z01 + linear1 + sinusoid1_1 + sinusoid2_1
X1 = shoreline_location(Qs1, eta1, t1)

t2 = np.linspace(0, tmax2, 500)
linear2 = Zdot2 * t2
sinusoid1_2 = A1_2 * np.sin(2 * np.pi * t2 / P1_2) if enable_s1_2 and P1_2 > 0 else np.zeros_like(t2)
sinusoid2_2 = A2_2 * np.sin(2 * np.pi * t2 / P2_2) if enable_s2_2 and P2_2 > 0 else np.zeros_like(t2)
eta2 = Z02 + linear2 + sinusoid1_2 + sinusoid2_2
X2 = shoreline_location(Qs2, eta2, t2)

# ----------------------
# Visualization
# ----------------------
if plot_on_single_graph:
    st.header("Combined Comparison Graphs")
    # (The rest of the plotting code remains the same)
    # 1. Time vs Sea-level
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t1, y=eta1, mode='lines', name="Scenario 1", line=dict(width=4, color='mediumseagreen')))
    fig1.add_trace(go.Scatter(x=t2, y=eta2, mode='lines', name="Scenario 2", line=dict(width=4, color='darkorange')))
    fig1.update_layout(title="1. Time vs. Sea Level", xaxis_title="Time (t)", yaxis_title="Sea Level (eta)", template="plotly_white")

    # 2. Time vs Shoreline Location
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t1, y=X1, mode='lines', name="Scenario 1", line=dict(width=4, color='royalblue')))
    fig2.add_trace(go.Scatter(x=t2, y=X2, mode='lines', name="Scenario 2", line=dict(width=4, color='firebrick')))
    fig2.update_layout(title="2. Time vs. Shoreline Position", xaxis_title="Time (t)", yaxis_title="Shoreline Position (X)", template="plotly_white")

    # 3. Shoreline Location vs Sea-level
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=X1, y=eta1, mode='lines', name="Scenario 1", line=dict(width=4, color='purple')))
    fig3.add_trace(go.Scatter(x=X2, y=eta2, mode='lines', name="Scenario 2", line=dict(width=4, color='green')))
    fig3.update_layout(title="3. Shoreline Position vs. Sea Level", xaxis_title="Shoreline Position (X)", yaxis_title="Sea Level (eta)", template="plotly_white")

    # Unify axis ranges automatically
    x_max_t = max(tmax1, tmax2)
    y_max_eta = max(np.nanmax(eta1) if np.any(eta1) else 0, np.nanmax(eta2) if np.any(eta2) else 0) * 1.1
    y_min_eta = min(np.nanmin(eta1) if np.any(eta1) else 0, np.nanmin(eta2) if np.any(eta2) else 0) * 1.1
    fig1.update_xaxes(range=[0, x_max_t]); fig1.update_yaxes(range=[y_min_eta, y_max_eta])

    y_max_X = max(np.nanmax(X1) if np.any(X1) else 0, np.nanmax(X2) if np.any(X2) else 0) * 1.1
    y_min_X = min(np.nanmin(X1) if np.any(X1) else 0, np.nanmin(X2) if np.any(X2) else 0)
    if y_min_X > 0: y_min_X = 0
    fig2.update_xaxes(range=[0, x_max_t]); fig2.update_yaxes(range=[y_min_X, y_max_X])

    fig3.update_xaxes(range=[y_min_X, y_max_X]); fig3.update_yaxes(range=[y_min_eta, y_max_eta])

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

else:
    # --- Separated Graphs ---
    def create_individual_figures(t, X, eta, scenario_num):
        colors = {'shoreline': 'royalblue', 'sealevel': 'mediumseagreen', 'trajectory': 'purple'} if scenario_num == 1 else {'shoreline': 'firebrick', 'sealevel': 'darkorange', 'trajectory': 'green'}
        
        fig1 = go.Figure(go.Scatter(x=t, y=eta, mode='lines', name="Sea Level", line=dict(width=4, color=colors['sealevel'])))
        fig1.update_layout(title=f"S{scenario_num}: 1. Time vs. Sea Level", xaxis_title="Time (t)", yaxis_title="Sea Level (eta)", template="plotly_white")

        fig2 = go.Figure(go.Scatter(x=t, y=X, mode='lines', name="Shoreline", line=dict(width=4, color=colors['shoreline'])))
        fig2.update_layout(title=f"S{scenario_num}: 2. Time vs. Shoreline Position", xaxis_title="Time (t)", yaxis_title="Shoreline Position (X)", template="plotly_white")

        fig3 = go.Figure(go.Scatter(x=X, y=eta, mode='lines', name="Trajectory", line=dict(width=4, color=colors['trajectory'])))
        fig3.update_layout(title=f"S{scenario_num}: 3. Shoreline Position vs. Sea Level", xaxis_title="Shoreline Position (X)", yaxis_title="Sea Level (eta)", template="plotly_white")
        
        return fig1, fig2, fig3

    figs1 = create_individual_figures(t1, X1, eta1, 1)
    figs2 = create_individual_figures(t2, X2, eta2, 2)

    if align_axes:
        x_max_t = max(tmax1, tmax2)
        y_max_eta = max(np.nanmax(eta1) if np.any(eta1) else 0, np.nanmax(eta2) if np.any(eta2) else 0) * 1.1
        y_min_eta = min(np.nanmin(eta1) if np.any(eta1) else 0, np.nanmin(eta2) if np.any(eta2) else 0) * 1.1
        
        y_max_X = max(np.nanmax(X1) if np.any(X1) else 0, np.nanmax(X2) if np.any(X2) else 0) * 1.1
        y_min_X = min(np.nanmin(X1) if np.any(X1) else 0, np.nanmin(X2) if np.any(X2) else 0)
        if y_min_X > 0: y_min_X = 0
        
        figs1[0].update_xaxes(range=[0, x_max_t]); figs1[0].update_yaxes(range=[y_min_eta, y_max_eta])
        figs2[0].update_xaxes(range=[0, x_max_t]); figs2[0].update_yaxes(range=[y_min_eta, y_max_eta])
        
        figs1[1].update_xaxes(range=[0, x_max_t]); figs1[1].update_yaxes(range=[y_min_X, y_max_X])
        figs2[1].update_xaxes(range=[0, x_max_t]); figs2[1].update_yaxes(range=[y_min_X, y_max_X])

        figs1[2].update_xaxes(range=[y_min_X, y_max_X]); figs1[2].update_yaxes(range=[y_min_eta, y_max_eta])
        figs2[2].update_xaxes(range=[y_min_X, y_max_X]); figs2[2].update_yaxes(range=[y_min_eta, y_max_eta])

    graph_col1, graph_col2 = st.columns(2)
    with graph_col1:
        for fig in figs1: st.plotly_chart(fig, use_container_width=True)
    with graph_col2:
        for fig in figs2: st.plotly_chart(fig, use_container_width=True)