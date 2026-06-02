import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# =========================================================
# CONFIGURACIÓN VISUAL Y PALETA DE COLORES

COLOR_PRINCIPAL = "#E8A0B5"   
COLOR_SECUNDARIO = "#B39DDB"  
COLOR_ACCENTO = "#F48FB1"     
COLOR_FONDO_G = "#FFF8FA"     
LINEA_GUIA = "#E0E0E0"        

# Estilo base limpio para los gráficos
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = COLOR_FONDO_G

def mostrar_grafico(fig):
    fig.tight_layout()
    st.pyplot(fig)
    plt.show(block=False)
    plt.pause(0.1)

# =========================================================
# CONFIGURACIÓN DE PÁGINA (STREAMLIT)
# =========================================================
st.set_page_config(
    page_title="Estadísticas de Lenguas - Pando",
    page_icon="🌸",
    layout="wide"
)

# Inyección de CSS para personalizar las fuentes y el fondo
st.markdown("""
    <style>
    .main { background-color: #FAFAFA; }
    h1 { color: #D81B60 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700; }
    h2, h3 { color: #8E24AA !important; font-family: 'Segoe UI', sans-serif; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #666; }
    .stTabs [data-baseweb="tab"]:hover { color: #F48FB1; }
    .stTabs [aria-selected="true"] { color: #D81B60 !important; border-bottom-color: #D81B60 !important; }
    </style>
""", unsafe_allow_html=True)

# TITULO PRINCIPAL 
st.title("🌸 Análisis Estadístico: Lenguas Locales en Pando")
st.markdown("Bienvenidos al sistema de procesamiento de datos lingüísticos del departamento de Pando. Organizado, limpio y visual.")
st.markdown("---")

# =========================================================
# FASE 1: CARGA DE DATOS CSV
# =========================================================
df = pd.read_csv("lenguas_locales_pando.csv")
cantidad_datos = len(df)

# Impresión en Terminal 
print("\n====================================================")
print("                 BASE DE DATOS")
print("====================================================")
print(df)
print("\nCantidad total de registros =", cantidad_datos)

# CREAMOS LAS PESTAÑAS (TABS) PARA ORGANIZAR TODO EL CONTENIDO
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Vista General de Datos", 
    "📊 Análisis Cualitativo (Lenguas)", 
    "📈 Datos No Agrupados (Medidas)", 
    "🧮 Datos Agrupados (Sturges)"
])

# =========================================================
# PESTAÑA 1: VISTA GENERAL DE DATOS
# =========================================================
with tab1:
    st.header("📌 Fase 1: Carga y Exploración de Datos")
    
    col_info, col_vacia = st.columns([1, 2])
    with col_info:
        st.metric(label="Total de Registros Cargados", value=f"{cantidad_datos} filas", delta="¡Éxito!", delta_color="normal")
    
    st.subheader("📋 Datos Completos (Archivo CSV)")
    st.write("Explora las filas y columnas de las lenguas locales registradas en los municipios:")
    st.dataframe(df, use_container_width=True)

