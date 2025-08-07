import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Set Streamlit page layout
st.set_page_config(layout="wide")

# File path (relative for Render deployment)
file_path = "Data 75%-rf.xlsx"  # Keep this file in the same folder as this script

# Load and clean data
df = pd.read_excel(file_path)
df.columns = [col.strip(" `") for col in df.columns]
df['Period'] = pd.to_datetime(df['Period'])

# Multiply y-axis data by 100
df['Spread_mult100'] = df['Spread'] * 100

# Horizontal lines (multiplied by 100)
lines = {
    'Average Spread: x\u0304': df['x'].iloc[0] * 100,
    'Average Spread: x\u0304 + σ': df['x + s'].iloc[0] * 100,
    'Average Spread: x\u0304 – σ': df['x – s'].iloc[0] * 100,
}

# Create figure
fig = go.Figure()

# Main line trace
fig.add_trace(go.Scatter(
    x=df['Period'],
    y=df['Spread_mult100'],
    mode='lines',
    name='Spot Spread: 75% – 25%',
    line=dict(color='blue'),
    hovertemplate='Spread: %{y:.2f}%<extra></extra>'
))

# Horizontal lines
line_styles = {
    'Average Spread: x\u0304': dict(dash='dash', width=2),
    'Average Spread: x\u0304 + σ': dict(dash='dot'),
    'Average Spread: x\u0304 – σ': dict(dash='dot'),
}

for label, y_val in lines.items():
    fig.add_trace(go.Scatter(
        x=[df['Period'].min(), df['Period'].max()],
        y=[y_val, y_val],
        mode='lines+text',
        name=label,
        line=dict(color='blue', **line_styles[label]),
        text=[label, ''],
        textposition='top right',
        hoverinfo='skip'
    ))

# Layout
fig.update_layout(
    title=dict(
        text='Estimates of the Credit Curve Spread: 75% LTV Mortgage Loans <br> Less the Riskless Rate for the Years 1996 through 1Q 2025',
        x=0.5,
        xanchor='center'
    ),
    yaxis=dict(
        title="Estimated Annual Interest Expense (k<sub>d</sub>)",
        ticks="outside",
        showgrid=True,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='LightPink',
        ticksuffix="%",
    ),
    xaxis=dict(
        tickformat='%Y',
        dtick="M24",
        hoverformat='%Y-%m-%d'
    ),
    hovermode='x unified',
    template='plotly_white',
    legend=dict(y=0.99, x=0.01),
    margin=dict(t=60, l=60, r=40, b=60),
    height=600
)

# Show in Streamlit
st.plotly_chart(fig, use_container_width=True)
