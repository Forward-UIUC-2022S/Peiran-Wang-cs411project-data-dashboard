from cProfile import label
from email import header
from turtle import title
from click import style
from dash import Dash, dcc, html, Input, Output, callback, State
from numpy import character, empty
import pandas as pd


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(className="all-wrapper",children=[
  html.Div("This is title", style={"color": "white"}, className="Navigation"),
  html.Div(className="main_wrapper", children= [
    html.Div(id="widget01", children=[
      html.H3("I am widget01") 
    ]),
    html.Div(id="widget02", children=[
      html.H3("I am widget02")
    ]),
    html.Div(id="widget03", children=[
      html.H3("I am widget03")
    ]),
    html.Div(id="widget04", children=[
      html.H3("I am widget04")
    ]),
    html.Div(id="widget05", children=[
      html.H3("I am widget05")
    ]),
    html.Div(id="widget06", children=[
      html.H3("I am widget06")
    ]),
  ]),
])

if __name__ == '__main__':
  app.run_server(debug=True)


