# Proyecto_MLops
Este proyecto tiene como objetivo implementar técnicas de machine learning, implementando un sistema de recomendación de películas, para esto se pasaron por 4 etapas:
1. Entender los requerimientos del proyecto (familiarizarse con los datos)
2. Desarrollar ETL para poder cargar a la API
3. Desarrollar API para la consulta de datos
4. Implementar modelo de machine learning para ser montado en la API
## Revisión de requerimientos
Se analizan los requerimientos del proyecto, las herramientas a utilizar y el posible resultado final. <br>
Las librerías a utilizar son:
1. Pandas
2. Jason
3. AST
4. Fastapi
5. Unidecode
6. Matplotlib
## Proceso de extracción, transformación y carga (ETL)
### Extracción:
Para el proceso de extracción se utilizaron los archivos llamados credits.csv y movies_dataset.csv
En primer lugar mediante Python se realizó la carga del archivo movies_dataset.csv y credits.csv en formato DataFrame 
**REVISAR EL ARCHIVO "ETL.csv" EN EL SE ENCUENTRA TODO EL PROCESO DE EXTRACCIÓN EXPLICADO
### Transformación
Una vez cargada la información en Dataframes se procede a limpiar en primer lugar el archivo movies_dataset.csv haciendo las siguientes transformaciones:
- Filtro de valores nulos
- Eliminación de columnas sin importancia
- Cambio a formato fecha a las columnas requeridas
- Desanidar y seleccionar la información relevante pesente en los diccionarios de algunas columnas
- Calculo de columnas como Return y Anio
- Exportar el nuevo datframe limpio
En segundo lugar se procede a limpiar el archivo credits.csv con las siguientes transformaciones:
- Revisión de valores nulos
- Desanidar y seleccionar información relevantes de la columna cast y crew, en este caso solo se necesitan el nombre de los acotres y directores
- Eliminar columnas anidadas
- Exportar el nuevo datframe
Finalmente por medio del Id de cada película se unos los dos Datframes limpios
###Carga
La carga de los datos se realizó mediante la exportación del datframe final_limpio.csv y su sincronización con la carpeta Proyecto_MLops en github
**Este proceso se explica de manera más profunda en la creación de la API**




