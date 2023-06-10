from fastapi import FastAPI
import pandas as pd 
import unicodedata as uni
from fastapi.encoders import jsonable_encoder



app = FastAPI(title="Información de películas")

#http://127.0.0.1:8000

@app.on_event("startup")
async def load_dataframe():
    global df
    df = pd.read_csv("final_clean.csv", parse_dates=['release_date'], date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

@app.get('/cantidad_filmaciones')
def cantidad_filmaciones(x: str): 
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
    de películas estrenadas en ese dia
    x = string del día en español
    return = entero numero de películas
    """
    import unicodedata as uni
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia = dia.lower()
    dia = uni.normalize('NFKD', dia).encode('ASCII', 'ignore').decode('utf-8')
    if dia in dias:
        total_films = pd.DataFrame({"dia":df["release_date"].dt.day_name(locale="es_ES")})
        total_films['dia'] = total_films['dia'].apply(lambda x: uni.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8').lower())
        total = total_films[total_films['dia'] == dia]
        total_final = total.shape[0]
        return {"dia": dia, "cantidad": total_final}
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
