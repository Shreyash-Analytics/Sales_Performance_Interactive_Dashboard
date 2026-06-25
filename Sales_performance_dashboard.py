import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# --- DATA LOADING ---
path = 'sales_data.csv'
#path = r'E:\MBA\Github\Sales_Data_Dashboard\sales_data.csv'
df = pd.read_csv(path)
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# --- INITIALIZE APP ---
app = Dash(__name__)
server = app.server

# --- LAYOUT ---
app.layout = html.Div([
    html.H1("Sales Performance Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([html.H3(id='sales-kpi'), html.P("Total Sales")], 
                 style={'width': '45%', 'display': 'inline-block', 'border': '1px solid black', 'textAlign': 'center'}),
        html.Div([html.H3(id='profit-kpi'), html.P("Total Profit")], 
                 style={'width': '45%', 'display': 'inline-block', 'border': '1px solid black', 'textAlign': 'center', 'marginLeft': '5%'})
    ]),

    html.Div([
        dcc.Dropdown(id='region-dropdown', 
                     options=[{'label': r, 'value': r} for r in df['Region'].unique()],
                     value=df['Region'].unique().tolist(), multi=True),
        dcc.DatePickerRange(id='date-range', 
                            start_date=df['Order_Date'].min(), 
                            end_date=df['Order_Date'].max())
    ], style={'margin': '20px'}),

    dcc.Graph(id='line-chart'), 
    dcc.Graph(id='bar-chart'),  
    dcc.Graph(id='pie-chart')   
])

# --- INTERACTIVITY ---
@app.callback(
    [Output('line-chart', 'figure'), Output('bar-chart', 'figure'), 
     Output('pie-chart', 'figure'), Output('sales-kpi', 'children'), 
     Output('profit-kpi', 'children')],
    [Input('region-dropdown', 'value'), Input('date-range', 'start_date'), Input('date-range', 'end_date')]
)
def update_graphs(regions, start, end):
    dff = df[(df['Region'].isin(regions)) & (df['Order_Date'] >= start) & (df['Order_Date'] <= end)]
    
    s_kpi = f"₹{dff['Sales'].sum():,.0f}"
    p_kpi = f"₹{dff['Profit'].sum():,.0f}"
    
    fig1 = px.line(dff.groupby('Order_Date')['Sales'].sum().reset_index(), x='Order_Date', y='Sales', title="Sales Trend")
    fig2 = px.bar(dff.groupby('Region')['Sales'].sum().reset_index(), x='Region', y='Sales', title="Regional Sales")
    fig3 = px.pie(dff, values='Sales', names='Product_Category', title="Category Contribution")
    
    return fig1, fig2, fig3, s_kpi, p_kpi

if __name__ == '__main__':
    print("Dashboard is starting... please visit http://127.0.0.1:8051/ in your browser")
    app.run(debug=False, port=8051)