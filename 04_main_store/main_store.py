import plotly.graph_objects as graph_obj
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash.dependencies import Input, Output
from dash import dcc, html, Input, Output

#Configurando o tema do Dash App com o Dash Bootstrap Components e o Dash Bootstrap Templates
dark_theme = 'darkly'
vapor_theme = 'vapor'
url_dark_theme = dbc.themes.DARKLY
url_vapor_theme = dbc.themes.VAPOR