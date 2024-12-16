import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
import pandas as pd
import plotly.graph_objects as go

# Load and preprocess the updated dataset
# data = [
#     ["Bobby Jackson", 30, "Male", "B-", "Cancer", "2024-01-31", "Matthew Smith", "Sons and Miller", "Blue Cross", 18856.28, 328, "Urgent", "2024-02-02", "Paracetamol", "Normal"],
#     ["Leslie Terry", 62, "Male", "A+", "Obesity", "2019-08-20", "Samantha Davies", "Kim Inc", "Medicare", 33643.33, 265, "Emergency", "2019-08-26", "Ibuprofen", "Inconclusive"],
#     ["Danny Smith", 76, "Female", "A-", "Obesity", "2022-09-22", "Tiffany Mitchell", "Cook PLC", "Aetna", 27955.10, 205, "Emergency", "2022-10-07", "Aspirin", "Normal"],
#     ["Andrew Watts", 28, "Female", "O+", "Diabetes", "2020-11-18", "Kevin Wells", "Hernandez Rogers and Vang,", "Medicare", 37909.78, 450, "Elective", "2020-12-18", "Ibuprofen", "Abnormal"],
#     ["Adrienne Bell", 43, "Female", "AB+", "Cancer", "2022-09-19", "Kathleen Hanna", "White-White", "Aetna", 14238.32, 458, "Urgent", "2022-10-09", "Penicillin", "Abnormal"],
#     ["Emily Johnson", 36, "Male", "A+", "Asthma", "2023-12-20", "Taylor Newton", "Nunez-Humphrey", "UnitedHealthcare", 48145.11, 389, "Urgent", "2023-12-24", "Ibuprofen", "Normal"],
#     ["Edward Edwards", 21, "Female", "AB-", "Diabetes", "2020-11-03", "Kelly Olson", "Group Middleton", "Medicare", 19580.87, 389, "Emergency", "2020-11-15", "Paracetamol", "Inconclusive"],
#     ["Christina Martinez", 20, "Female", "A+", "Cancer", "2021-12-28", "Suzanne Thomas", "Powell Robinson and Valdez,", "Cigna", 45820.46, 277, "Emergency", "2022-01-07", "Paracetamol", "Inconclusive"]
# ]
# data = "./assets/healthcare.csv"

# columns = ["Name", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission", "Doctor", "Hospital", 
#            "Insurance Provider", "Billing Amount", "Room Number", "Admission Type", "Discharge Date", "Medication", 
#            "Test Results"]

# Specify the file path
data = "./assets/data.csv"

# Load the CSV file into a DataFrame
df_healthcare = pd.read_csv(data)

# Preprocess data
df_healthcare['Date of Admission'] = pd.to_datetime(df_healthcare['Date of Admission'])
df_healthcare['Discharge Date'] = pd.to_datetime(df_healthcare['Discharge Date'])
df_healthcare['Length of Stay (Days)'] = (df_healthcare['Discharge Date'] - df_healthcare['Date of Admission']).dt.days
df_healthcare['Name'] = df_healthcare['Name'].str.title()
df_healthcare['Gender'] = df_healthcare['Gender'].str.capitalize()
df_healthcare['Hospital'] = df_healthcare['Hospital'].str.strip()
df_healthcare['Medical Condition'] = df_healthcare['Medical Condition'].str.capitalize()

# Metrics
avg_length_of_stay = df_healthcare['Length of Stay (Days)'].mean()
most_common_condition = df_healthcare['Medical Condition'].mode()[0]

