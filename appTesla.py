# Importacion de scripts
from NoticiasTesla import menuNoticias
from teslaEntrenamiento import menuEntrenamiento
from prediccionTesla import main_prediccion
from BotOperaciones import main_bot

# Importacion de librerias
import streamlit as st
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ngrok http 8501 --basic-auth="Kleincorp:kleinlytics"

if 'valor' not in st.session_state:
    st.session_state.valor = 2  # Inicializar con un valor por defecto, como 2

if 'prediccion' not in st.session_state:
    st.session_state.prediccion = [0]  # Inicializar con un valor por defecto, como 0


def graficas(precios_cierre, dias):
    # Usar un estilo disponible y adecuado
    # st.write(precios_cierre.run(window=10)) #ver documentacion para hacer mejores graficas

    plt.style.use('seaborn-v0_8-darkgrid')

    # Crear la figura y el eje para más control
    fig, ax = plt.subplots(figsize=(10, 5))

    # Dibujar la gráfica con personalizaciones
    ax.plot(precios_cierre, marker='o', markersize=5, linestyle='-', color='royalblue', linewidth=2)

    # Personalizar el título y las etiquetas
    ax.set_title(f"Precios de Cierre de Tesla a lo Largo de {dias} dias", fontsize=14, fontweight='bold')
    ax.set_xlabel("Días", fontsize=12)
    ax.set_ylabel("Precio de Cierre ($)", fontsize=12)

    # Configurar los marcadores del eje X para que muestren enteros
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)


def calcular_cantidad(diferencia, sentimiento):
    # Normaliza los valores (puedes ajustar los rangos según tus necesidades)
    factor_precio = (diferencia - min(st.session_state.prediccion)) / (
                max(st.session_state.prediccion) - min(st.session_state.prediccion))
    factor_sentimiento = (sentimiento + 1) / 2  # Convertir de rango -1 a 1 a rango 0 a 1

    # Calcula un promedio ponderado para la cantidad
    cantidad = (factor_precio + factor_sentimiento) / 2

    # Estrategia de inversión combinada
    if diferencia > 0 and sentimiento > 0:
        cantidad = 3
        accion = 1
    elif diferencia > 0 and sentimiento < 0:
        cantidad = 1
        accion = 1
    elif diferencia < 0 and sentimiento > 0:
        cantidad = 1
        accion = 0
    elif diferencia < 0 and sentimiento < 0:
        cantidad = 3
        accion = 0
    else:
        cantidad = 0
        accion = 2

    return cantidad, accion


def bot_operaciones():
    estado = 1
    espaciador_izquierda, col_central, espaciador_derecha = st.columns([1, 2, 1])
    # Botón para ejecutar el bot
    with col_central:
        if st.button("Activar Bot"):
            with st.spinner('Ejecutando... Por favor, espera.'):
                if st.session_state.valor != 2 and st.session_state.prediccion[0] != 0:

                    diferencia = st.session_state.prediccion[-1] - st.session_state.prediccion[
                        0]  # calcular si baja o sube el precio
                    cantidad, accion = calcular_cantidad(diferencia,
                                                         st.session_state.valor)  # calcular la cantidad a invertir y la accion a realizar

                    #estado = main_bot(cantidad, accion)  # mandar al bot las ordenes (Llamada al bot)

                    if estado == 0:
                        st.write("Error: no se ha podido conectar con el servidor web")
                    else:
                        accion_text = "Compra" if accion != 0 else "Venta"  # mostrar al cliente la accion de manera visual

                        st.success(
                            f'{accion_text} de {cantidad} acciones realizada con exito!')  # confirmar la compra o venta y la cnatidad de esta
                else:
                    #menuNoticias()  # scraper de noticias
                    time.sleep(1)
                    sentimientoNoticias = menuEntrenamiento()  # realizar analisis de sentimineto

                    prediccionPrecios = main_prediccion(5)  # hacer prediccion de precios a 5 dias

                    diferencia = prediccionPrecios[-1] - prediccionPrecios[0]  # calcular si baja o sube el precio
                    cantidad, accion = calcular_cantidad(diferencia,
                                                         sentimientoNoticias)  # calcular la cantidad a invertir y la accion a realizar

                    #estado = main_bot(cantidad, accion)  # mandar al bot las ordenes (Llamada al bot)

                    if estado == 0:
                        st.write("Error: no se ha podido conectar con el servidor web")
                    else:
                        accion_text = "Compra" if accion != 0 else "Venta"  # mostrar al cliente la accion de manera visual

                        st.success(
                            f'{accion_text} de {cantidad} acciones realizada con exito!')  # confirmar la compra o venta y la cnatidad de esta


