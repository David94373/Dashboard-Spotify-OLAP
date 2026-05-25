# Dashboard OLAP - Análisis de Spotify 2024

Este proyecto es un sistema interactivo de **Procesamiento Analítico en Línea (OLAP)** desarrollado con Python y Flask. Permite analizar, filtrar y visualizar las métricas de las canciones más escuchadas en plataformas de streaming (Spotify, YouTube, TikTok, Apple Music) durante el año 2024.

A través de 6 vistas diferentes, el sistema aplica operaciones clave de Business Intelligence como **Slice, Dice, Roll-Up, Drill-Down y Pivot** de manera dinámica.

## Requisitos Previos

Para ejecutar este proyecto en tu computadora, necesitas tener instalado lo siguiente:
- [Python 3.x](https://www.python.org/downloads/)
- Un navegador web moderno (Chrome, Edge, Firefox, Safari)

Además, el proyecto utiliza dos librerías externas de Python que deben ser instaladas:
- `flask` (Para el servidor y enrutamiento web)
- `pandas` (Para el procesamiento y análisis del dataset)

## Instrucciones de Ejecución

Sigue estos pasos para arrancar el servidor local y visualizar el dashboard:

**1. Descargar el proyecto**
Clona este repositorio o descarga el archivo `.zip` y extráelo en una carpeta de tu computadora.

**2. Abrir la terminal**
Abre una terminal (Símbolo del sistema, PowerShell o la terminal de tu editor de código) y navega hasta la carpeta raíz del proyecto (donde se encuentra el archivo `app.py`).

**3. Instalar las dependencias**
Ejecuta el siguiente comando en la terminal para instalar Flask y Pandas:
```bash
pip install flask pandas
