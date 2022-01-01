from application import app
from flask import render_template, url_for
import pandas as pd
import plotly
import plotly.express as px
import json

@app.route("/")
def index():

    # Graph One
    df = pd.read_csv('../data/avg_yearly.csv')

    fig1 = px.line(df, x='year_', y=['women_perc','RM5'],
            title='Women Representation in Parliament (Global Average) from 1945 to 2018',
            markers=True,
            labels=dict(year_='Year', women_perc='Participation (%)')
            )
    fig1.update_yaxes(title_text='Women (%)')

    fig1.update_layout(
            font_family="Courier New",
            font_color="grey",
            title_font_family="Courier New",
            title_font_color="#1f77b4",
            legend_title_font_color="grey",
            autosize=False,
            width=800,
            height=500
        )
    fig1.update_xaxes(nticks=10)
    fig1.update_xaxes(rangeslider_visible=True)

    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph2
    fig2 = px.box(df, x="decade", y="women_perc", color="decade",
             title="Women Representation in Parliament (Global Average) from 50's to 10's ",
             labels=dict(women_perc='Women (%)', decade='Decade')
            )

    fig2.update_layout(
            font_family="Courier New",
            font_color="grey",
            title_font_family="Courier New",
            title_font_color="#1f77b4",
            legend_title_font_color="grey",
            autosize=False,
            width=800,
            height=400
            )

    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)


    


    return render_template("index.html", title="Home", graph1JSON = graph1JSON, graph2JSON = graph2JSON)