**Descripción**

Este proyecto tiene la finalidad de procesar un dataset de peliculas y otro con directores y actores para disponibilizar queries sobre las peliculas y las personas que la hicieron, asi como crear un sistema de recomendación basado en distintas caracteristicas de las películas.

**Estructura del proyecto**
- **Data original:** Contiene los datasets originales sin ninguna modificacion
- **Data procesada:** Contiene la data despues de aplicarle las transformaciones para las consultas y el sistema de recomendación
- **Notebooks:** Los notebooks de transformación, EDA y pruebas de distintas funciones o modelos de ML, así como un main auxiliar que sirvió para probar distintos cambios de manera local
- **main.py:** Contiene el script necesario para la creación de la API con todos sus endpoints
- **requirements.txt:** Archivo de texto con las dependencias necesarias para levantar el servidor de render con la API

**Metodología**

Se usaron técnicas para la exploración de datos como llenado de valores faltantes y creación de nuevas columnas necesarias para las consultas, asi como nuevos archvios *csv* con datos reducidos por limitaciones en render o por eficiencia.
Para la API se utiliza la libreria fastapi con sus decoradores *app.get(/)*.
Modelo de recomendación funciona agregando todas las variables relevantes de una película en un mismo string para después aplicar TF-IDF y similitud del coseno para encontrar palabras relevantes y similitud entre distintas películas.

**Descarga e instalación**

Al clonar el repo, se deben de sustituir los paths que actualmente apuntan al repo de github para que funcione con render, así como instalar por medio de pip algunas librerias que hagan falta, como por ejemplo pandas, numpy, sklearn, uvicorn, matplotlib, seaborn, etc.

**Insights y observaciones**

Los mayores retos en la creación de dicha API es el manejo del tamaño de los datos, ya que debido a limitaciones de memoria en render se debieron de reducir significativamnte para permitir el funcionamiento, pero de manera local se pueden crear las matrices de simulitud de de aproximadamente 15.6 gb con una buena funcionalidad.
Otro reto es desanidar los datos de *datasets originales* ya que al venir listas de diccionarios, resulta un proceso complejo y toma bastante tiempo.

**Autor:** Fernando Sánchez Barrera