# =========================================================
# PESTAÑA 2: VARIABLES CUALITATIVAS (LENGUA)
# =========================================================
with tab2:
    st.header("📌 Fase 2: Distribución por Tipo de Lengua")
    st.write("Análisis cualitativo basado en la frecuencia en la que aparece cada lengua en el registro.")

    frecuencia_lengua = df["Lengua"].value_counts()
    tabla_cualitativa = pd.DataFrame({
        "Lengua": frecuencia_lengua.index,
        "fi": frecuencia_lengua.values
    })
    tabla_cualitativa["hi"] = tabla_cualitativa["fi"] / tabla_cualitativa["fi"].sum()
    tabla_cualitativa["hip"] = tabla_cualitativa["hi"] * 100
    tabla_cualitativa["Fi"] = tabla_cualitativa["fi"].cumsum()
    tabla_cualitativa["Hi"] = tabla_cualitativa["hi"].cumsum()
    tabla_cualitativa = tabla_cualitativa.round(4)

    print("\n====================================================")
    print("       TABLA DE FRECUENCIA CUALITATIVA")
    print("====================================================")
    print(tabla_cualitativa)

    st.subheader("📋 Tabla de Frecuencias Cualitativa")
    st.dataframe(tabla_cualitativa, use_container_width=True)

    # Gráficos lado a lado para que se vea ordenado y lindo
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("📊 Gráfico de Barras")
        fig1, ax1 = plt.subplots(figsize=(6, 4.5), dpi=110)
        barras = ax1.bar(
            tabla_cualitativa["Lengua"], tabla_cualitativa["fi"],
            color=COLOR_PRINCIPAL, edgecolor="#C2185B", linewidth=1.2
        )
        ax1.set_title("FRECUENCIA POR LENGUA", fontsize=11, fontweight="bold", color="#8E24AA")
        ax1.set_xlabel("Lenguas", fontsize=9)
        ax1.set_ylabel("Frecuencia (fi)", fontsize=9)
        ax1.grid(True, linestyle="--", alpha=0.5, color=LINEA_GUIA)
        plt.xticks(rotation=20, ha='right', fontsize=8)
        
        for barra in barras:
            altura = barra.get_height()
            ax1.text(barra.get_x() + barra.get_width()/2, altura + 0.1, str(int(altura)), ha='center', fontsize=8, fontweight='bold', color="#6A1B9A")
        mostrar_grafico(fig1)

    with col_graf2:
        st.subheader("📊 Gráfico de Torta / Porcentajes")
        fig2, ax2 = plt.subplots(figsize=(5, 5), dpi=110)
        colores_torta = [COLOR_PRINCIPAL, COLOR_SECUNDARIO, "#F8BBD0", "#E1BEE7", "#FFCDD2"]
        ax2.pie(
            tabla_cualitativa["fi"], labels=tabla_cualitativa["Lengua"],
            autopct="%1.1f%%", startangle=90,
            colors=colores_torta[:len(tabla_cualitativa)],
            textprops={'fontsize': 8, 'weight': 'bold'}
        )
        ax2.set_title("PARTICIPACIÓN PORCENTUAL", fontsize=11, fontweight="bold", color="#8E24AA")
        mostrar_grafico(fig2)

