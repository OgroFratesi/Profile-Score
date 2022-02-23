import dash  #(version 1.12.0)
from dash.dependencies import Input, Output
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import date
import numpy as np
from app_functions import *

import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------------------------------------
# Import the cleaned data (importing csv into pandas)
info = pd.read_csv('final.csv', index_col=0)

df = pd.read_csv('scores.csv', index_col=0)

df = round(df, 2)

columnas_tabla = ['Name', 'Experience', 'Positions', 'Aptitudes', 'Education', 'Total']


# -------------------------------------------------------------------------------------

color_style = {'background-color': 'rgb(248, 247, 241)'}

# Iniciamos la app

app = dash.Dash(
    __name__,
    external_stylesheets=[ dbc.themes.ZEPHYR ]
                )

# Creamos la arquitectura

app.layout = dbc.Container([

    # dbc.Spinner(color="primary",  #<--- Bootstrap para cuando tiene que cargar algo de lo que esta adentro de Children
    #             type="grow",    #<--- Tipos de animaciones 
    #             children=[

    dbc.Row([
            html.Br()  # <--- espacio
            ], style = color_style),

    dbc.Row(
            html.H1('PROFILE ANALYSIS', className='text-center text-primary mb-4', style={'font-family': 'Lato', 'font-size': '45px'}),  #<--- título
                justify='center',style = color_style#<-- Style para que quede centrado en la pagina
            ),

    dbc.Row([
            html.Br(),html.Br()   # <--- espacio
            ],style = color_style),
    
    dbc.Row(
        dbc.Col(
            html.Div('Skills:', style={'font-family': 'Lato', 'font-size': '22px'}),
                    className='text-center text-primary mb-4'
                    ),  style = color_style
                
            ),

    dbc.Row(
        dbc.Col(
            dbc.Input(id="input_1",                   #<--- input para escribir el primer autor
                        type="text", 
                        value='Python, Deep Learning, Machine Learning, PyTorch, NLP, Computer Vision', 
                        className='text-center')
                ), style = color_style
            ),

    dbc.Row([
            html.Br()  # <--- espacio
            ], style = color_style),

    dbc.Row([
        dbc.Col([
                dbc.Row(
                        html.Div('Experiencia:',style={'font-family': 'Lato', 'font-size': '22px'}), className='text-center text-primary mb-4'
                        ), 
                dbc.Row(
                        dcc.Dropdown(
                            options=[
                                {'label': 'No Experience', 'value': '0'},
                                {'label': '+1', 'value': '1'},
                                {'label': '+2', 'value': '2'},
                                 {'label': '+3', 'value': '3'},
                                  {'label': '+4', 'value': '4'},
                                   {'label': '+5', 'value': '5'}
                            ],
                            searchable=False
                        )
                        )],className='text-center mb-4',width={'size':4, 'offset':1, 'order':0}

                    ),
        dbc.Col([
                dbc.Row(
                        html.Div('Education:', style={'font-family': 'Lato', 'font-size': '22px'}), className='text-center text-primary mb-4'
                        ),
                dbc.Row(
                        dcc.Dropdown(
                            options=[
                                {'label': 'No Education', 'value': '0'},
                                {'label': 'Bachelor', 'value': '1'},
                                {'label': 'Post-Graduated', 'value': '2'},
                                 {'label': 'Master', 'value': '3'},
                                  {'label': 'PhD', 'value': '4'}
                            ],
                            searchable=False
                        )
                        )], className='text-center mb-4',width={'size':4, 'offset':2, 'order':0}

                    )
            ]),

    dbc.Row([
            html.Br()  # <--- espacio
            ], style = color_style),
    
    dbc.Row(
        dbc.Col(               # <---- Botón para comenzar a correr la función
            dbc.Button(
                    "Analize",
                    id='button', 
                    color="primary", 
                    size='lg'),
                className='text-center mb-3'),style = color_style
            ),

    dbc.Row([
            html.Br()  # <--- espacio
            ],style = color_style),
    
    dbc.Row([ 
        dbc.Col([

             dash_table.DataTable(                       #<--- df para el segundo autor
                        id='datatable1',
                        page_size= 10,
                        style_cell_conditional=[
                            {'if': {'column_id': i},'textAlign': 'left'} for i in columnas_tabla],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0},
                        style_header={
                            'textAlign':'left',
                            'backgroundColor': 'rgb(0, 119, 182)',
                            'fontWeight': 'bold',
                            'family-font':'Lato',
                            'color':'black'
                        },
                        style_data={
                            'backgroundColor': 'rgb(142, 202, 230)',
                            'color': 'black',
                            'family-font':'Lato'
                        },
                        tooltip_duration=None,
                        sort_action="native",
                        sort_mode="multi",
                        row_selectable="multi",
                        row_deletable=False,
                        selected_rows=[],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        virtualization=False,
                        page_action='none')
                ],className='text-center mb-4',width={'size':6, 'offset':0, 'order':0}),
        
        dbc.Col([
    
            dcc.Graph(id='grafico1'),

        ],className='text-center mb-4', width={'size':6, 'offset':0, 'order':2}),


    ],style = color_style),

            
    dbc.Row([
            html.Br(),html.Br()   # <--- espacio
            ]),

    dbc.Row(                         # <--- Boton para crear los graficos
        dbc.Col(
            dcc.Graph(id='grafico2'))

            ),
    

    dbc.Row([
            html.Br()
            ]),

    dbc.Row([
            dbc.Col([
                        dbc.ButtonGroup(
                            [dbc.Button("Experience"), dbc.Button("Education"), dbc.Button("Certifications")]
                        )
                ],className='text-center mb-4')]),


    dbc.Row([

            dbc.Col([               # <--- Segunda columna para insertar las cards

                dbc.CardGroup([
                                    
                    dbc.Card([
                        html.H2(id='name1', className='card-text',style={"margin-left": "15px"}),
                        html.P(id='position1', className='card-text',style={"margin-left": "15px"})
                    ],color="primary", outline=True,className='mini_container', style={'background-color': 'rgb(142, 202, 230)', "margin-left": "50px"}),

                            ])
            ]),

            dbc.Col([               # <--- Segunda columna para insertar las cards

                dbc.CardGroup([
                                    
                    dbc.Card([
                        html.H2(id='name2', className='card-title',style={"margin-left": "15px"}),
                        html.P(id='description2', className='card-text', style={"margin-left": "15px"})
                    ],color="primary", outline=True,className='mini_container', style={'background-color': 'rgb(142, 202, 230)', "margin-left": "50px"}),

                            ]),
            ]),

        ]),

    dbc.Row([
            html.Br(),html.Br()   # <--- espacio
            ],style = color_style),

    dbc.Row([                       # <--- Boton para crear los graficos
        dbc.Col(
            dcc.Graph(id='grafico3'),className='text-center mb-4',width={'size':8, 'offset':0, 'order':0}),

            

        dbc.Col([

                html.Br(),html.Br(),

                dbc.CardGroup([
                                    
                    dbc.Card([
                        html.H4('Bachelor', className='card-text',style={"margin-left": "5px"}),
                        html.P('93%', className='card-text', style={"margin-left": "10px"})
                    ],color="primary", outline=True,className='mini_container', style={'background-color': 'rgb(142, 202, 230)'}),

                    dbc.Card([
                        html.H4('Post-Graduated', className='card-text',style={"margin-left": "5px"}),
                        html.P('55%', className='card-text', style={"margin-left": "15px"})
                    ],color="primary", outline=True,className='mini_container', style={'background-color': 'rgb(142, 202, 230)', "margin-left": "10px"})

                            ]),

                dbc.CardGroup([
                                    
                    dbc.Card([
                        html.H4('Master', className='card-text',style={"margin-left": "5px"}),
                        html.P('33%', className='card-text', style={"margin-left": "10px"})
                    ],color="primary", outline=True,className='mini_container', style={'background-color': 'rgb(142, 202, 230)', 'margin-top':'10px'}),

                    dbc.Card([
                        html.H4('PhD', className='card-text',style={"margin-left": "5px"}),
                        html.P('15%', className='card-text', style={"margin-left": "15px"})
                    ],color="primary", outline=True,className='mini_container', style={'background-color': 'rgb(142, 202, 230)', "margin-left": "10px", 'margin-top':'10px'})

                            ])
                            
                            
        ],className='text-center mb-4',width={'size':4}) 
                            
                            
                ,],style = color_style)

    # ])
   
    
],style = color_style) 

