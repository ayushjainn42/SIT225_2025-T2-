import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px


df = pd.read_csv("gyro_data.csv")

if 'time' not in df.columns:
    df.insert(0, 'time', range(len(df)))


#the Dash app
app = dash.Dash(__name__)

#App Layout
app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard", style={'textAlign': 'center'}),

    # Graph type dropdown
    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Distribution Plot', 'value': 'histogram'}
        ],
        value='line'
    ),

    # Variable selection dropdown
    html.Label("Select Variables:"),
    dcc.Dropdown(
        id='variable-select',
        options=[
            {'label': 'X', 'value': 'x'},
            {'label': 'Y', 'value': 'y'},
            {'label': 'Z', 'value': 'z'},
        ],
        value=['x', 'y', 'z'],
        multi=True
    ),

    # Number of samples input
    html.Label("Number of samples to display:"),
    dcc.Input(id='num-samples', type='number', value=100, min=1, step=1),

    # Navigation buttons
    html.Div([
        html.Button("Previous", id='prev-btn', n_clicks=0),
        html.Button("Next", id='next-btn', n_clicks=0)
    ], style={'marginTop': '10px'}),

    # Graph output
    dcc.Graph(id='gyro-graph'),

    # Data summary table
    html.H3("Data Summary"),
    dash_table.DataTable(id='summary-table')
])

@app.callback(
    [Output('gyro-graph', 'figure'),
     Output('summary-table', 'data'),
     Output('summary-table', 'columns')],
    [Input('graph-type', 'value'),
     Input('variable-select', 'value'),
     Input('num-samples', 'value'),
     Input('prev-btn', 'n_clicks'),
     Input('next-btn', 'n_clicks')],
    [State('gyro-graph', 'figure')]
)
def update_graph(graph_type, variables, num_samples, prev_clicks, next_clicks, existing_fig):
    # Keep track of navigation index
    offset = (next_clicks - prev_clicks) * num_samples
    start = max(0, offset)
    end = min(len(df), start + num_samples)

    # Slice dataframe
    filtered_df = df.iloc[start:end]

    # Build figure
    if graph_type == 'line':
        fig = px.line(filtered_df, x='time', y=variables)
    elif graph_type == 'scatter':
        fig = px.scatter(filtered_df, x='time', y=variables)
    elif graph_type == 'histogram':
        fig = px.histogram(filtered_df, x=variables[0]) if variables else px.histogram(filtered_df, x='x')
    else:
        fig = px.line(filtered_df, x='time', y=variables)

    # Summary table
    summary = filtered_df[variables].describe().reset_index()
    columns = [{"name": i, "id": i} for i in summary.columns]
    data = summary.to_dict('records')

    return fig, data, columns

# -----------------------
# 5. Run the app
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)

