import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import re  #regex

parametros = {
        'ano': 2021,
        'codcur': ''
    }

defesas_json = requests.get(url = 'https://dados.fflch.usp.br/api/defesas', params = parametros)
defesas_json = defesas_json.json()

df_defesas = pd.DataFrame(defesas_json)

def loadNivel():
    nivel_plot = sns.countplot(x='nivel', data=df_defesas)
    plt.xticks(rotation=45)
    buffer = BytesIO() 
    nivel_plot.figure.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return {'df': df_defesas, 'nivel_plot': graph}

def loadDefesasProgramaCurso():
    cursos = df_defesas['nomcur'].value_counts()
    defesasPorCurso = {}
    defesasPorPrograma = []
    for i,v in cursos.items():
        curso = re.sub('\s\([^()]*\)', "", i )
        curso = 'História' if 'História' in curso else curso 
        curso = 'Letras' if any(substr in curso for substr in ['Tradução', 'Árabes', 'Língua', 'Lingüística', 'Literatura', 'Letras']) else curso#It will return True if any of the substrings in substring_list is contained in string.
        curso = 'Ciência Social' if any(substr in curso for substr in ['Política', 'Sociologia']) else curso
        defesasPorPrograma.append([curso, i,v])
        try:
            defesasPorCurso[curso] += v
        except KeyError:
            defesasPorCurso[curso] = v
    #grafico defesas por curso
    fig = go.Figure(
    data=[go.Bar(x=list(defesasPorCurso.keys()), y=list(defesasPorCurso.values()))],
    layout_title_text="Defesas de Mestrado e Doutorado realizadas em 2021 separadas por curso")

    graphDefesasPorCurso = plot(fig, output_type="div")

    #grafico defesas programa curso
    df = pd.DataFrame(defesasPorPrograma, columns=["Curso", "Programa", "Defesas"])
    
    fig2 = px.bar(df, x="Curso", y="Defesas", color="Programa", title="Defesas FFLCH 2021",
     height=800)
    fig2.add_annotation(
        text = (f"Fonte: Portal de Dados FFLCH https://dados.fflch.usp.br/ ")
        , showarrow=False
        , x = 0
        , y = -0.15
        , xref='paper'
        , yref='paper' 
        , xanchor='left'
        , yanchor='bottom'
        , xshift=-1
        , yshift=-5
        , font=dict(size=10, color="grey")
        , align="left"
    )
    graphDefesasPorPrograma = plot(fig2, output_type="div")

    return {'defesasPorCurso': graphDefesasPorCurso, 'defesasPorPrograma': graphDefesasPorPrograma}