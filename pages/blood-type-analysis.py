import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Create age groups
age_bins = [0, 18, 35, 50, 65, 100]
age_labels = ["0-18", "19-35", "36-50", "51-65", "65+"]
df_healthcare['Age Group'] = pd.cut(df_healthcare['Age'], bins=age_bins, labels=age_labels, right=False)

# Graph 1: Blood Type vs Hospital (Bar Chart)
blood_type_hospital = df_healthcare.groupby(['Blood Type', 'Hospital']).size().reset_index(name='Count')

fig_blood_type_hospital = px.bar(
    blood_type_hospital,
    x='Hospital',
    y='Count',
    color='Blood Type',
    barmode='stack',
    title="Blood Type Distribution Across Hospitals"
)
fig_blood_type_hospital.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title=dict(x=0.5)
)

# Graph 2: Blood Type vs Age Group (Stacked Bar Chart)
blood_type_age = df_healthcare.groupby(['Blood Type', 'Age Group']).size().reset_index(name='Count')

fig_blood_type_age = px.bar(
    blood_type_age,
    x='Age Group',
    y='Count',
    color='Blood Type',
    barmode='stack',
    title="Age Group Distribution by Blood Type"
)
fig_blood_type_age.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title=dict(x=0.5)
)

# Graph 3: Blood Type vs Doctor (Bar Chart)
blood_type_doctor = df_healthcare.groupby(['Blood Type', 'Doctor']).size().reset_index(name='Count')

fig_blood_type_doctor = px.bar(
    blood_type_doctor,
    x='Doctor',
    y='Count',
    color='Blood Type',
    barmode='group',
    title="Blood Type Distribution by Doctor"
)
fig_blood_type_doctor.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title=dict(x=0.5)
)

# Graph 4: Blood Type Distribution (Pie Chart)
blood_type_distribution = df_healthcare['Blood Type'].value_counts().reset_index()
blood_type_distribution.columns = ['Blood Type', 'Count']

fig_blood_type_pie = px.pie(
    blood_type_distribution,
    names='Blood Type',
    values='Count',
    title="Proportion of Blood Types",
    color_discrete_sequence=px.colors.sequential.Plasma
)
fig_blood_type_pie.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title=dict(x=0.5)
)

# Graph 5: Length of Stay by Blood Type (Box Plot)
fig_blood_type_los = px.box(
    df_healthcare,
    x='Blood Type',
    y='Length of Stay (Days)',
    color='Blood Type',
    title="Length of Stay Distribution by Blood Type"
)
fig_blood_type_los.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    title=dict(x=0.5)
)

# Define Layout
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Blood Type Analysis", className="text-center", style={"color": "#1DB954"})),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_blood_type_hospital), width=12),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_blood_type_age), width=12),
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_blood_type_doctor), width=6),
                dbc.Col(dcc.Graph(figure=fig_blood_type_pie), width=6)
            ],
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_blood_type_los), width=12),
            className="mb-4"
        )
    ],
    fluid=True
)

# Register the page
dash.register_page(__name__, path="/blood-type-analysis")
