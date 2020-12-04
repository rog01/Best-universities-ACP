import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
         return app1.layout1
    elif pathname == '/apps/app2':
         return app2.layout2
    else:
        return 'Cette url n\'est pas valide'

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1',port=8060)