def sentimiento_noticias():
    espaciador_izquierda, col_central, espaciador_derecha = st.columns([1, 2, 1])
    # Botón para ejecutar el analisi de sentimiento
    with col_central:
        if st.button("Analizar Noticias"):
            with st.spinner('Ejecutando... Por favor, espera.'):
                # menuNoticias()  # scraper de noticias
                time.sleep(1)
                st.session_state.valor = menuEntrenamiento()  # realizar analisis de sentimineto
                if st.session_state.valor > 0.4:
                    sentimiento = "Positivo"
                elif st.session_state.valor < -0.4:
                    sentimiento = "Negativo"
                else:
                    sentimiento = "Neutro"

            # Establecer el estilo del texto
            estilo_texto = f"color: white; font-size: larger; font-weight: bold"

            st.markdown(f"<p style='{estilo_texto}'>{sentimiento} con un {st.session_state.valor}</p>", unsafe_allow_html=True)
            # mostrar al cliente el sentimiento y la puntuacion


def prediccion_precio():
    espaciador_izquierda, col_central, espaciador_derecha = st.columns([1, 2, 1])
    hayDatos = 0
    with col_central:
        dias_predecir = st.number_input('Número de días a predecir', min_value=1, max_value=75,
                                        value=10)  # dejar que el cliente decida los dias a predecir

    with col_central:
        if st.button("Predecir Precio"):
            with st.spinner('Ejecutando... Por favor, espera.'):
                st.session_state.prediccion = main_prediccion(int(dias_predecir))  # predecir los precios a x dias
                hayDatos = 1

    if hayDatos == 1:
        graficas(st.session_state.prediccion, dias_predecir)  # mostrar la grafica con la evolucion del precio


# menu lateral para selección
opcion = st.sidebar.selectbox("Elige una opción:",
                              ["Inicio", "Prediccion Precio", "Análisis de Sentimiento", "Bot de Trading Automático",
                               "Proyección a Futuro"])

# limpia la pagina antes de mostrar el contenido seleccionado
st.empty()

if opcion == "Inicio":
    st.title("Bienvenido a KleinLytics")

    # Usando Markdown para un formato mejorado
    st.markdown("""
    ## Instrucciones para el Uso del Sistema

    Bienvenido a Tesla Market Analytics, tu plataforma avanzada para análisis y predicción del valor de mercado de Tesla. Aquí te guiaremos a través de las siguientes funcionalidades clave:

    - **Predicción de Precio:** Utiliza el modelo XGBOOST para predecir cómo se moverá la gráfica del mercado de Tesla en el futuro. Esta herramienta analiza tendencias y patrones para ofrecer estimaciones valiosas.

    - **Análisis de Sentimiento de Noticias:** Realiza un scrapeo de las últimas noticias sobre Tesla y las analiza mediante un modelo de análisis de sentimiento previamente entrenado. Esto te proporciona una comprensión profunda de cómo las noticias actuales pueden influir en el mercado de Tesla.

    - **Bot de Operaciones Automáticas:** Basado en los resultados obtenidos de las predicciones y el análisis de sentimientos, este bot opera automáticamente en el mercado, comprando o vendiendo acciones de Tesla según las oportunidades identificadas.

    **Comienza explorando cada funcionalidad desde el menú lateral para entender y capitalizar las tendencias del mercado de Tesla.**
    """, unsafe_allow_html=True)

