# PLN de Neuromante | Ismael

Proyecto académico con la muestra oficial en español de **Neuromante**, de William Gibson, traducida por David Tejera Expósito. No analiza la novela completa.

## Fuente y reproducción local

- Ficha editorial: https://www.planetadelibros.com.mx/libro-neuromante/432536
- Muestra de la editorial: https://proassetspdlcom.cdnstatics2.com/usuaris/libros_contenido/arxius/53/52201_Neuromante.pdf
- Consulta: 23 de octubre de 2026.

El paquete incluye código y resultados numéricos, sin redistribuir el PDF ni una copia extensa de su texto. El script `preparar_texto.py` obtiene la muestra desde la editorial y genera el archivo TXT local necesario para el ejercicio. Puede recibir una copia local mediante `--pdf ruta.pdf`. La disponibilidad de la fuente puede cambiar.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python preparar_texto.py
python procesar.py
```

En Windows, activar el entorno con `.venv\Scripts\activate`.

## Etapas

1. Extraer el texto del PDF con pypdf, omitiendo cubierta, portada, créditos y pies de imprenta. Unir palabras separadas por guiones de final de línea y estandarizar espacios.
2. Normalizar Unicode NFC; tokenizar, segmentar oraciones y lematizar con spaCy español. Filtrar puntuación y palabras vacías, conservando negaciones. Separar lemas compuestos para compartir el vocabulario de sklearn y Gensim.
3. Representar oraciones con Bag-of-Words y TF-IDF. Exportar las matrices dispersas y el vocabulario.
4. Entrenar Word2Vec Skip-gram: 30 dimensiones, ventana 4, mínimo de una aparición, 150 épocas, semilla 42 y un trabajador.
5. Proyectar a dos dimensiones con PCA y generar dos PNG. La selección de 25 términos más frecuentes se realiza por conteo, sin elegir manualmente los resultados.

## Resultados de la ejecución

- 366 oraciones.
- 6,494 tokens originales.
- 2,644 tokens tras filtrado y lematización.
- 1,466 términos distintos.
- Matrices BoW y TF-IDF de 366 × 1,466.

Los resultados están en `resultados/`. El script también genera localmente texto procesado y una tabla de tokens para revisión; esos archivos no se incluyen en la distribución.

## Interpretación y límites

BoW conserva conteos y TF-IDF pondera términos distintivos entre oraciones, pero ambas representaciones de unigramas pierden orden. Word2Vec aprende asociaciones de contexto; sus vecinos no son necesariamente sinónimos. En una muestra de una sola obra no hay base para afirmar calidad semántica general. Los nombres y la jerga de ficción pueden inducir errores del modelo lingüístico.

Las gráficas muestran una proyección PCA, no el espacio completo: cercanía en 2D no prueba equivalencia de significado. La extracción del PDF puede introducir errores y la muestra finaliza antes que la novela; deben revisarse esos límites al interpretar resultados. No se evaluó comprensión lectora ni se midió rendimiento predictivo del modelo.

## Distribución

El código puede revisarse y adaptarse para la tarea. Los derechos de la obra y la traducción corresponden a sus titulares. `data/LEEME.txt` explica cómo generar el TXT local. No se ha creado ni publicado un repositorio de GitHub para esta versión.
