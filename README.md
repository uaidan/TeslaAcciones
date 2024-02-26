# 📈 Predicción de Precio de Acciones y Análisis de Sentimiento de Noticias Tesla 🚀

¡Bienvenido al proyecto de predicción de precio de acciones y análisis de sentimiento de noticias de Tesla! Este proyecto utiliza técnicas de aprendizaje automático para predecir el precio futuro de las acciones de Tesla y realiza un análisis de sentimiento de las noticias actuales relacionadas con la empresa. Además, incluye un bot que puede realizar compras automáticas de acciones según las predicciones.

## ✨ Características

- **Predicción de Precio de Acciones:** Utiliza modelos de aprendizaje automático para predecir el precio futuro de las acciones de Tesla.
- **Análisis de Sentimiento:** Analiza el sentimiento de las noticias actuales sobre Tesla para evaluar su impacto en el precio de las acciones.
- **Bot de Compras Automáticas:** Realiza compras automáticas de acciones según las predicciones del modelo.
- **Visión a Futuro:** Presenta una visión estratégica del proyecto, detallando la dirección y los objetivos a largo plazo que se pretenden alcanzar.

## 🛠️ Tecnologías Utilizadas

- **Python:** Lenguaje de programación utilizado para la lógica del proyecto.
- **Streamlit:** Framework para crear aplicaciones web interactivas con Python.
- **Matplotlib:** Biblioteca de visualización de datos en Python para crear gráficos.
- **Selenium:** Herramienta de automatización de pruebas que se utiliza aquí para interactuar con sitios web.
- **Pandas:** Biblioteca de Python para manipulación y análisis de datos.
- **NumPy:** Biblioteca de Python para cálculos numéricos.
- **Requests:** Biblioteca de Python para enviar solicitudes HTTP.
- **XGBoost:** Biblioteca de aprendizaje automático de Python para implementar algoritmos de gradient boosting.
- **scikit-learn:** Biblioteca de aprendizaje automático de Python para implementar algoritmos de minería y análisis de datos.

## 🚀 Cómo Empezar

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener instalado Python y todas las dependencias listadas en `requirements.txt`.
3. Ejecuta la aplicación con `streamlit run appTesla.py`.
4. Sigue las instrucciones en pantalla para realizar la predicción de precio de acciones, análisis de sentimiento y/o activar el bot de compras automáticas.

## 🛠️ Configuración Adicional

Para el correcto funcionamiento del proyecto, asegúrate de descomentar las siguientes líneas en el archivo `appTesla.py`:

```python
# Descomenta estas líneas para el correcto funcionamiento

# Línea 90
# estado = main_bot(cantidad, accion)  # mandar al bot las ordenes (Llamada al bot)

# Línea 100
# menuNoticias()  # scraper de noticias

# Línea 110
# estado = main_bot(cantidad, accion)  # mandar al bot las ordenes (Llamada al bot)

# Línea 127
# menuNoticias()  # scraper de noticias
```

## 🤝 Contribuir

¡Agradecemos cualquier contribución para mejorar este proyecto! Si tienes alguna idea o sugerencia, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Haz tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`).
4. Sube tus cambios a tu repositorio (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## 📋 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.

## 💬 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto con nosotros.

---

¡Gracias por contribuir al proyecto de predicción de precio de acciones y análisis de sentimiento de noticias de Tesla! Esperamos que disfrutes explorando las funcionalidades y contribuyendo al desarrollo de este proyecto.
