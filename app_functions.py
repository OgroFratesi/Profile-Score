import pandas as pd
import plotly.graph_objects as go
from dash import dcc

df_new = pd.read_csv('scores.csv', index_col=0)

df_info = pd.read_csv('final.csv', index_col=0)

categories = ['Experience','Positions','Aptitudes', 'Education', 'Other']

def traer_df():

    df = pd.read_csv('scores.csv', index_col=0)

    return df


def traer_info(rows1):

    if len(rows1) == 0:
        rows1 = df_new.sort_values('total', ascending=False).index[:2].to_list()
    elif len(rows1) == 1:
        rows1 += df_new.sort_values('total', ascending=False).index[:1].to_list()

    df_new['rank'] = df_new.total.rank(ascending=False, method='min')

    name, position, company, description, url = [], [], [], [], []
    ranking = []

    for e in range(len(rows1)):
        name.append(df_info.loc[rows1[e], 'name'])
        position.append(df_info.loc[rows1[e], 'title_raw'])
        company.append(df_info.loc[rows1[e], 'company'])
        description.append(df_info.loc[rows1[e], 'description'])
        url.append(df_info.loc[rows1[e], 'url'])
        ranking.append(int(df_new.loc[rows1[e], 'rank']))

    info_profiles = []
    for e in range(2):
        nam = name[e]
        url = url[e]
        pos = position[e].split('/n')
        com = company[e].split('/n')
        des = description[e].split('/n')
        info = []
        info.append((f' # {nam} ({ranking[e]}°)'))
        info.append((f' ---------- '))
        for p, c, d in zip(pos, com, des):
            info.append((f'#### {c} - {p}'))
            info.append((f'{d}'))
            info.append((f' ---------- '))
        info_profiles.append(info)

    return info_profiles[0], info_profiles[1]

def plot_radar(rows1):

    pool_mean = round(df_new.mean()).to_list()

    if len(rows1) != 0:                 # <--- Modificamos el df, para tener solo los datos de las filas seleccionadas.
        df_sel = df_new[df_new.index.isin (rows1)]
        r = []
        r_names = []
        for e in range(len(df_sel)):
            r.append(df_sel.iloc[e,:].to_list()[1:])
            r_names.append(df_sel.iloc[e,:].to_list()[0])
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=pool_mean,
        theta=categories,
        fill='toself',
        name='Pool Mean'
    ))

    if len(rows1) != 0:  
        for name, profile in zip(r_names, r):

            fig.add_trace(go.Scatterpolar(
                r=profile,
                theta=categories,
                fill='toself',
                name=name
            ))


    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=False,
        range=[0, 100],
        )),
          paper_bgcolor='rgb(248, 247, 241)',
        plot_bgcolor='rgb(248, 247, 241)',
    showlegend=True,
    font=dict(family='Lato', size=15)
    )

    return fig


def plot_bar(rows1):

    
    if len(rows1) != 0:                 # <--- Modificamos el df, para tener solo los datos de las filas seleccionadas.
        df_sel = df_new[df_new.index.isin (rows1)]
        r = []
        r_names = []
        for e in range(len(df_sel)):
            r.append(df_sel.iloc[e,:].to_list()[1:])
            r_names.append(df_sel.iloc[e,:].to_list()[0])
    
    pool_mean = round(df_new.mean()).to_list()

    fig = go.Figure()

    fig.add_trace(go.Bar(x=categories, y=pool_mean, name='Pool Mean',
                        marker_color='rgb(142,140,39)', marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.6,
                        textposition = "outside", texttemplate = "<b>%{y}<b>"
                        ))
    if len(rows1) != 0: 
        for name, scores in zip(r_names, r):
            fig.add_trace(go.Bar(x=categories, y=scores, name=name,
                                marker_line_width=1.5, opacity=0.6,marker_line_color='rgb(8,48,107)',
                                textposition = "outside", texttemplate = "<b>%{y}<b>"
                                ))


    fig.update_xaxes(title='<b>Categories<b>', showgrid=False)
    fig.update_yaxes(title='<b>Score<b>')

    fig.update_layout(title=dict(text="<b>Score Comparison</b>",
                                font=dict(size=40, family="Lato")),
                    showlegend=True,
                    paper_bgcolor='rgb(248, 247, 241)',
                    plot_bgcolor='rgb(248, 247, 241)',
                    font=dict(family='Lato', size=15))

    return fig

def plot_skills(skill_list):


    per_skill = []

    for skill in skill_list:
        s = skill.lower()
        p = round((df_info[df_info.expertise.str.contains(s, na=False)].shape[0] / df_info.shape[0]) * 100,1)
        per_skill.append(p)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=per_skill, y=skill_list, name='Libres',
                        marker_color='rgb(142,140,39)', marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.6,
                        textposition = "outside", texttemplate = "<b>%{x}<b>", orientation='h'
                        ))


    fig.update_xaxes(title='<b>%<b>', ticksuffix='%',showgrid=False, range=[0, 100])
    fig.update_yaxes(title='<b>Skills<b>')

    # fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

    fig.update_layout(title=dict(text="<b>% of profiles with skills</b>",
                                font=dict(size=35)),
                    showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Lato'))

    return fig