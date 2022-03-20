from dash import Dash, dcc, html, Input, Output, callback, State
from numpy import character, empty
import mysql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import myneo4j
import mymongodb

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server


popularData = mysql.getTop5Professor();
def generateTopInfo(info, index):
  return html.Div(id=f"card-container{index}", className="card-wrapper",children=[
    html.Img(className="round", src=info[4]),
    html.Div(className="info-card", children = [
      html.H3(f"{info[0]}"),
      html.H6(f"{info[5]}"),
      html.H6(f"{info[2]}")
    ], style={"display": "inline-block", "position": "relative", "top": "-10px"})
  ]
  )

popularArticleData = mysql.getPopularArticle()
data = dict(
  character = popularArticleData[0],
  parent = popularArticleData[1],
  value = popularArticleData[2]
)
popularArticle_fig = px.sunburst(
  data,
  names = 'character',
  parents= 'parent',
  values = 'value'
)
popularArticle_fig.update_layout(
  autosize = False,
  width = 350,
  height = 350,
  font=dict(
    size = 10
  ),
  margin=dict(l=0, r=0, t=40, b=20),
  title = "top 5 popular areas and top 5 popular articles"
)

mysql.createTable()

app.layout = html.Div(className="all-wrapper",children=[
  html.Div("Find your research paper's direction & resources", style={"color": "white"}, className="Navigation"),
  html.Div(className="main_wrapper", children= [
    html.Div(id="popularFig-wrapper", children=[
    html.Div(dcc.Graph(id = "popularArticle", figure=popularArticle_fig))
  ]),
  html.Div(id="trend-wrapper", children = [
    html.H2("See the Trend of Different Areas", style={"color": "rgb(144, 147, 221)"}),
    dcc.Input(
        id='trend-list', className='input', type='text', placeholder='type topic to see the trend by the number of publications', value='',
        style={'height':'40px','margin': '10px'}
    ),
    html.Button("Search", id="trend-btn", n_clicks=0),
    html.Div(id="trendFig-wrapper")
  ]),
  html.Div(className="top-professor-wrapper", children=[
    html.H2("Top5 Professor Based on #Citations", style={"position": "relative", "top": "-400px", "color": "rgb(144, 147, 221)"}),
    html.Div(children = [generateTopInfo(item, index) for (index, item) in enumerate(popularData)])
  ]),
  html.Div(id="articleInArea-wrapper", children = [
    html.H2("See All Paper in This Area", style={"color": "rgb(144, 147, 221)"}),
    dcc.Input(
        id='area-list', className='input', type='text', placeholder='type topic to see all the article be publised in this area', value='',
        style={'height':'40px', 'margin': '10px'}
    ),
    html.Button("Search", id="articleInArea-btn", n_clicks=0),
    html.Div(id="articleInAreaFig-wrapper"),
  ]),
  html.Div(id="articleInProfessor-wrapper", children = [
    html.H2("See All Paper of The Professor", style={"color": "rgb(144, 147, 221)"}),
    dcc.Input(
        id='articleInProfessor-list', className='input', type='text', placeholder='type topic to see all the article be publised', value='',
        style={'height':'40px', 'margin': '10px'}
    ),
    html.Button("Search", id="articleInProfessor-btn", n_clicks=0),
    html.Div(id="articleInProfessorFig-wrapper")
  ]),
  html.Div(id="citationList-wrapper",
    children = [
      html.H1("Your Citation List"),
      dcc.Input(
        id='add_citation_list', className='input', type='text', placeholder='search article to add to citation list', value='',
        style={'height':'40px'}
      ),
      html.Div(id="citation_error"),
      html.Button("Add", id="add_btn", n_clicks=0),
      html.Div(id="citationFig-wrapper"),
      html.Button("Submit", id="remove_btn", n_clicks=0),
      html.Div(id="not_important")
  ]),

  ]),
])


@app.callback(Output("not_important", "children"),
              Input("remove_btn", "n_clicks")
)
def removeIt(n_clicks):
  mysql.removeCitationList()
  return html.Div()

@app.callback(Output('articleInProfessorFig-wrapper', 'children'),
              Input('articleInProfessor-btn', 'n_clicks'),
              State('articleInProfessor-list', 'value')
)
def showProfessorList(n_clicks, value):
  if (n_clicks == 0):
    return html.Div()
  else:
    info = mymongodb.getArticleByName(value)
    fig = go.Figure(data=[go.Table(header=dict(values=['title', 'venue', 'year', 'numCitations']),
                 cells=dict(values = info))
                     ])
    fig.update_layout(
      autosize = False,
      width = 500,
      height = 350,
      margin=dict(l=0, r=0, t=0, b=20),
    )
    return dcc.Graph(id="articleInProfessorFig", figure=fig)


@app.callback(Output('articleInAreaFig-wrapper', 'children'),
              Input('articleInArea-btn', 'n_clicks'),
              State('area-list', 'value')
)
def showList(n_clicks, value):
  if (n_clicks == 0):
    return html.Div()
  else:
    info = myneo4j.getArticleInArea(value)
    fig = go.Figure(data=[go.Table(header=dict(values=['title', 'venue', 'year', 'numCitations']),
                 cells=dict(values = info))
                     ])
    fig.update_layout(
      autosize = False,
      width = 500,
      height = 350,
      margin=dict(l=0, r=0, t=0, b=20),
    )
    return dcc.Graph(id="trend_fig", figure=fig)


@app.callback(Output('trendFig-wrapper', 'children'),
              Input('trend-btn', 'n_clicks'),
              State('trend-list', 'value')
)
def showTrendList(n_clicks, value):
  if (n_clicks == 0):
    return html.Div()
  else:
    year, num = mysql.getTrend(value)
    fig = go.Figure(data=go.Scatter(x=year, y=num))
    fig.update_layout(
      autosize = False,
      width = 650,
      height = 250,
      margin=dict(l=0, r=0, t=0, b=20),
    )
    return dcc.Graph(id="trend_fig", figure=fig)



@app.callback(Output('citationFig-wrapper', 'children'),
              Input('add_btn', 'n_clicks'),
              State('add_citation_list', 'value')
)
def showCitationList(n_clicks, value):
  data = mysql.getCitationList()
  citationList_fig = go.Figure(
    data = [go.Table(
    header = dict(values=['Title', 'Aruthor', 'published year','Num of Citation']),
    cells = dict(values = data))])
  citationList_fig.update_layout(
      autosize = False,
      width = 1300,
      height = 200,
      margin=dict(l=0, r=0, t=10, b=20),
    )
  if value != ' ':
    sign = mysql.insertCitaion(value)
  if (len(sign) == 0 and n_clicks > 0):
    return dcc.Graph(id="citation_list", figure=citationList_fig)
  if (len(sign) > 0 and sign[0] == 0 and n_clicks > 0):
    return dcc.Graph(id="citation_list", figure=citationList_fig)
  data2 = mysql.getCitationList()
  citationList_fig2 = go.Figure(
    data = [go.Table(
    header = dict(values=['Title', 'Aruthor', 'published year','Num of Citation']),
    cells = dict(values = data2))])
  citationList_fig2.update_layout(
      autosize = False,
      width = 1300,
      height = 200,
      margin=dict(l=0, r=0, t=10, b=20),
    )
  return dcc.Graph(id="citation_list", figure=citationList_fig2)

if __name__ == '__main__':
  app.run_server(debug=True)