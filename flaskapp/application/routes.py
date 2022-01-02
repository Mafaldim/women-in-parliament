from application import app
from flask import render_template, url_for
import pandas as pd
import plotly
import plotly.express as px
import json
import plotly.graph_objects as go


@app.route("/")
def index():

    # Graph One
    df = pd.read_csv('../data/avg_yearly.csv')
    df['women_perc'] = round(df['women_perc'], 2)

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

    # Graph 3
    df_dec_avg = pd.DataFrame(df.groupby(['decade'])['women_perc'].median())
    df_dec_avg = df_dec_avg.sort_values('women_perc')
    df_dec_avg['perc_change'] = round( df_dec_avg['women_perc'].pct_change(), 2)

    fig3 = go.Figure(data=[go.Table(header=dict(values=['Decade', 'Percentage Increase']),
                    cells=dict(values=[df_dec_avg.index[1:], df_dec_avg['perc_change'].iloc[1:]]))
                        ])
    fig3.update_layout(autosize=False,  width=350, height=350)

    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph 4
    df4 = pd.read_csv('../data/participation_by_decade_country_pop.csv')

    fig4 = px.scatter(df4, x='country', y='women_perc', color='country', size='pop',
                facet_col='decade', facet_col_wrap=2,facet_row_spacing=0.10,
                title='Women Participation in Parliaments(%) by Decade - World',
                labels=dict(women_perc='Women(%)', decade='Decade',
                country='Country',pop='Population (thousands)'),

    )
    fig4.update_layout(
            font_family="Courier New",
            font_color="grey",
            title_font_family="Courier New",
            title_font_color="#1f77b4",
            legend_title_font_color="grey"
            )
    fig4.update_xaxes(visible=False, showticklabels=False)
    fig4.update_yaxes(tick0=0, dtick=0.2,title_font = {"size": 11} )

    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


    


    return render_template("index.html", title="Home", graph1JSON = graph1JSON, graph2JSON = graph2JSON, graph3JSON = graph3JSON,graph4JSON = graph4JSON)