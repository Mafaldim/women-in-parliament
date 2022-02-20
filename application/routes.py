from application import app
from flask import render_template, url_for
import pandas as pd, numpy as np
import plotly
import plotly.express as px
from plotly.offline import plot
import json
import plotly.graph_objects as go


@app.route("/")
def index():

    # Graph 1
    df = pd.read_csv('./data/avg_yearly.csv')
    df['women_perc'] = round(df['women_perc'], 2)

    fig1 = px.line(df, x='year', y=['women_perc','RM5'],
            title="Women's Representation in Parliament from 1945 to 2018 (Global Average)",
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
            autosize=True,
           
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
            autosize=True
            )
    
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph 3
    df_dec_avg = pd.DataFrame(df.groupby(['decade'])['women_perc'].median())
    df_dec_avg = df_dec_avg.sort_values('women_perc')
    df_dec_avg['perc_change'] = round( df_dec_avg['women_perc'].pct_change(), 2)

    fig3 = go.Figure(data=[go.Table(header=dict(values=['Decade', 'Percentage Increase']),
                    cells=dict(values=[df_dec_avg.index[1:], df_dec_avg['perc_change'].iloc[1:]]))
                        ])
    fig3.update_layout(autosize=True,height=350)

    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph 4
    df_historic_iso = pd.read_csv('./data/df_historic_iso.csv')

    fig4 = px.scatter(df_historic_iso, x="country", y="women_perc"
                    ,color="year",color_continuous_scale=px.colors.sequential.Turbo
                    ,labels=dict(women_perc='Women (%)', year='Year', country='Country')
                    ,title='Women Representation in Parliament Through the Years - Country Level from 1945 to 2018',)
    fig4.update_traces(marker_size=10)

    fig4.update_traces(marker=dict(size=8,
                                line=dict(width=1,
                                            color='blue')),
                    selector=dict(mode='markers'))

    fig4.update_layout(
            font_family="Courier New",
            font_color="grey",
            title_font_family="Courier New",
            title_font_color="#1f77b4",
            legend_title_font_color="grey",
            autosize=True,
            height=1000)            

    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder) 


    # Graph 5
    df_2021_region = pd.read_csv('./data/women_percent_as_of2021_with_regions.csv')
    fig5 = px.treemap(df_2021_region, 
                 path=[px.Constant("world"), 'region', 'country'], 
                 values='%W',
                 color='%W', 
                 title='Women Representation in Parliament 2021',
                 color_continuous_scale='RdBu',
                 color_continuous_midpoint=np.average(df_2021_region['%W'], weights=df_2021_region['%W']),
                 hover_data = ['%W'])
    fig5.update_traces(root_color="red")
    fig5.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig5.data[0].hovertemplate = "%{label}<br>%{value}%"

    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)


    # Graph 6
    df = pd.read_csv('./data/barchart.csv')

    fig6 = px.bar(df, x="region", y="women_perc",
                  color="region",  hover_name="country",
                  animation_frame="year", animation_group="country", range_y=[0,15],
                  labels=dict(women_perc='Aggregate Women Percentage(%)', region='Region',year='Year'),
                  title='Women Participation for Countries in Region - 1960 to 2017')
    
    fig6.update_layout(
            font_family="Courier New",
            font_color="grey",
            title_font_family="Courier New",
            title_font_color="#1f77b4",
            legend_title_font_color="grey",
            )
    
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", title="Home", graph1JSON = graph1JSON, graph2JSON = graph2JSON, graph3JSON = graph3JSON, graph4JSON = graph4JSON, graph5JSON = graph5JSON,graph6JSON=graph6JSON)
    
    
