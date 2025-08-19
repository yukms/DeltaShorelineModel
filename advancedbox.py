import streamlit as st
import numpy as np
import plotly.graph_objects as go

def shoreline_location_advanced(q_s, eta, t, S_t, S_f, S_b):
    """Advanced shoreline location model with topset, foreset, basement slopes"""
    # Ensure s=0 at t=0 and prevent division by zero or negative eta
    s = np.zeros_like(t, dtype=float)
    valid_mask = (eta > 0) & (t > 0)
    
    # Prevent invalid slope relationships
    if S_t <= 0 or S_b <= 0 or S_f <= 0 or not (S_t < S_b < S_f):
        return np.full_like(t, np.nan)
    
    if np.any(valid_mask):
        alpha = S_t / (S_b - S_t)
        beta = S_f / (S_f - S_b)
        denom = S_b * (alpha + beta)
        
        with np.errstate(invalid='ignore', divide='ignore'):
            sqrt_arg = (2 * q_s * t[valid_mask]) / denom
            sqrt_arg = np.where(sqrt_arg < 0, 0, sqrt_arg)
            s[valid_mask] = -eta[valid_mask] / S_b + np.sqrt(sqrt_arg)
    
    return s

# ----------------------
# UI Helper Function
# ----------------------
def create_input_widget(label, min_val, max_val, default_val, step, key, help_text=""):
    """Creates a compact widget with synchronized slider and number input using session state."""
    st.markdown(f"**{label}**")
    if not help_text:
        help_text = f"Range: {min_val} to {max_val}"
    
    # Initialize session state
    if f"{key}_value" not in st.session_state:
        st.session_state[f"{key}_value"] = default_val
    
    # Slider updates session state
    slider_val = st.slider(
        label, min_value=min_val, max_value=max_val, value=st.session_state[f"{key}_value"],
        step=step, key=f"{key}_slider", label_visibility="collapsed", help=help_text,
        on_change=lambda: setattr(st.session_state, f"{key}_value", st.session_state[f"{key}_slider"])
    )
    
    # Number input updates session state
    num_input = st.number_input(
        label, min_value=min_val, max_value=max_val, value=st.session_state[f"{key}_value"],
        step=step, key=f"{key}_num", label_visibility="collapsed", help=help_text,
        on_change=lambda: setattr(st.session_state, f"{key}_value", st.session_state[f"{key}_num"])
    )
    
    return st.session_state[f"{key}_value"]

st.set_page_config(layout="wide")
st.title("🏔️ Advanced Shoreline Model: Scenario Comparison with Slopes")
st.markdown(r"""
This model uses the following equation with topset, foreset, and basement slopes:

$$
s(t) = -\frac{\eta}{S_b} + \sqrt{\frac{2q_s t}{S_b (\alpha+\beta)}}
$$

where

$$
\alpha = \frac{S_t}{S_b - S_t}
$$

$$
\beta = \frac{S_f}{S_f - S_b}
$$

- $S_t$: topset slope  
- $S_f$: foreset slope  
- $S_b$: basement slope  
- $q_s$: sediment supply  
- $\eta$: water depth (varies with time)
- $t$: time

Create complex sea-level scenarios by combining Linear and optional Sinusoidal components.
Analyze the resulting shoreline changes from three different perspectives.
""")

# --- Input Columns ---
col1, col2 = st.columns(2)

def scenario_controls(scenario_num):
    """Creates all input controls for one scenario."""
    st.header(f"Scenario {scenario_num}")
    # Avoid nested columns: just show widgets sequentially
    q_s = create_input_widget("Sediment Supply ($q_s$)", 10, 500, 250 if scenario_num == 1 else 250, 10, f"qs{scenario_num}")
    tmax = create_input_widget("Simulation Time ($t$)", 10, 500, 100, 10, f"tmax{scenario_num}")
    
    with st.expander("Slope Parameters", expanded=False):
        S_t = create_input_widget("Topset Slope ($S_t$)", 0.001, 0.1, 0.01 if scenario_num == 1 else 0.01, 0.001, f"St{scenario_num}")
        S_f = create_input_widget("Foreset Slope ($S_f$)", 0.01, 1.0, 0.1 if scenario_num == 1 else 0.1, 0.01, f"Sf{scenario_num}")
        S_b = create_input_widget("Basement Slope ($S_b$)", 0.001, 0.1, 0.05 if scenario_num == 1 else 0.05, 0.001, f"Sb{scenario_num}")

    with st.expander("Sea Level Change Parameters", expanded=False):
        Z0 = create_input_widget("Initial Water Depth ($Z_0$)", 1.0, 100.0, 1.0, 0.5, f"Z0{scenario_num}")
        Zdot = create_input_widget("Linear Rate ($\dot{Z}$)", -1.0, 10.0, 0.3 if scenario_num == 1 else 0.3, 0.1, f"Zdot{scenario_num}")
        st.markdown("---")
        enable_s1 = st.checkbox("Enable Sinusoid 1 (Short-term)", value=False, key=f"enable_s1_{scenario_num}")
        A1, P1 = 0.0, 0
        if enable_s1:
            A1 = create_input_widget("Amplitude ($A_1$)", 0.0, 10.0, 1.0, 0.1, f"A1{scenario_num}")
            P1 = create_input_widget("Period ($P_1$)", 1, 100, 10, 1, f"P1{scenario_num}")
        st.markdown("---")
        enable_s2 = st.checkbox("Enable Sinusoid 2 (Long-term)", value=False, key=f"enable_s2_{scenario_num}")
        A2, P2 = 0.0, 0
        if enable_s2:
            A2 = create_input_widget("Amplitude ($A_2$)", 0.0, 50.0, 5.0, 0.5, f"A2{scenario_num}")
            P2 = create_input_widget("Period ($P_2$)", 50, 500, 100, 10, f"P2{scenario_num}")
    return q_s, tmax, S_t, S_f, S_b, Z0, Zdot, enable_s1, A1, P1, enable_s2, A2, P2