# =========================================================
# PESTAÑA 3: DATOS NO AGRUPADOS (MEDIDAS ESTADÍSTICAS)
# =========================================================
with tab3:
    st.header("📌 Fase 3: Análisis de Hablantes Estimados (Datos No Agrupados)")
    
    # Cálculos Estadísticos
    media = df["Hablantes_Estimados"].mean()
    mediana = df["Hablantes_Estimados"].median()
    moda = df["Hablantes_Estimados"].mode()[0]
    varianza = df["Hablantes_Estimados"].var()
    desviacion = df["Hablantes_Estimados"].std()
    valor_maximo_h = df["Hablantes_Estimados"].max()
    valor_minimo_h = df["Hablantes_Estimados"].min()
    rango_h = valor_maximo_h - valor_minimo_h

    
    st.subheader("🌸 Medidas Estadísticas Centrales y de Dispersión")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="Promedio (Media)", value=f"{media:,.2f}")
    with c2: st.metric(label="Mediana (Centro)", value=f"{mediana:,.1f}")
    with c3: st.metric(label="Moda (Más repetido)", value=f"{moda:,}")
    with c4: st.metric(label="Desviación Estándar", value=f"{desviacion:,.2f}")

    frecuencia_hablantes = df["Hablantes_Estimados"].value_counts().sort_index()
    tabla_discreta = pd.DataFrame({
        "Hablantes_Estimados": frecuencia_hablantes.index,
        "fi": frecuencia_hablantes.values
    })
    tabla_discreta["hi"] = tabla_discreta["fi"] / tabla_discreta["fi"].sum()
    tabla_discreta["hip"] = tabla_discreta["hi"] * 100
    tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()
    tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()
    tabla_discreta = tabla_discreta.round(4)

    tabla_medidas = pd.DataFrame({
        "Medida": ["Media", "Mediana", "Moda", "Varianza", "Desviación Estándar", "Valor Máximo", "Valor Mínimo", "Rango"],
        "Valor": [round(media, 4), round(mediana, 4), round(moda, 4), round(varianza, 4), round(desviacion, 4), valor_maximo_h, valor_minimo_h, rango_h]
    })

    print("\n====================================================")
    print("           MEDIDAS ESTADÍSTICAS")
    print("====================================================")
    print(tabla_medidas)

    col_t1, col_g1 = st.columns([1, 1.2])
    with col_t1:
        st.write("📋 **Tabla Completa de Medidas y Frecuencias:**")
        st.dataframe(tabla_medidas, use_container_width=True)
    with col_g1:
        st.write("📊 **Gráfico de Bastón:**")
        fig3, ax3 = plt.subplots(figsize=(6, 3.8), dpi=110)
        markerline, stemlines, baseline = ax3.stem(tabla_discreta["Hablantes_Estimados"], tabla_discreta["fi"])
        plt.setp(stemlines, linewidth=1.5, color=COLOR_SECUNDARIO)
        plt.setp(markerline, markersize=5, color=COLOR_ACCENTO)
        ax3.set_title("DISTRIBUCIÓN DE HABLANTES ESTIMADOS", fontsize=11, fontweight="bold", color="#8E24AA")
        ax3.set_xlabel("Cantidad de Hablantes", fontsize=9)
        ax3.set_ylabel("Frecuencia (fi)", fontsize=9)
        ax3.grid(True, linestyle="--", alpha=0.5, color=LINEA_GUIA)
        mostrar_grafico(fig3)

