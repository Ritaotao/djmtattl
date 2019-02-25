# template: https://alysivji.github.io/reactive-dashboards-with-dash.html
# standard library
import os

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# additional libs
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# sqlalchemy funcs
from models import Station, Device, Turnstile, data_frame
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import INTEGER
from sqlalchemy import func

# set params
# connString = os.environ['DB_URI']
connString = 'sqlite:///C:\\Users\\Ruitao.Cheng\\Desktop\\mta\\mta_sample1718.db'
conn = create_engine(connString, echo=True)

def make_session(engine=conn):
    Session = sessionmaker(bind=conn)
    session = Session()
    return session

###########################
# Data Manipulation / Model
###########################
def to_ts(date_str):
    '''convert string date ie. 2018-01-01 00:00:00 to unix timestamp
        WARNING: may need to consider TIMEZONE, db used NY timezone'''
    date_dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return int((date_dt - datetime(1970, 1, 1)) / timedelta(seconds=1))

def get_station_summary(start_date='2018-01-01 00:00:00', end_date='2018-02-01 00:00:00'):
    start_ts = to_ts(start_date)
    end_ts = to_ts(end_date)
    session = make_session(conn)
    query = session.query(Station.name, func.sum(Turnstile.entry), func.sum(Turnstile.exit)).\
        filter(Turnstile.device_id==Device.id).filter(Device.station_id==Station.id).\
        filter(Turnstile.timestamp>=start_ts, Turnstile.timestamp<=end_ts).\
        filter(Station.name.isnot(None)).\
        group_by(Station.name).all()
    df = pd.DataFrame(query, columns=['station', 'entry', 'exit'])
    df['volume'] = df['entry'] + df['exit']
    df = df.sort_values('volume', ascending=False)
    #print(df.head())
    return df

df = get_station_summary()

#########################
# Dashboard Layout / View
# Wire-frame components in this section, data will be populated via Model and Controller
#########################

def generate_table(dataframe, max_rows=10):
    '''Given dataframe, return template generated using Dash components'''
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# Set up Dashboard and create layout
app = dash.Dash()
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Station Summary',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='top-station-entry-vs-exit',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['station'] == i]['entry'],
                    y=df[df['station'] == i]['exit'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.station.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Entry'},
                yaxis={'title': 'Exit'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }       
    ),

    generate_table(df)

])


#############################################
# Interaction Between Components / Controller
#############################################




# start Flask server
if __name__ == '__main__':
    app.run_server(
        debug=True,
        #host='0.0.0.0',
        port=8050
    )