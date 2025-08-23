import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, dash_table, callback_context
import plotly.express as px
import os


csv_file = "/Users/ayushjain/Desktop/SIT225 DATA CAPTURE CODES/HD TASK/gyrooo_data.csv"


def load_csv():
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    data = pd.read_csv(csv_file)
    if data.empty:
        raise ValueError("CSV file is empty")
    return data


app = Dash(__name__)
app.title = "Gyroscope Dashboard"


app.layout = html.Div([
    html.H1("Gyroscope Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Chart Type:"),
        dcc.Dropdown(
            id='chart-type',
            options=[{'label': i, 'value': i} for i in ['Line', 'Scatter', 'Distribution']],
            value='Line',
            clearable=False
        ),
        html.Label("Select Axes:"),
        dcc.Dropdown(
            id='axis-select',
            options=[{'label': i, 'value': i} for i in ['x','y','z']],
            value=['x','y','z'],
            multi=True
        ),
        html.Label("Number of Samples:"),
        dcc.Input(id='num-samples', type='number', value=50, min=1),
        html.Br(), html.Br(),
        html.Button("Previous", id='prev-btn', n_clicks=0),
        html.Button("Next", id='next-btn', n_clicks=0),
        html.Div(id='current-range', style={'marginTop': 10})
    ], style={'width':'30%', 'display':'inline-block', 'verticalAlign':'top'}),

    html.Div([
        dcc.Graph(id='gyro-graph')
    ], style={'width':'65%', 'display':'inline-block', 'padding':'0 20'}),

    html.H3("Data Summary"),
    dash_table.DataTable(id='summary-table'),


    dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0)
])


@app.callback(
    Output('gyro-graph', 'figure'),
    Output('summary-table', 'data'),
    Output('current-range', 'children'),
    Input('chart-type', 'value'),
    Input('axis-select', 'value'),
    Input('num-samples', 'value'),
    Input('prev-btn', 'n_clicks'),
    Input('next-btn', 'n_clicks'),
    Input('interval-component', 'n_intervals'),
    State('prev-btn', 'n_clicks'),
    State('next-btn', 'n_clicks')
)
def update_dashboard(chart_type, axes, num_samples, prev_clicks, next_clicks, n_intervals, prev_state, next_state):
    try:
        data = load_csv()
    except Exception as e:
        return {}, [], f"Error: {e}"

    num_samples = min(num_samples, len(data))

 
    start_idx = 0
    ctx = callback_context
    if ctx.triggered:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'prev-btn':
            start_idx = max(0, prev_clicks * num_samples - num_samples)
        elif triggered_id == 'next-btn':
            start_idx = min(len(data) - num_samples, next_clicks * num_samples)

    subset = data.iloc[start_idx:start_idx+num_samples][axes]

    # Create figure
    if chart_type == 'Line':
        fig = px.line(subset, y=axes)
    elif chart_type == 'Scatter':
        if len(axes) >= 2:
            fig = px.scatter(subset, x=axes[0], y=axes[1])
        else:
            fig = px.scatter(subset, x=subset.index, y=axes[0])
    else:  # Distribution
        fig = px.histogram(subset, x=axes[0])


    summary = subset.describe().reset_index().to_dict('records')

    range_text = f"Displaying samples {start_idx} to {start_idx + len(subset)} of {len(data)}"

    return fig, summary, range_text


if __name__ == "__main__":
    app.run(debug=True)
