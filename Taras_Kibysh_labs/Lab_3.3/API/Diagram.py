import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from django_plotly_dash import DjangoDash

# Створіть Dash додаток через DjangoPlotlyDash
app = DjangoDash('InsuranceDashboard')

app.layout = html.Div([
    html.H1("Numbers of years")
    dcc.RangeSlider(
        min=2020,
        max=2024,
        step=1,
        value=[2020, 2024],
        marks={year: str(year) for year in range(2020, 2025)},
        id='year-range-slider'
    ),
    html.Div(id='slider-output-container'),
    dcc.Graph(id='insurance-graph-1'),
])

@app.callback(
    [Output('slider-output-container', 'children'),
     Output('insurance-graph-1', 'figure'),
     Output('insurance-graph-2', 'figure')],
    Input('year-range-slider', 'value')
)
def update_output(year_range):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    fig1 = px.line(filtered_df, x='year', y='total_count', markers=True,
                   title='Insurance Capacity by Year - Graph 1')
    fig2 = px.bar(filtered_df, x='year', y='total_count', title='Insurance Capacity by Year - Graph 2')

    range_output = f'You have selected years: {year_range[0]} - {year_range[1]}'

if __name__ == 'InsuranceDashboard':
    app.run(debug=True)