with col1:
    q_s1, tmax1, S_t1, S_f1, S_b1, Z01, Zdot1, enable_s1_1, A1_1, P1_1, enable_s2_1, A2_1, P2_1 = scenario_controls(1)

with col2:
    q_s2, tmax2, S_t2, S_f2, S_b2, Z02, Zdot2, enable_s1_2, A1_2, P1_2, enable_s2_2, A2_2, P2_2 = scenario_controls(2)

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
s1 = shoreline_location_advanced(q_s1, eta1, t1, S_t1, S_f1, S_b1)

t2 = np.linspace(0, tmax2, 500)
linear2 = Zdot2 * t2
sinusoid1_2 = A1_2 * np.sin(2 * np.pi * t2 / P1_2) if enable_s1_2 and P1_2 > 0 else np.zeros_like(t2)
sinusoid2_2 = A2_2 * np.sin(2 * np.pi * t2 / P2_2) if enable_s2_2 and P2_2 > 0 else np.zeros_like(t2)
eta2 = Z02 + linear2 + sinusoid1_2 + sinusoid2_2
s2 = shoreline_location_advanced(q_s2, eta2, t2, S_t2, S_f2, S_b2)

# Warn user if input is invalid for either scenario
invalid1 = S_t1 <= 0 or S_b1 <= 0 or S_f1 <= 0 or not (S_t1 < S_b1 < S_f1)
invalid2 = S_t2 <= 0 or S_b2 <= 0 or S_f2 <= 0 or not (S_t2 < S_b2 < S_f2)

if invalid1:
    st.error(r"Scenario 1 - Invalid input: $S_t < S_b < S_f$ and all must be positive.")
if invalid2:
    st.error(r"Scenario 2 - Invalid input: $S_t < S_b < S_f$ and all must be positive.")

# ----------------------
# Visualization
# ----------------------
if plot_on_single_graph and not (invalid1 or invalid2):
    st.header("Combined Comparison Graphs")
    # 1. Time vs Sea-level
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t1, y=eta1, mode='lines', name="Scenario 1", line=dict(width=4, color='mediumseagreen')))
    fig1.add_trace(go.Scatter(x=t2, y=eta2, mode='lines', name="Scenario 2", line=dict(width=4, color='darkorange')))
    fig1.update_layout(title="1. Time vs. Sea Level", xaxis_title="Time (t)", yaxis_title="Sea Level (η)", template="plotly_white")

    # 2. Time vs Shoreline Location
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t1, y=s1, mode='lines', name="Scenario 1", line=dict(width=4, color='royalblue')))
    fig2.add_trace(go.Scatter(x=t2, y=s2, mode='lines', name="Scenario 2", line=dict(width=4, color='firebrick')))
    fig2.update_layout(title="2. Time vs. Shoreline Position", xaxis_title="Time (t)", yaxis_title="Shoreline Position (s)", template="plotly_white")

    # 3. Shoreline Location vs Sea-level
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=s1, y=eta1, mode='lines', name="Scenario 1", line=dict(width=4, color='purple')))
    fig3.add_trace(go.Scatter(x=s2, y=eta2, mode='lines', name="Scenario 2", line=dict(width=4, color='green')))
    fig3.update_layout(title="3. Shoreline Position vs. Sea Level", xaxis_title="Shoreline Position (s)", yaxis_title="Sea Level (η)", template="plotly_white")

    # Unify axis ranges automatically
    x_max_t = max(tmax1, tmax2)
    y_max_eta = max(np.nanmax(eta1) if np.any(eta1) else 0, np.nanmax(eta2) if np.any(eta2) else 0) * 1.1
    y_min_eta = min(np.nanmin(eta1) if np.any(eta1) else 0, np.nanmin(eta2) if np.any(eta2) else 0) * 1.1
    fig1.update_xaxes(range=[0, x_max_t]); fig1.update_yaxes(range=[y_min_eta, y_max_eta])

    y_max_s = max(np.nanmax(s1) if np.any(s1) else 0, np.nanmax(s2) if np.any(s2) else 0) * 1.1
    y_min_s = min(np.nanmin(s1) if np.any(s1) else 0, np.nanmin(s2) if np.any(s2) else 0)
    if y_min_s > 0: y_min_s = 0
    fig2.update_xaxes(range=[0, x_max_t]); fig2.update_yaxes(range=[y_min_s, y_max_s])

    fig3.update_xaxes(range=[y_min_s, y_max_s]); fig3.update_yaxes(range=[y_min_eta, y_max_eta])

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

