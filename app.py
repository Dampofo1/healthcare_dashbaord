import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)

app.title = "Health Care Dashboard"

# Your app layout and callbacks here
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Dashboard", href="/", style={"color": "#ff440c"})),
            dbc.NavItem(dbc.NavLink("Insurance Analysis", href="/insurance")),
            dbc.NavItem(dbc.NavLink("Blood Type Analysis", href="/blood-type-analysis")),
            dbc.NavItem(dbc.NavLink("Features Analysis", href="/medical_condition_analysis")),
            ],
        color="balck",
        dark=True,
        className="mb-4",
    ),
    dash.page_container  # Container to load the current page's layout
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)