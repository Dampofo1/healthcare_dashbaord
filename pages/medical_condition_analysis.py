import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import numpy as np

# Load the dataset
data = "./assets/data.csv"
df_healthcare = pd.read_csv(data)

# Preprocess the dataset
df_healthcare['Date of Admission'] = pd.to_datetime(df_healthcare['Date of Admission'])
df_healthcare['Discharge Date'] = pd.to_datetime(df_healthcare['Discharge Date'])
df_healthcare['Length of Stay (Days)'] = (df_healthcare['Discharge Date'] - df_healthcare['Date of Admission']).dt.days
df_healthcare['Name'] = df_healthcare['Name'].str.title()
df_healthcare['Gender'] = df_healthcare['Gender'].str.capitalize()
df_healthcare['Hospital'] = df_healthcare['Hospital'].str.strip()
df_healthcare['Medical Condition'] = df_healthcare['Medical Condition'].str.capitalize()

# Graph 1: Treemap of Medical Conditions by Hospital
fig_treemap_conditions = px.treemap(
    df_healthcare,
    path=['Hospital', 'Medical Condition'],
    values='Billing Amount',
    title="Treemap of Medical Conditions by Hospital",
    color='Length of Stay (Days)',
    color_continuous_scale='Viridis'
)
fig_treemap_conditions.update_layout(
    paper_bgcolor="black",
    font=dict(color="white"),
    title_font=dict(size=16),
    margin=dict(t=50, l=10, r=10, b=10)
)

# Graph 2: Bubble Chart of Billing Amount vs Length of Stay by Medical Condition
condition_bubble_data = df_healthcare.groupby('Medical Condition').agg(
    {'Billing Amount': 'sum', 'Length of Stay (Days)': 'mean', 'Name': 'count'}).reset_index()
condition_bubble_data.rename(columns={'Name': 'Number of Patients'}, inplace=True)

fig_bubble_conditions = px.scatter(
    condition_bubble_data,
    x='Length of Stay (Days)',
    y='Billing Amount',
    size='Number of Patients',
    color='Medical Condition',
    title="Billing Amount vs Length of Stay by Medical Condition",
    size_max=50,
    hover_data={'Medical Condition': True, 'Number of Patients': True, 'Billing Amount': ':.2f'}
)
fig_bubble_conditions.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title_font=dict(size=16),
    margin=dict(t=50, l=10, r=10, b=10)
)

# Replace negative billing amounts with NaN or filter them out
df_healthcare = df_healthcare[df_healthcare['Billing Amount'] >= 0]

# Graph 3: Timeline of Admissions by Medical Condition
fig_timeline_conditions = px.scatter(
    df_healthcare,
    x='Date of Admission',
    y='Medical Condition',
    color='Medical Condition',
    size='Billing Amount',  # Marker size
    title="Timeline of Admissions by Medical Condition",
    hover_data={'Date of Admission': True, 'Medical Condition': True, 'Billing Amount': ':.2f'}
)

fig_timeline_conditions.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title_font=dict(size=16),
    margin=dict(t=50, l=10, r=10, b=10)
)


# Graph 4: Correlation Heatmap

df_healthcare['Medical Condition'] = pd.factorize(df_healthcare['Medical Condition'])[0]


correlation_data = df_healthcare[['Age', 'Billing Amount', 'Length of Stay (Days)', 'Medical Condition']].corr()

fig_correlation_heatmap = go.Figure(
    data=go.Heatmap(
        z=correlation_data.values,
        x=correlation_data.columns,
        y=correlation_data.columns,
        colorscale='Viridis',
        colorbar=dict(title="Correlation")
    )
)
fig_correlation_heatmap.update_layout(
    title="Correlation Heatmap of Numerical Variables",
    xaxis=dict(tickangle=45),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title_font=dict(size=16),
    margin=dict(t=50, l=10, r=10, b=10)
)

# Define Layout
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Medical Condition Analysis", className="text-center", style={"color": "#0d6efd",})),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_treemap_conditions), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_bubble_conditions), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_timeline_conditions), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_correlation_heatmap), width=12),
            className="mb-4"
        )
    ],
    fluid=True
)

# Register the page
dash.register_page(__name__, path="/medical_condition_analysis")