#---------------------------------------------------------------------------------------#
#Configuramos los decoradores#


# El primer decorador, obtiene los valores de los autores seleccionados, y el rango de fechas.
# Pero para comenzar a activar la funcion, es necesario hacer click en el boton 'analizar'.
# Los outputs de este decorador son las tablas para cada autor. Donde cada tabla necesita el nombre de sus
# columnas y un diccionario que le pase la 'data'. Ademas, le pasamos los datos para el component_property
# 'tooltip_data', que nos permite pasar el mouse por arriba del texto y que nos muestre el texto completo.

@app.callback([
     dash.dependencies.Output(component_id='datatable1',component_property= 'columns'),
     dash.dependencies.Output(component_id='datatable1',component_property= 'data'),
     dash.dependencies.Output(component_id='datatable1',component_property= 'tooltip_data')],  # <--- pasa el nombre de los autores seleccionados
    [dash.dependencies.Input(component_id='button',component_property= 'n_clicks'),
     dash.dependencies.State(component_id='input_1',component_property= 'value')],prevent_initial_call=False)
def update_app(n, skills):

    global df1                                              # <--- hacemos los df globales asi podemos usarlos en otras funciones
    df1 = traer_df()

    df1_to_show = df1[['name', 'experience', 'positions', 'aptitudes', 'education', 'total']]
    df1_to_show.columns = columnas_tabla
    columns1 = [{'name': col, 'id': col} for col in df1_to_show.columns]
    data1 = df1_to_show.to_dict(orient='records')


    tooltip_data1=[{column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                    } for row in df1_to_show.to_dict('records')]


    return columns1,data1, tooltip_data1



