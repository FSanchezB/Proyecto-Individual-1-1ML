import pandas as pd
df=pd.read_csv(r'C:\Users\Fernando\Desktop\Proyecto 1\Proyecto-Individual-1-ML\data procesada para funciones\movies_procesado')
df_directores=pd.read_csv(r'C:\Users\Fernando\Desktop\Proyecto 1\Proyecto-Individual-1-ML\data procesada para funciones\directores_procesado')
df_actores=pd.read_csv(r'C:\Users\Fernando\Desktop\Proyecto 1\Proyecto-Individual-1-ML\data procesada para funciones\actores_procesado')
df.drop('Unnamed: 0',axis=1,inplace=True)

from fastapi import FastAPI

app = FastAPI()

#funcion 1
@app.get("/cantidad_filmaciones_mes/{mes}")
def get_cantidad_filmaciones_mes(mes:str):
    meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    mes = mes.lower()
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d')
    count = df.loc[df['release_date'].dt.month == meses[mes]].shape[0]
    return {f"{count} peliculas fueron estrenadas en el mes de {mes.title()}"}


#funcion 2
@app.get("/cantidad_filmaciones_dia/{dia}")
def get_cantidad_filmaciones_dia(dia:str):
    dias={'lunes':'Monday','martes':'Tuesday','miercoles':'Wednesday','jueves':'Thursday','viernes':'Friday','sabado':'Saturday','domingo':'Sunday'} #diccionario con el nombre en espanol y su equivalente en ingles del df
    dia=dia.lower() #estandarizamos
    count=df.loc[df['day_of_week_release']==dias[dia]].shape[0]
    return {f'{count} peliculas fueron estrenadas en día {dia.title()}'} #sacamos las filas del dataframe que cumple con esas condiciones