elif opcion == "Prediccion Precio":
    st.title("Predicción de Precio de Tesla")

    st.markdown("""
    ### Predicción de Tendencias de con XGBOOST

    Utiliza tecnologías avanzadas de Machine Learning, específicamente el modelo XGBOOST, para predecir el movimiento futuro de los precios de las acciones de Tesla. Esta herramienta te proporcionará una estimación basada en patrones históricos y tendencias actuales del mercado.

    **Instrucciones:**
    - **Selecciona la Cantidad de Días:** Elige el número de días hacia el futuro para los cuales quieres predecir el precio de las acciones. Ten en cuenta que, aunque el modelo puede predecir para varios días en el futuro, la precisión puede disminuir cuanto más lejos se proyecte la predicción.
    - **Haz clic en 'Predecir Precio':** Una vez ingresados los parámetros, haz clic en este botón para ver las estimaciones del modelo.

    """)

    prediccion_precio()

elif opcion == "Análisis de Sentimiento":
    st.title("Análisis de Sentimiento")
    st.markdown("""
    ### Análisis de Sentimiento de las Últimas Noticias sobre Tesla

    Esta herramienta analiza el sentimiento de las últimas noticias relacionadas con Tesla para proporcionarte una perspectiva sobre cómo las noticias pueden estar afectando la percepción del mercado.

    **Cómo se Interpreta el Resultado:**
    - El resultado del análisis de sentimiento fluye entre -1 y 1.
    - **Positivo (0.5 a 1):** Noticias mayormente positivas, indicando una percepción favorable en el mercado.
    - **Neutro (-0.5 a 0.5):** Sentimiento neutral, indicando un equilibrio en las percepciones del mercado.
    - **Negativo (-0.5 a -1):** Noticias mayormente negativas, lo que podría indicar una percepción desfavorable en el mercado.


    **Instrucciones:**
    - Haz clic en 'Analizar' para recopilar y analizar las últimas noticias sobre Tesla.
    """)

    sentimiento_noticias()


elif opcion == "Bot de Trading Automático":
    st.title("Bot de Operaciones Automáticas")

    st.markdown("""
    ### Bot Automatizado para Operar en el Mercado de Tesla

    Este bot aprovecha la información obtenida de las predicciones de precios y el análisis de sentimiento para tomar decisiones de inversión en el mercado de acciones de Tesla de manera autónoma.

    **Características del Bot:**
    - **Automatización Completa:** No es necesario configurar manualmente el bot. Si no se han ejecutado los pasos previos de predicción de precios o análisis de sentimiento, el bot los realizará automáticamente, lo que puede llevar algo más de tiempo.
    - **Decisiones Basadas en Datos:** El bot toma decisiones basándose en los últimos análisis disponibles, asegurando una estrategia de inversión informada y actualizada.

    ### Advertencia
    :warning: La efectividad del bot está influenciada significativamente por la elección de días en la predicción de precio. Una selección de días muy larga puede disminuir la precisión de las predicciones y, por tanto, la efectividad del bot. Se recomienda precaución y considerar los resultados de la predicción de precios como uno de varios factores en la toma de decisiones.
    """, unsafe_allow_html=True)

    bot_operaciones()

elif opcion == "Proyección a Futuro":
    doc = "https://github.com/uaidan/TeslaAcciones/blob/main/Future.pdf"
    st.empty()
    st.title("Proyección a Futuro")

    st.markdown("""
        ## Visión Futura y Estrategia de Monetización

        En esta sección, exploramos nuestra visión a largo plazo para el proyecto y detallamos nuestra estrategia de monetización. Nuestro objetivo es crear un servicio que no solo sea innovador y valioso para nuestros usuarios, sino que también sea sostenible desde el punto de vista financiero.

        Para obtener más detalles sobre nuestra visión y estrategia de monetización, por favor, consulta el siguiente documento:

        """, unsafe_allow_html=True)

    #[Ver Documento de Estrategia](https://liveuem-my.sharepoint.com/:p:/g/personal/22156837_live_uem_es/ESMP6TzWCKJLibnddTRfW6gBwuZaPVaOra2nN14FrQzXHw?rtime=mOus2i0Q3Eg)

    espaciador_izquierda, col_central, espaciador_derecha = st.columns([1, 2, 1])
    with col_central:
        st.markdown(f"[Abrir {archivo_pdf}](./{archivo_pdf})")
                # Ruta al archivo que deseas abrir
                