# =========================================================
# PESTAÑA 4: DATOS AGRUPADOS (INTERVALOS)
# =========================================================
with tab4:
    st.header("📌 Fase 4: Datos Agrupados bajo la Regla de Sturges")
    st.write("Cuando los datos varían mucho, se agrupan en rangos automáticos para entender mejor la población.")

    n = len(df["Hablantes_Estimados"])
    valor_maximo = df["Hablantes_Estimados"].max()
    valor_minimo = df["Hablantes_Estimados"].min()
    rango = valor_maximo - valor_minimo
    k = int(1 + 3.322 * np.log10(n))
    amplitud = int(np.ceil(rango / k))

    # Parámetros organizados de manera visual
    st.subheader("📋 Parámetros Calculados")
    p1, p2, p3, p4, p5 = st.columns(5)
    p1.markdown(f"**Total Datos (n):** {n}")
    p2.markdown(f"**Mínimo:** {valor_minimo}")
    p3.markdown(f"**Máximo:** {valor_maximo}")
    p4.markdown(f"**N° de Clases (k):** {k}")
    p5.markdown(f"**Amplitud:** {amplitud}")

    # Creación de intervalos y tabla final
    intervalos = pd.interval_range(start=valor_minimo, end=valor_maximo + amplitud, freq=amplitud)
    df["Intervalos"] = pd.cut(df["Hablantes_Estimados"], bins=intervalos)
    
    tabla_agrupada = df.groupby("Intervalos").size().reset_index(name="fi")
    tabla_agrupada["Intervalos_Texto"] = tabla_agrupada["Intervalos"].apply(lambda x: f"{int(x.left)} - {int(x.right)}")
    tabla_agrupada["Marca_Clase"] = tabla_agrupada["Intervalos"].apply(lambda x: (x.left + x.right) / 2)
    tabla_agrupada["hi"] = tabla_agrupada["fi"] / tabla_agrupada["fi"].sum()
    tabla_agrupada["hip"] = tabla_agrupada["hi"] * 100
    tabla_agrupada["Fi"] = tabla_agrupada["fi"].cumsum()
    tabla_agrupada["Hi"] = tabla_agrupada["hi"].cumsum()
    tabla_agrupada = tabla_agrupada.round(4)

    tabla_final = tabla_agrupada[["Intervalos_Texto", "Marca_Clase", "fi", "hi", "hip", "Fi", "Hi"]]

    print("\n====================================================")
    print("           TABLA DE DATOS AGRUPADOS")
    print("====================================================")
    print(tabla_final)

    st.subheader("📋 Tabla de Frecuencias de Datos Agrupados")
    st.dataframe(tabla_final, use_container_width=True)

    # Sección de gráficos avanzados
    st.subheader("📊 Galería de Gráficos de Distribución Continua")
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        st.write("**Histograma:**")
        fig4, ax4 = plt.subplots(figsize=(6, 3.8), dpi=110)
        ax4.hist(df["Hablantes_Estimados"], bins=k, color=COLOR_PRINCIPAL, edgecolor="#C2185B", alpha=0.8)
        ax4.set_title("HISTOGRAMA DE HABLANTES", fontsize=11, fontweight="bold", color="#8E24AA")
        ax4.set_xlabel("Rango de Hablantes", fontsize=9)
        ax4.set_ylabel("Frecuencia", fontsize=9)
        ax4.grid(True, linestyle="--", alpha=0.5, color=LINEA_GUIA)
        mostrar_grafico(fig4)

        st.write("**Histograma y Polígono de Frecuencias Combinado:**")
        fig6, ax6 = plt.subplots(figsize=(6, 3.8), dpi=110)
        ax6.hist(df["Hablantes_Estimados"], bins=k, color="#F8BBD0", edgecolor="#C2185B", alpha=0.6)
        ax6.plot(tabla_agrupada["Marca_Clase"], tabla_agrupada["fi"], marker="o", linewidth=2.5, color=COLOR_SECUNDARIO)
        ax6.set_title("HISTOGRAMA + POLÍGONO", fontsize=11, fontweight="bold", color="#8E24AA")
        ax6.grid(True, linestyle="--", alpha=0.5, color=LINEA_GUIA)
        mostrar_grafico(fig6)

    with g_col2:
        st.write("**Polígono de Frecuencia Solitario:**")
        fig5, ax5 = plt.subplots(figsize=(6, 3.8), dpi=110)
        ax5.plot(tabla_agrupada["Marca_Clase"], tabla_agrupada["fi"], marker="o", linewidth=2.5, color=COLOR_SECUNDARIO)
        ax5.set_title("POLÍGONO DE FRECUENCIA", fontsize=11, fontweight="bold", color="#8E24AA")
        ax5.set_xlabel("Marca de Clase", fontsize=9)
        ax5.set_ylabel("Frecuencia", fontsize=9)
        ax5.grid(True, linestyle="--", alpha=0.5, color=LINEA_GUIA)
        mostrar_grafico(fig5)

        st.write("**Ojiva (Frecuencia Acumulada):**")
        fig7, ax7 = plt.subplots(figsize=(6, 3.8), dpi=110)
        ax7.plot(tabla_agrupada["Marca_Clase"], tabla_agrupada["Fi"], marker="s", linewidth=2.5, color="#4DB6AC")
        ax7.set_title("OJIVA (FRECUENCIA ACUMULADA)", fontsize=11, fontweight="bold", color="#8E24AA")
        ax7.set_xlabel("Marca de Clase", fontsize=9)
        ax7.set_ylabel("Frecuencia Acumulada (Fi)", fontsize=9)
        ax7.grid(True, linestyle="--", alpha=0.5, color=LINEA_GUIA)
        mostrar_grafico(fig7)

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.markdown("---")
st.success("🌸 PROCESAMIENTO COMPLETO Y EJECUTADO CON ÉXITO")

print("\n====================================================")
print("      PROGRAMA EJECUTADO CORRECTAMENTE")
print("====================================================")

plt.ioff()
plt.show()