# El segundo callback, obtiene las filas seleccionadas de la tabla, y devuelve la informacion dentro de las cartas.
# Establecemos que si no se selecciona ninguna fila, los valores de las cartas seran los totales de cada usuario.
# Ademas, para cada valor, se le asigna un color. Rojo si el valor es menor que el del autor a comparar, y verde si es mayor.

@app.callback(
    [ dash.dependencies.Output(component_id='grafico2',component_property= 'figure'),
     dash.dependencies.Output(component_id='grafico1',component_property= 'figure')],
    [dash.dependencies.Input('datatable1', 'selected_rows')]
     ,prevent_initial_call=False)
def update_info(rows1):
    
    fig1 = plot_radar(rows1)
    # global df1_p

    fig2 = plot_bar(rows1)

    return fig2, fig1

# # El tercer callback, tiene como inputs los nombres de los autors, las filas seleccionadas de la tabla, el valor del
# # radio_item y si se clickeo o no el boton.
# # Devuelve los graficos actualizados. 

@app.callback(
    [dash.dependencies.Output(component_id='name1',component_property= 'children'),
     dash.dependencies.Output(component_id='position1',component_property= 'children'),
     dash.dependencies.Output(component_id='name2',component_property= 'children'),
     dash.dependencies.Output(component_id='description2',component_property= 'children')],
    [dash.dependencies.Input('datatable1', 'selected_rows')]
     ,prevent_initial_call=False)
def update_info(rows1):
    
    
    text1, text2 = traer_info(rows1)

    name_s = 'font-weight-bold text-success'
    position_s = 'font-weight-bold text-success'

    position_t = 'Data Scientist'

    text1_markdown = []
    text2_markdown = []
    for t in text2[1:]:
        text2_markdown.append(dcc.Markdown(t))
    for t in text1[1:]:
        text1_markdown.append(dcc.Markdown(t))

    text1_markdown.append(dbc.CardLink("Linkedin Profile", href="https://linkedin.com/in/aakankshasharma19", target='_blank'))
    text2_markdown.append(dbc.CardLink("Linkedin Profile", href="https://linkedin.com/in/aakankshasharma19"))
    
    # f'{name_t}', html.Br(), 'hola')

    return (dcc.Markdown(text1[0])), tuple(text1_markdown) ,(dcc.Markdown(text2[0])), tuple(text2_markdown)



@app.callback(
    [ dash.dependencies.Output(component_id='grafico3',component_property= 'figure')],
    [dash.dependencies.Input(component_id='button',component_property= 'n_clicks'),
    dash.dependencies.State(component_id='input_1',component_property= 'value')]
     ,prevent_initial_call=False)
def update_info(n, skills_list):
    
    skills_l = skills_list.split(',')
    skills_list = []
    for sk in skills_l:
        if sk[0] == ' ':
            skills_list.append(sk[1:])
        else:
            skills_list.append(sk)

    fig2 = plot_skills(skills_list)

    return [fig2]

# -------------------------------------------------------------------------------------




if __name__ == '__main__':
    app.run_server(debug=True)