elif not (invalid1 or invalid2):
    # --- Separated Graphs ---
    def create_individual_figures(t, s, eta, scenario_num):
        colors = {'shoreline': 'royalblue', 'sealevel': 'mediumseagreen', 'trajectory': 'purple'} if scenario_num == 1 else {'shoreline': 'firebrick', 'sealevel': 'darkorange', 'trajectory': 'green'}
        
        fig1 = go.Figure(go.Scatter(x=t, y=eta, mode='lines', name="Sea Level", line=dict(width=4, color=colors['sealevel'])))
        fig1.update_layout(title=f"S{scenario_num}: 1. Time vs. Sea Level", xaxis_title="Time (t)", yaxis_title="Sea Level (η)", template="plotly_white")

        fig2 = go.Figure(go.Scatter(x=t, y=s, mode='lines', name="Shoreline", line=dict(width=4, color=colors['shoreline'])))
        fig2.update_layout(title=f"S{scenario_num}: 2. Time vs. Shoreline Position", xaxis_title="Time (t)", yaxis_title="Shoreline Position (s)", template="plotly_white")

        fig3 = go.Figure(go.Scatter(x=s, y=eta, mode='lines', name="Trajectory", line=dict(width=4, color=colors['trajectory'])))
        fig3.update_layout(title=f"S{scenario_num}: 3. Shoreline Position vs. Sea Level", xaxis_title="Shoreline Position (s)", yaxis_title="Sea Level (η)", template="plotly_white")
        
        return fig1, fig2, fig3

    figs1 = create_individual_figures(t1, s1, eta1, 1)
    figs2 = create_individual_figures(t2, s2, eta2, 2)

    if align_axes:
        x_max_t = max(tmax1, tmax2)
        y_max_eta = max(np.nanmax(eta1) if np.any(eta1) else 0, np.nanmax(eta2) if np.any(eta2) else 0) * 1.1
        y_min_eta = min(np.nanmin(eta1) if np.any(eta1) else 0, np.nanmin(eta2) if np.any(eta2) else 0) * 1.1
        
        y_max_s = max(np.nanmax(s1) if np.any(s1) else 0, np.nanmax(s2) if np.any(s2) else 0) * 1.1
        y_min_s = min(np.nanmin(s1) if np.any(s1) else 0, np.nanmin(s2) if np.any(s2) else 0)
        if y_min_s > 0: y_min_s = 0
        
        figs1[0].update_xaxes(range=[0, x_max_t]); figs1[0].update_yaxes(range=[y_min_eta, y_max_eta])
        figs2[0].update_xaxes(range=[0, x_max_t]); figs2[0].update_yaxes(range=[y_min_eta, y_max_eta])
        
        figs1[1].update_xaxes(range=[0, x_max_t]); figs1[1].update_yaxes(range=[y_min_s, y_max_s])
        figs2[1].update_xaxes(range=[0, x_max_t]); figs2[1].update_yaxes(range=[y_min_s, y_max_s])

        figs1[2].update_xaxes(range=[y_min_s, y_max_s]); figs1[2].update_yaxes(range=[y_min_eta, y_max_eta])
        figs2[2].update_xaxes(range=[y_min_s, y_max_s]); figs2[2].update_yaxes(range=[y_min_eta, y_max_eta])

    graph_col1, graph_col2 = st.columns(2)
    with graph_col1:
        for fig in figs1: st.plotly_chart(fig, use_container_width=True)
    with graph_col2:
        for fig in figs2: st.plotly_chart(fig, use_container_width=True)