# Define layout for the Overview page
dash.register_page(__name__, path="/")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.H1("Health Care Overview", className="text-center", style={"color": "#0d6efd", "margin-bottom": "20px"})
                ]), width=12)
            ],
            className="mb-4",
            style={"backgroundColor": "black"},
        ),

        # Metric Overview
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.H2(f"{len(df_healthcare)}", className="text-center", style={"color": "#0d6efd"}),
                    html.P("Total Admissions", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),

                dbc.Col(html.Div([
                    html.H2(f"{round(avg_length_of_stay, 1)} Days", className="text-center", style={"color": "#0d6efd"}),
                    html.P("Avg Length of Stay", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),

                dbc.Col(html.Div([
                    html.H2(f"{most_common_condition}", className="text-center", style={"color": "#0d6efd"}),
                    html.P("Most Common Condition", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),

                dbc.Col(html.Div([
                    html.H2(f"${round(df_healthcare['Billing Amount'].mean(), 2)}", className="text-center", style={"color": "#0d6efd"}),
                    html.P("Avg Billing Amount (USD)", className="text-center", style={"color": "white"})
                ]), width=3, className="p-3", style={"backgroundColor": "#000"}),
            ],
            justify="center",
            className="mb-4"
        ),

        # Year Range Slider
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.Label("Select Year Range for Analysis:", style={"color": "#0d6efd", "font-size": "16px"}),
                        dcc.RangeSlider(
                            id="year-range-slider",
                            min=df_healthcare['Date of Admission'].dt.year.min(),
                            max=df_healthcare['Date of Admission'].dt.year.max(),
                            value=[df_healthcare['Date of Admission'].dt.year.min(), df_healthcare['Date of Admission'].dt.year.max()],
                            marks={year: str(year) for year in range(df_healthcare['Date of Admission'].dt.year.min(), 
                                                                      df_healthcare['Date of Admission'].dt.year.max() + 1)},
                            step=1,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ]),
                    width=12
                )
            ],
            className="mb-2",
            style={"backgroundColor": "black"}
        ),

        # Graphs: Admissions by Year and Avg Billing Amount
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="admissions-per-year-bar-chart",
                              config={"displayModeBar": False}),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id="avg-billing-line-chart",
                              config={"displayModeBar": False}),
                    width=6
                )
            ],
            className="mb-4"
        ),

        # Interactive Table
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H4("Patient Details", className="text-center", style={"color": "#0d6efd"}),
                        DataTable(
                            id="patient-details-table",
                            columns=[{"name": col, "id": col} for col in ["Name", "Age", "Gender", "Medical Condition", "Billing Amount"]],
                            data=df_healthcare.to_dict('records'),
                            style_table={'height': '300px', 'overflowY': 'auto'},
                            style_header={'backgroundColor': '#0d6efd', 'color': 'white'},
                            style_cell={
                                'backgroundColor': 'black',
                                'color': 'white',
                                'textAlign': 'center',
                            },
                        )
                    ])
                )
            ],
            className="mb-4"
        )
    ],
    fluid=True
)

# Callbacks for Graphs
@dash.callback(
    Output("admissions-per-year-bar-chart", "figure"),
    Output("avg-billing-line-chart", "figure"),
    Input("year-range-slider", "value")
)
def update_graphs(year_range):
    # Filter data by year range
    filtered_df = df_healthcare[(df_healthcare['Date of Admission'].dt.year >= year_range[0]) & 
                                (df_healthcare['Date of Admission'].dt.year <= year_range[1])]

    # Bar chart: Admissions per Year
    admissions_per_year = filtered_df['Date of Admission'].dt.year.value_counts().sort_index()
    fig_bar = go.Figure(go.Bar(
        x=admissions_per_year.index.astype(str),
        y=admissions_per_year.values,
        marker_color="#0d6efd"
    ))
    fig_bar.update_layout(
        title="Admissions Per Year",
        xaxis_title="Year",
        yaxis_title="Number of Admissions",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    # Line chart: Avg Billing Amount
    avg_billing_per_year = filtered_df.groupby(filtered_df['Date of Admission'].dt.year)['Billing Amount'].mean()
    fig_line = go.Figure(go.Scatter(
        x=avg_billing_per_year.index.astype(str),
        y=avg_billing_per_year.values,
        mode='lines+markers',
        line=dict(color="#0d6efd", width=2),
        marker=dict(size=6, color="#0d6efd", symbol='circle')
    ))
    fig_line.update_layout(
        title="Avg Billing Amount Per Year",
        xaxis_title="Year",
        yaxis_title="Avg Billing Amount (USD)",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig_bar, fig_line
