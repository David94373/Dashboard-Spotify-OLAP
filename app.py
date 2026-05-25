from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Ruta del archivo CSV (debe estar en la misma carpeta que app.py)
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Most_Streamed_Spotify_Songs_2024.csv")

def cargar_datos():
    df = pd.read_csv(CSV_PATH, encoding="latin-1")
    # Limpiar números que vienen con comas (ej: "1,000,000")
    for col in ["Spotify Streams", "Spotify Playlist Count", "Apple Music Playlist Count",
                "YouTube Views", "TikTok Views", "Shazam Counts", "Track Score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce").fillna(0)
    return df

# ── Páginas ────────────────────────────────────────────────────────────────────
@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/vista1")
def vista1():
    return render_template("vista1.html")

@app.route("/vista2")
def vista2():
    return render_template("vista2.html")

@app.route("/vista3")
def vista3():
    return render_template("vista3.html")

@app.route("/vista4")
def vista4():
    return render_template("vista4.html")

@app.route("/vista5")
def vista5():
    return render_template("vista5.html")

# ── APIs de datos ──────────────────────────────────────────────────────────────

# Vista 1: Top 10 canciones con más streams
@app.route("/api/top10")
def top10():
    df = cargar_datos()
    datos = df[["Track", "Artist", "Spotify Streams"]].sort_values("Spotify Streams", ascending=False).head(10)
    return jsonify(datos.to_dict(orient="records"))

# Vista 2: Comparar Spotify vs YouTube vs TikTok
@app.route("/api/plataformas")
def plataformas():
    df = cargar_datos()
    datos = df[["Track", "Artist", "Spotify Streams", "YouTube Views", "TikTok Views"]].sort_values("Spotify Streams", ascending=False).head(8)
    return jsonify(datos.to_dict(orient="records"))

# Vista 3: Cuántas canciones tiene cada artista (top 8 artistas)
@app.route("/api/artistas")
def artistas():
    df = cargar_datos()
    datos = df.groupby("Artist")["Spotify Streams"].sum().reset_index()
    datos.columns = ["Artist", "Total"]
    datos = datos.sort_values("Total", ascending=False).head(8)
    return jsonify(datos.to_dict(orient="records"))

# Vista 4: Streams por mes de lanzamiento
@app.route("/api/meses")
def meses():
    df = cargar_datos()
    df["Mes"] = pd.to_datetime(df["Release Date"], errors="coerce").dt.month
    nombres = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
               7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
    datos = df.groupby("Mes")["Spotify Streams"].sum().reset_index()
    datos["Mes"] = datos["Mes"].map(nombres)
    return jsonify(datos.to_dict(orient="records"))

# Vista 5: Top 5 canciones más populares en playlists
@app.route("/api/playlists")
def playlists():
    df = cargar_datos()
    datos = df[["Track", "Artist", "Spotify Playlist Count", "Apple Music Playlist Count"]].sort_values("Spotify Playlist Count", ascending=False).head(5)
    datos.columns = ["Track", "Artist", "Spotify", "Apple"]
    return jsonify(datos.to_dict(orient="records"))

# Vista 6: Consulta personalizable (Interfaz HTML)
@app.route("/vista6")
def vista6():
    return render_template("vista6.html")

@app.route("/api/consulta_dinamica", methods=["POST"])
def consulta_dinamica():
    parametros = request.json
    agrupar_por = parametros.get("agrupar_por", "Artist") 
    metrica = parametros.get("metrica", "Spotify Streams")
    limite = int(parametros.get("limite", 10))
    filtro_tiempo = parametros.get("filtro_tiempo", "todos") # NUEVO

    df = cargar_datos()

    # --- Procesamiento de fechas ---
    df["Fecha_Real"] = pd.to_datetime(df["Release Date"], errors="coerce")
    df["Mes Num"] = df["Fecha_Real"].dt.month.fillna(0).astype(int)
    
    nombres_meses = {
        1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio",
        7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"
    }
    df["Mes de Lanzamiento"] = df["Mes Num"].map(nombres_meses)
    df["Año de Lanzamiento"] = df["Fecha_Real"].dt.year.fillna(0).astype(int)

    # --- Aplicar el filtro de tiempo si el usuario eligió un mes específico ---
    if filtro_tiempo != "todos":
        df = df[df["Mes de Lanzamiento"] == filtro_tiempo]

    # Agrupar y sumar dinámicamente
    datos = df.groupby(agrupar_por)[metrica].sum().reset_index()
    
    # Ordenar de mayor a menor y limitar la cantidad de resultados
    datos = datos.sort_values(metrica, ascending=False).head(limite)
    
    return jsonify(datos.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
