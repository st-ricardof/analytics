import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def load():
    parametros = {
        'ano': 2021,
        'codcur': ''
    }

    defesas_json = requests.get(url = 'https://dados.fflch.usp.br/api/defesas', params = parametros)
    defesas_json = defesas_json.json()

    df_defesas = pd.DataFrame(defesas_json)

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
