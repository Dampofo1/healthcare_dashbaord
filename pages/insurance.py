import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the CSV file into a DataFrame
data = "./assets/data.csv"
df_healthcare = pd.read_csv(data)

# Preprocess data
df_healthcare['Date of Admission'] = pd.to_datetime(df_healthcare['Date of Admission'])
df_healthcare['Discharge Date'] = pd.to_datetime(df_healthcare['Discharge Date'])
df_healthcare['Length of Stay (Days)'] = (df_healthcare['Discharge Date'] - df_healthcare['Date of Admission']).dt.days
df_healthcare['Name'] = df_healthcare['Name'].str.title()
df_healthcare['Gender'] = df_healthcare['Gender'].str.capitalize()
df_healthcare['Hospital'] = df_healthcare['Hospital'].str.strip()
df_healthcare['Medical Condition'] = df_healthcare['Medical Condition'].str.capitalize()

# Create age groups
age_bins = [0, 18, 35, 50, 65, 100]
age_labels = ["0-18", "19-35", "36-50", "51-65", "65+"]
df_healthcare['Age Group'] = pd.cut(df_healthcare['Age'], bins=age_bins, labels=age_labels, right=False)

# Pie Chart: Share of admissions by insurance provider
insurance_share = df_healthcare['Insurance Provider'].value_counts().reset_index()
insurance_share.columns = ['Insurance Provider', 'Admissions']

fig_pie_insurance = px.pie(
    insurance_share,
    names='Insurance Provider',
    values='Admissions',
    title="Admissions Share by Insurance Provider",
    color_discrete_sequence=px.colors.sequential.Plasma
)
fig_pie_insurance.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white")
)

# Bar Chart: Admissions grouped by hospital and insurance provider
hospital_insurance_counts = df_healthcare.groupby(['Hospital', 'Insurance Provider']).size().reset_index(name='Admissions')

fig_bar_hospital_insurance = px.bar(
    hospital_insurance_counts,
    x='Hospital',
    y='Admissions',
    color='Insurance Provider',
    title="Admissions by Hospital and Insurance Provider",
    barmode='stack'
)
fig_bar_hospital_insurance.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white")
)

# Radar Chart: Comparing Length of Stay by Medical Condition
condition_length_of_stay = df_healthcare.groupby('Medical Condition')['Length of Stay (Days)'].mean().reset_index()

fig_radar_condition = go.Figure()

fig_radar_condition.add_trace(go.Scatterpolar(
    r=condition_length_of_stay['Length of Stay (Days)'],
    theta=condition_length_of_stay['Medical Condition'],
    fill='toself',
    name='Length of Stay',
    marker=dict(color="#1DB954")
))

fig_radar_condition.update_layout(
    polar=dict(
        radialaxis=dict(visible=True)
    ),
    showlegend=True,
    title="Average Length of Stay by Medical Condition",
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white")
)

# Bar Chart: Age group distribution grouped by insurance provider
age_insurance_counts = df_healthcare.groupby(['Age Group', 'Insurance Provider']).size().reset_index(name='Admissions')

fig_bar_age_insurance = px.bar(
    age_insurance_counts,
    x='Age Group',
    y='Admissions',
    color='Insurance Provider',
    title="Age Group Distribution by Insurance Provider",
    barmode='stack'
)
fig_bar_age_insurance.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white")
)

# Page Layout
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Insurance Analysis", className="text-center", style={"color": "#0d6efd",})),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_pie_insurance), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_bar_hospital_insurance), width=12),
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_radar_condition), width=6),
                dbc.Col(dcc.Graph(figure=fig_bar_age_insurance), width=6)
            ],
            className="mb-4"
        )
    ],
    fluid=True
)

# Register the page
dash.register_page(__name__, path="/insurance")
