#TRABAJO FINAL APLICACION - 2024 - 2
#LIBRERIAS A USAR EN EL CODIGO
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from io import BytesIO

# Esto hace que la ruta sea relativa al SCRIPT, no a donde estés parado en la terminal
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
archivo_csv = os.path.join(carpeta_actual, "Tabla1.csv")
archivo_xlsx = os.path.join(carpeta_actual, "Tabla2.xlsx")

#PRINCIPALMENTE PARA LA PARTE DE ESTADISTICAS
from sklearn.linear_model import LinearRegression

#CREAMOS LA CLASE DONDE SE EFECTUARA TODAS LAS OPERACIONES
class AgriculturaData:
    #DECLARACION DEL CONSTRUCTOR
    def __init__(self, ruta_csv, ruta_excel):
        """Inicializa las rutas de los archivos CSV y Excel y lee los datos."""
        self.data_csv = pd.read_csv(ruta_csv)
        # Unificar la etiqueta inconsistente del archivo académico de entrada.
        self.data_csv["Cultivo"] = self.data_csv["Cultivo"].replace({"MaÍz": "Maiz"})
        self.data_excel = pd.read_excel(ruta_excel)
        #INFORMACION DE LOS ESTUDIANTES Y MUESTRA DE DATOS DE LAS TABLAS SELECCIONADAS
    def mostrar_datos(self):
        st.write("Trabajo Final CC201 / Ciclo 2024-02 / Sección: SX24")
        st.write("Integrantes:")
        st.write("\tDiego Joaquín Díaz Urday, Diego Alberto Aquino Chacara, Manuel Jesus Chavez Cuba")
        #TABLA NUMERO 1
        st.write("- - - - - - - - - - - - - - - - -")
        st.write("Archivo CSV:")
        st.dataframe(self.data_csv)
        #TABLA NUMERO 2
        st.write("Archivo Excel:")
        st.dataframe(self.data_excel)

        #GRAFICO DE PRODUCCION SEGUN AÑO
    def graf_produccion(self):
        df_csv = self.data_csv

        #AÑOS QUE AGREGARA EL USUARIO PARA COMPARACION (HAY FALLO SI NO TIENE SENTIDO - UN AÑO MAYOR A UNO MENOR)
        ano_a = st.sidebar.selectbox("Seleccione el Año A:", df_csv['Ano'].unique())
        ano_b = st.sidebar.selectbox("Seleccione el Año B:", df_csv['Ano'].unique())

        # Evitar intervalos invertidos y modificaciones sobre vistas de pandas.
        if ano_a > ano_b:
            st.warning("El año inicial debe ser menor o igual al año final.")
            return

        #FILTRADO DE LOS DATOS
        df_filtrado = df_csv[(df_csv['Ano'] >= ano_a) & (df_csv['Ano'] <= ano_b) & (df_csv['Cultivo'].isin(['Maiz', 'Papa']))].copy()

        #VERIFICA EL FORMATO ADECUADO DE LOS AÑOS
        df_filtrado['Ano'] = df_filtrado['Ano'].astype(str)

        #REALIZA LA GRAFICA DE LO QUE SOLICITE EL USUARIO
        plt.figure(figsize=(12, 6))

        #GRAFICA LA PRODUCCION DE MAIZ Y PAPA (uso de FORS)
        for cultivo in ['Maiz', 'Papa']:
            data_cultivo = df_filtrado[df_filtrado['Cultivo'] == cultivo]
            for region in data_cultivo['Region'].unique():
                data_region = data_cultivo[data_cultivo['Region'] == region]
                plt.plot(data_region['Ano'], data_region['Produccion'], marker='o', label=f'{cultivo} - {region}')
        #DECORACIONES PARA LA GRAFICA
        plt.title('Producción de Maíz y Papa por Región')
        plt.xlabel('Año')
        plt.ylabel('Producción')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        
        st.pyplot(plt)

    def export_consumo(self):
        df_excel = self.data_excel

        #AÑOS SOLICITADOS POR EL USUARIO (A Y B)
        ano_a = st.sidebar.selectbox("Seleccione el Año A para Arroz:", df_excel['Ano'].unique())
        ano_b = st.sidebar.selectbox("Seleccione el Año B para Arroz:", df_excel['Ano'].unique())

        if ano_a > ano_b:
            st.warning("El año inicial debe ser menor o igual al año final.")
            return

        #FILTRA LOS DATOS SEGUN LOS AÑOS SELECCIONADOS POR EL USUARIO
        df_filtrado_arroz = df_excel[(df_excel['Ano'] >= ano_a) & (df_excel['Ano'] <= ano_b) & (df_excel['Cultivo'] == 'Arroz')]

        #SELECCIONA LAS REGIONES A COMPARAR A SU ELECCION
        regiones = df_filtrado_arroz['Region'].unique()
        region1 = st.sidebar.selectbox("Seleccione la primera región:", regiones)
        region2 = st.sidebar.selectbox("Seleccione la segunda región:", regiones)

        # FILTRA LAS REGIONES SELECCIONADAS
        df_region1 = df_filtrado_arroz[df_filtrado_arroz['Region'] == region1]
        df_region2 = df_filtrado_arroz[df_filtrado_arroz['Region'] == region2]

        # CREACIOND EL DATAFRAME (pd.DataFrame)
        df_comparativo = pd.DataFrame({
            'Ano': df_region1['Ano'].tolist() + df_region2['Ano'].tolist(),
            'Region': [region1]*len(df_region1) + [region2]*len(df_region2),
            'Produccion': df_region1['Produccion'].tolist() + df_region2['Produccion'].tolist(),
            'Exportaciones': df_region1['Exportaciones'].tolist() + df_region2['Exportaciones'].tolist()
        })

        # GRAFICA
        df_comparativo.set_index('Ano', inplace=True)
        df_comparativo.pivot_table(index='Ano', columns='Region', values=['Produccion', 'Exportaciones']).plot(kind='bar', stacked=True, figsize=(12, 6))
        #DECORACIONES DEL GRAFICO
        plt.title('Comparación de Exportaciones y Producción de Arroz')
        plt.xlabel('Año')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid()
        
        st.pyplot(plt)
        #GRAFICA DE DISPERSION
    def graf_dispersión(self):
        df_csv = self.data_csv

        #SOLICITUD DE LA REGION AL USUARIO
        region_seleccionada = st.sidebar.selectbox("Seleccione la región para el gráfico de dispersión:", df_csv['Region'].unique())

        #FILTRACION DE LOS DATOS DE LA REGION SELECCIONADA
        df_region = df_csv[df_csv['Region'] == region_seleccionada]

        #AREA COSECHADA Y PRODUCCION TOTAL (GRAFICO DE ESTOS 2)
        plt.figure(figsize=(12, 6))
        plt.scatter(df_region['Area Cosechada'], df_region['Produccion'], color='blue', alpha=0.5)
        plt.title(f'Relación entre Área Cosechada y Producción Total en {region_seleccionada}')
        plt.xlabel('Área Cosechada')
        plt.ylabel('Producción Total')
        plt.grid()

        st.pyplot(plt)

    def graf_pastel(self):
        df_csv = self.data_csv

        #SOLICITA LOS AÑOS AL USUARIO
        ano_seleccionado = st.sidebar.selectbox("Seleccione el año para el gráfico de pastel:", df_csv['Ano'].unique())

        #FILTRACION DE LOS DATOS SELECCIONADOS
        df_año = df_csv[df_csv['Ano'] == ano_seleccionado]

        #SUMA PRODUCCION POR REGION
        produccion_por_region = df_año.groupby('Region')['Produccion'].sum()

        #SOLICITUD DE LA REGION SELECCIONADA
        region_seleccionada = st.sidebar.selectbox("Seleccione la región para comparar:", df_año['Region'].unique())

        #PRODUCCIOND DE LA REGION SELECCIONADA
        produccion_region_seleccionada = produccion_por_region[region_seleccionada]

        #PRODUCCION TOTAL 
        produccion_total = produccion_por_region.sum()

        # DATA FRAME PARA EL GRAFICO (PASTEL)
        datos_pastel = pd.Series({
            region_seleccionada: produccion_region_seleccionada,
            'Otras Regiones': produccion_total - produccion_region_seleccionada
        })

        # GRAFICAR Y DECORACIONES
        plt.figure(figsize=(8, 8))
        plt.pie(datos_pastel, labels=datos_pastel.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Distribución de Producción en {region_seleccionada} respecto a Otras Regiones para el Año {ano_seleccionado}')
        plt.axis('equal') #ESTO PERMITE QUE LA GRAFICA SE MUESTRE DE MANERA CIRCULAR

        st.pyplot(plt)
        #LAS ESTADISTICAS  PRINCIPALES COMO TENDENCIA CENTRAL, DISPERSION, ETC SEGUN EL PRODUCTO QUE ELIJA EL USUARIO
    def calcular_est(self):
        df_csv = self.data_csv

        #SOLICITUD DEL CULTIVO AL USUARIO
        cultivo_seleccionado = st.sidebar.selectbox("Seleccione el cultivo para estadísticas:", df_csv['Cultivo'].unique())

        # FILTRACIOND E LOS DAATOS SELECCIONADOS (CULTIVOS)
        df_cultivo = df_csv[df_csv['Cultivo'] == cultivo_seleccionado]

        #OPCIONES DE TENDENCIA CENTRAL Y SUS CALCULOS
        media = df_cultivo['Produccion'].mean()
        mediana = df_cultivo['Produccion'].median()
        moda = df_cultivo['Produccion'].mode()[0]

        # OPCIONES DE MEDIDAS DE DISPERSION Y SUS CALCULOS
        varianza = df_cultivo['Produccion'].var()
        desviacion_estandar = df_cultivo['Produccion'].std()
        rango_intercuartilico = df_cultivo['Produccion'].quantile(0.75) - df_cultivo['Produccion'].quantile(0.25)

        #DECORACION PARA MOSTRAR LAAS ESTADISTICAS
        st.write(f"**Estadísticas para {cultivo_seleccionado}:**")
        st.write(f"Media: {media}")
        st.write(f"Mediana: {mediana}")
        st.write(f"Moda: {moda}")
        st.write(f"Varianza: {varianza}")
        st.write(f"Desviación Estándar: {desviacion_estandar}")
        st.write(f"Rango Intercuartílico: {rango_intercuartilico}")

        #AHORA CALCULO DE LA CORRELACION Y LA VARIANZA
        correlacion = df_cultivo['Area Cosechada'].corr(df_cultivo['Produccion'])
        covarianza = df_cultivo['Area Cosechada'].cov(df_cultivo['Produccion'])

        st.write(f"**Correlación entre Área Cosechada y Producción:** {correlacion}")
        st.write(f"**Covarianza entre Área Cosechada y Producción:** {covarianza}")

        #LIBRERIA PARA LA REGRESION LINEAL (LinearRegression())
        X = df_cultivo[['Area Cosechada']]
        y = df_cultivo['Produccion']
        modelo = LinearRegression()
        modelo.fit(X, y)
        pendiente = modelo.coef_[0]
        intercepto = modelo.intercept_

        st.write(f"**Modelo de Regresión Lineal:** Producción = {pendiente} * Área Cosechada + {intercepto}")

        #PERMITE VISUALIZAR LA GRAFICA DE LO SOLICITADO
        plt.figure(figsize=(10, 6))
        plt.hist(df_cultivo['Produccion'], bins=10, color='skyblue', edgecolor='black')
        plt.title(f'Distribución de Producción para {cultivo_seleccionado}')
        plt.xlabel('Producción')
        plt.ylabel('Frecuencia')
        plt.grid()
        st.pyplot(plt)
        #EXPORTACION DE DATOS SEGUN EL USUARIO DESEE, SI CSV O EXCEL Y SE GUARDA EN EL ARCHIVO...
    def exportar_data(self):
        """Entregar los datos al navegador sin escribir en el servidor."""
        formato = st.sidebar.selectbox("Seleccione el formato de exportación:", ["CSV", "Excel"])
        if formato == "CSV":
            datos = self.data_csv.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Descargar datos CSV", data=datos,
                file_name="produccion_agricola.csv", mime="text/csv"
            )
        else:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                self.data_excel.to_excel(writer, sheet_name="Exportaciones", index=False)
            st.download_button(
                "Descargar datos Excel", data=buffer.getvalue(),
                file_name="exportaciones_agricolas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

#FUNCION MENU PAR EL TRABAJO
    def menu(self):
        #TITULO Y OPCIONES
        st.title("-ProductísticoPE-")
        opcion = st.sidebar.selectbox("Seleccione los datos a mostrar:", ["Ver Datos CSV y Excel", "Gráfico de Producción", 
                                                                          "Gráfico de Exportaciones y Consumo", "Gráfico de Dispersión",
                                                                          "Gráfico Pastel", "Estadísticas", "Exportar Datos"])
        #OPCIONES A ELEGIR PARA EL USUARIO 
        match(opcion):
            case "Ver Datos CSV y Excel":
                self.mostrar_datos()
            case "Gráfico de Producción":
                self.graf_produccion()
            case "Gráfico de Exportaciones y Consumo":
                self.export_consumo()
            case "Gráfico de Dispersión":
                self.graf_dispersión()
            case "Gráfico Pastel":
                self.graf_pastel()
            case "Estadísticas":
                self.calcular_est()
            case "Exportar Datos":
                self.exportar_data()

#CREACION DEL MENU Y DE LA "APP" ADEMAS DE INGRESO DE LAS TABLAS 1 Y 2
if __name__ == "__main__":
    #TABLA1-CSV TABLA2-EXCEL
    app = AgriculturaData(archivo_csv, archivo_xlsx)
    app.menu()