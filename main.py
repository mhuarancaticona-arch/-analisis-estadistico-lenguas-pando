import os
import pandas as pd

def verificar_proyecto():
    print("====================================================")
    print("🌸 VALIDACIÓN DEL PROYECTO ESTADÍSTICO - PANDO 🌸")
    print("====================================================")
    
    archivo_csv = "lenguas_locales_pando.csv"
    
    # Verificar si el dataset existe en la carpeta
    if os.path.exists(archivo_csv):
        print(f"✅ ¡Excelente! El archivo '{archivo_csv}' fue detectado con éxito.")
        df = pd.read_csv(archivo_csv)
        print(f"📊 Registros totales encontrados: {len(df)}")
        print("\n✨ Para iniciar la aplicación web visual con los gráficos pasteles,")
        print("   ejecuta en la terminal: streamlit run app_estadistica.py")
    else:
        print(f"❌ ERROR: No se encuentra el archivo '{archivo_csv}' en esta carpeta.")
        print("   Asegúrate de que el nombre esté escrito exactamente igual.")
    
    print("====================================================")

if __name__ == "__main__":
    verificar_proyecto()