from fastapi import FastAPI
import pandas as pd 
import unicodedata as uni
from fastapi.encoders import jsonable_encoder
from unidecode import unidecode


app = FastAPI(title="Información de películas")

#http://127.0.0.1:8000

@app.on_event("startup")
async def load_dataframe():
    global df
    df = pd.read_csv("final_clean.csv", parse_dates=['release_date'], date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

@app.get('/peliculas_idioma')
def peliculas_idioma(idioma: str):
    """
    Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). 
    Debe devolver la cantidad de películas producidas en ese idioma.
    """
    idioma = idioma.capitalize()
    total_films = df[df['name_language'] == idioma]
    total = total_films.shape[0]
    return {"Idioma": idioma, "cantidad": total}
@app.get('/peliculas_duración')
def peliculas_duración(pelicula:str):
    """
    Se ingresa una pelicula. Debe devolver la la duracion y el año.
    """
    pelicula = pelicula.lower()
    if pelicula in df["title"].str.lower().values:
        year = df.loc[df["title"].str.lower() == pelicula, "release_year"].values[0]
        duration = df.loc[df["title"].str.lower() == pelicula, "runtime"].values[0]
        return jsonable_encoder({"titulo": pelicula, "anio": int(year), "duración": float(duration)})
    else:
        return None
@app.get('/franquicia')
def franquicia(franquicia:str):
    """
    Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
    """
    df["name_collec"] = df["name_collec"].fillna("")
    reveneu = []
    peliculas = []
    for index, row in df.iterrows():
        if franquicia in row["name_collec"]:
            peliculas.append(row['title'])
            reveneu.append(row["revenue"])
        else: 
            continue 
    new_retorno = [valor for valor in reveneu if valor != 0]
    reveneu_final = sum(new_retorno)
    if len(peliculas) > 1:
        return {'Franquicia':franquicia, 'cantidad_filmaciones':len(peliculas), 'Ganancia Total':reveneu_final}
    else: 
        return print("Franquicia sin registros")

@app.get('/peliculas_pais')
def peliculas_pais(pais:str):
    """
    Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), 
    retornando la cantidad de peliculas producidas en el mismo.
    """
    total_films = df[df['name_country'] == pais]
    total = total_films.shape[0]
    return {"País": pais, "cantidad": total}

@app.get('/productora')
def productora(productora:str):
    """
   Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.
    """
    retorno = []
    peliculas = []
    for index, row in df.iterrows():
        if productora in row["productor"]:
            peliculas.append(row['title'])
            retorno.append(row["return"])
        else: 
            continue 
    new_retorno = [valor for valor in retorno if valor != 0]
    retorno_final = sum(new_retorno)
    if len(peliculas) > 1:
        return {'Productora':productora, 'cantidad_filmaciones':len(peliculas), 'retorno_total':retorno_final}
    else: 
        return print("Productora sin registros")
    
@app.get('/cantidad_filmaciones_mes')
def cantidad_filmaciones_mes(x: str): 
    """"
    x = Recibe como argumentos un string con el nombre del mes en español
    return = devuelve el número de películas que se estrenaron en ese mes
    """
    y = x
    x = x.lower() 
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"] 
    if x in months:
        x = months.index(x) + 1
    else:
        print("El mes ingresado no es válido")
    
    total_films = df[df['release_date'].dt.month == x]
    total = total_films.shape[0]
    return {"mes": y, "cantidad": total}

@app.get('/cantidad_filmaciones_dia')
def cantidad_filmaciones_dia(dia: str):
    """"
    Esta función recibe como parámetro un día en español y devuelve el número
    de películas estrenadas en ese día
    x = string del día en español
    return = entero número de películas
    """
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    dia = dia.lower()
    dia = unidecode(dia)
    if dia in dias:
        total_films = pd.DataFrame({"dia": df["release_date"].dt.day_name()})
        total_films['dia'] = total_films['dia'].apply(lambda x: unidecode(x.lower()))
        total = total_films[total_films['dia'] == dia]
        total_final = total.shape[0]
        return {"dia": dia, "cantidad": int(total_final)}
    else:
        print("El día ingresado no es válido")

@app.get('/score_titulo')
def score_titulo(nombre: str):
    """""
    Esta función recibe un string del nombre de una película y devuelve un string indicando 
    el año en que fue estrenada, y su popularidad
    """
    nombre = nombre.lower()
    if nombre in df["title"].str.lower().values:
        year = df.loc[df["title"].str.lower() == nombre, "release_year"].values[0]
        score = df.loc[df["title"].str.lower() == nombre, "popularity"].values[0]
        return jsonable_encoder({"titulo": nombre, "anio": int(year), "popularidad": float(score)})
    else:
        return None

@app.get('/votos_titulo')
def votos_titulo(titulo):
    """"
    Esta función recibe como parámetro un título de una película y retorna
    un string donde se menciona el año de estreno, el total de votos y su promedio
    """
    titulo = titulo.lower()
    if titulo in df["title"].str.lower().values:
        year = df.loc[df["title"].str.lower() == titulo, "release_year"].values[0]
        votes = df.loc[df["title"].str.lower() == titulo, "vote_count"].values[0]
        average = df.loc[df["title"].str.lower() == titulo, "vote_average"].values[0]
        if votes >= 2000:
            return {'titulo':titulo, 'anio':int(year), 'voto_total':float(votes), 'voto_promedio':float(average)}
        else:
            return print("La película no tiene al menos 2000 votos")

@app.get('/get_actor')
def get_actor(nombre_actor: str):
    """"
    Esta función recibe como parámetro el nombre de un actor
    y devuelve un string con el nombre del actor, el número de filmaciones en las que ha participado,
    el retorno total que han tenido estas películas y el promedio de retorno del actor
    """
    retorno = []
    peliculas = []
    for index, row in df.iterrows():
        if nombre_actor in row["actors"]:
            peliculas.append(row['title'])
            retorno.append(row["return"])
        else: 
            continue 
    retorno_sum = sum(retorno)
    new_retorno = [valor for valor in retorno if valor != 0]
    retorno_final = sum(new_retorno)
    if len(peliculas) > 1:
        
        promedio = retorno_final/len(new_retorno)
        return {'actor':nombre_actor, 'cantidad_filmaciones':len(peliculas), 'retorno_total':retorno_final, 'retorno_promedio':promedio}
    else: 
        return print("Actor sin registros")

@app.get('/get_director')
def get_director(nombre_director):
    retorno = []
    peliculas = []
    indice = []
    for index, row in df.iterrows():
        if nombre_director in row["directors"]:
            peliculas.append(row['title'])
            retorno.append(row["return"])
            indice.append(index)
        else: 
            continue 
    new_retorno = [valor for valor in retorno if valor != 0]
    retorno_final = sum(new_retorno)
    retorno_sum = sum(retorno)
    
    if len(peliculas) > 1:
        promedio = retorno_final/len(new_retorno)
        peliculas_seleccionadas = df.loc[indice]
        peliculas_part = []
        fecha_lanzamiento = []
        retorno = []
        costo = []
        reveneu = []
        for _, fila in peliculas_seleccionadas.iterrows():
            peliculas_part.append(fila["title"])
            fecha_lanzamiento.append(fila["release_date"])
            reveneu.append(fila["revenue"])
            costo.append(fila["budget"])
            retorno.append(fila["return"])
              
        return {'director':nombre_director, 'retorno_total_director':retorno_final, 
    'peliculas':peliculas_part, 'anio':fecha_lanzamiento, 'retorno_pelicula':retorno, 
    'budget_pelicula':costo, 'revenue_pelicula':reveneu}

    else: 
        print("Director sin registros")
        return None
