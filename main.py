import pandas as pd
import numpy as np
df=pd.read_csv('data procesada para funciones/movies_reducido')
df_directores=pd.read_csv('data procesada para funciones/directores_reducido')
df_actores=pd.read_csv('data procesada para funciones/actores_reducido')
df_ml=pd.read_csv('data procesada para funciones/data_funcion_recomendacion')
df.drop('Unnamed: 0',axis=1,inplace=True)

from fastapi import FastAPI

app = FastAPI()

#funcion 1
@app.get("/cantidad_filmaciones_mes/{mes}")
def get_cantidad_filmaciones_mes(mes:str):
    meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    mes = mes.lower()
    
    if mes not in meses: 
        return {f'{mes} no es una entrada valida, intente de nuevo'}
    
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d')
    count = df.loc[df['release_date'].dt.month == meses[mes]].shape[0]
    return {f"{count} peliculas fueron estrenadas en el mes de {mes.title()}"}


#funcion 2
@app.get("/cantidad_filmaciones_dia/{dia}")
def get_cantidad_filmaciones_dia(dia:str):
    dias={'lunes':'Monday','martes':'Tuesday','miercoles':'Wednesday','jueves':'Thursday','viernes':'Friday','sabado':'Saturday','domingo':'Sunday'} 
    dia=dia.lower() #estandarizamos

    if dia not in dias:
        return {f'{dia} no es una entrada valida, intente de nuevo'}
    
    count=df.loc[df['day_of_week_release']==dias[dia]].shape[0]
    return {f'{count} peliculas fueron estrenadas en día {dia.title()}'} 

#funcion 3
@app.get("/score_titulo/{titulo_de_la_filmacion}")
def get_score_titulo(titulo_de_la_filmacion:str):
    pelicula = df.loc[df['title'] == titulo_de_la_filmacion]

    if pelicula.empty:
        return{f'No se encontró la película con el título {titulo_de_la_filmacion}.'} 
    
    titulo = pelicula['title'].values[0]
    score = pelicula['popularity'].values[0] 
    year = pelicula['release_year'].values[0]

    return{f'La pelicula {titulo} fue estrenada en el año {year} con un score de {score}'}

#funcion 4
@app.get('/votos_titulo/{titulo_de_la_filmacion}')
def get_votos_titulo( titulo_de_la_filmacion:str ):
    pelicula = df.loc[df['title'] == titulo_de_la_filmacion] 

    if pelicula.empty:
        return{f'No se encontró la película con el título {titulo_de_la_filmacion}'} 
    
    titulo = pelicula['title'].values[0]
    votos=pelicula['vote_count'].values[0] 
    vavg=pelicula['vote_average'].values[0]
    
    if votos>2000:
        return{f'La pelicula {titulo} cuenta con {votos} valoraciones, con un puntaje promedio de {vavg}'} 
    else:
        return{'La pelicula cuenta con menos de 2000 votos'}
    
#funcion 5
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    
    columnas_actor = [col for col in df_actores.columns if 'Actor ' in col and 'Id' not in col] 
    
    melted_df = df_actores.melt(id_vars=['Id_Pelicula'], 
                        value_vars=columnas_actor, 
                        var_name='actor_column', 
                        value_name='nombre_actor')
    
    filtered_df = melted_df[melted_df['nombre_actor'] == nombre_actor] 

    if filtered_df.empty:
        return{'No se encontro el actor con ese nombre'}

    peliculas_aparicion_count = filtered_df['Id_Pelicula'].shape[0] 
    peliculas_aparicion = pd.DataFrame(filtered_df['Id_Pelicula'].unique(), columns=['Id_Pelicula']) 

    
    df_act = pd.merge(df, peliculas_aparicion, on='Id_Pelicula', how='inner') 
    avg_retorno=df_act['return'].mean() 
    retorno_total=df_act['return'].sum() 

    return{f'El actor {nombre_actor} aparece en {peliculas_aparicion_count} peliculas con un retorno total de {retorno_total} y retorno promedio de {avg_retorno}'}
    


#funcion 6
@app.get('/get_director/{director}')
def get_director(director:str):
    columnas_director = [col for col in df_directores.columns if 'Director ' in col and 'Id' not in col] 
    
    melted_df = df_directores.melt(id_vars=['Id_Pelicula'], 
                        value_vars=columnas_director, 
                        var_name='columna_director', 
                        value_name='nombre_director')
    
    filtered_df = melted_df[melted_df['nombre_director'] == director] 
    if filtered_df.empty:
        return{'No se econtro el director con ese nombre'}

    peliculas_aparicion_count = filtered_df['Id_Pelicula'].nunique() 
    peliculas_aparicion = pd.DataFrame(filtered_df['Id_Pelicula'].unique(), columns=['Id_Pelicula']) 

    
    df_dir = pd.merge(df, peliculas_aparicion, on='Id_Pelicula', how='inner') 
    retorno_total=df_dir['return'].sum() 
    
    peliculas_info = df_dir[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')

    return {f'{director} ha drigido {peliculas_aparicion_count} peliculas con un retorno total de {retorno_total} y sus peliculas con las siguientes: '},{"Peliculas dirigidas":peliculas_info}
