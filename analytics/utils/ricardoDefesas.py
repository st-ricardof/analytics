import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from plotly.offline import plot
import plotly.graph_objects as go
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

def loadDefesasCurso():
    cursos = df_defesas['nomcur'].value_counts()
    defesasPorCurso = {}
    for i,v in cursos.items():
        curso = re.sub('\s\([^()]*\)', "", i )
        curso = 'História' if 'História' in curso else curso 
        curso = 'Letras' if any(substr in curso for substr in ['Tradução', 'Árabes', 'Língua', 'Lingüística', 'Literatura', 'Letras']) else curso#It will return True if any of the substrings in substring_list is contained in string.
        curso = 'Ciência Social' if any(substr in curso for substr in ['Política', 'Sociologia']) else curso
        try:
            defesasPorCurso[curso] += v
        except KeyError:
            defesasPorCurso[curso] = v
        return defesasPorCurso