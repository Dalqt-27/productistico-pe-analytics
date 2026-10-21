# ProductísticoPE | Analítica agrícola en Python

Aplicación académica desarrollada en equipo para explorar datos agrícolas mediante **Streamlit, pandas, matplotlib y scikit-learn**. Permite analizar tablas CSV/Excel, visualizar producción por año y región, calcular estadísticos y ajustar una regresión lineal simple exploratoria.

## Ejecutar en Windows

Requisitos: Python **3.10 o posterior**. Desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Si PowerShell no permite activar el entorno virtual, se puede usar directamente `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` y `.\.venv\Scripts\python.exe -m streamlit run app.py`.

## Funciones

- Lectura de `Tabla1.csv` y `Tabla2.xlsx`.
- Gráficos de líneas, barras, dispersión, sectores e histogramas.
- Estadísticas descriptivas, correlación y covarianza.
- Modelo de regresión lineal **exploratorio**; no se ha validado su capacidad predictiva fuera de los datos usados para ajustarlo.
- Descarga de CSV y Excel mediante el navegador.

## Datos y alcance

Los archivos de entrada son los provistos en el trabajo de clase. **La procedencia y la correspondencia con series oficiales del INEI no se han verificado**. No se deben presentar como cifras oficiales ni como un sistema de pronóstico de producción validado. La cadena `MaÍz` se normaliza a `Maiz` en tiempo de ejecución para que los filtros sean coherentes.

## Posibles mejoras

Filtrar años con controles más amigables; agregar métricas MAE/RMSE/R² con partición de entrenamiento y prueba; documentar unidades, fuentes y metodología de los datos.

## Créditos

Proyecto grupal desarrollado para Programación Orientada a Objetos en la UPC. Autores originales indicados en el trabajo: Diego Joaquín Díaz Urday, Diego Alberto Aquino Chaccara y Manuel Jesús Chávez Cuba. Confirmar autorización del equipo antes de difundir públicamente.
