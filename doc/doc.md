# Chatbot Assistant

## Objetivo

Desarrollar una aplicación de asistente de chatbot utilizando una arquitectura RAG. El asistente debe ser capaz de responder preguntas sobre la empresa Promtior. En particular, debe ser capaz de responder correctamente las siguientes preguntas:

- _What services does Promtior offer?_
- _When was the company founded?_

## Alcance

Es importante definir el alcance que tendrá mi aplicación de Asistente de Chatbot para tener una definición clara de los objetivos. Por lo tanto, voy a definir:

### Lo que se hará:

- Se tomarán como fuentes la página oficial de Promtior y la presentación en PDF recibida por parte del equipo.
- Se realizará un scraping de las principales vistas de la página web.
- Se realizará una extracción básica del texto de la presentación en PDF, sin tener en cuenta las secciones específicas de los elementos. Además, solo se tomará como fuente las páginas 3 y 4 del PDF, ya que el resto de páginas son instrucciones sobre cómo realizar la prueba técnica.
- Se realizará la creación de una base vectorial previa a la ejecución de la aplicación. Una vez persistida la base vectorial, se realiza la carga solo una vez al principio de la aplicación.
- Se realizará un asistente de chatbot que responde a las preguntas del usuario basándose en contexto relevante relacionado con la pregunta.
- Se realizará una interfaz conversacional simple, donde las preguntas son independientes unas de otras.

### Lo que no se hará:

- No se agregará memoria real. Esto no es necesario dado que tener una conversación sin memoria es útil en consultas de tipo FAQ para mantener respuestas independientes en cada turno.

---

## Enfoques de desarrollo y dificultades encontradas

Durante el desarrollo del chatbot "Cuervo", enfrenté múltiples desafíos técnicos que dividí en tres enfoques distintos. Cada uno de ellos trajo sus propios aprendizajes, dificultades y resultados.

---

### **Enfoque 1: Despliegue con 2 contenedores (Ollama y Llama2)**

En este enfoque quise mantener separación de responsabilidades: un contenedor corría Ollama con el modelo Llama2 como backend LLM, y otro contenedor ejecutaba FastAPI y se conectaba al servicio Ollama vía HTTP (`http://ollama:11434`). Para los embeddings usé `nomic-embed-text`.

**Problemas encontrados:**

- La comunicación entre los contenedores no fue sencilla. Aunque configuré correctamente el `docker-compose`, el contenedor de FastAPI no lograba conectarse a Ollama, incluso cuando el servicio estaba activo.
- Muchas veces la API devolvía `Failed to connect to Ollama`, pese a estar accesible vía `curl` desde dentro del contenedor.
- La instalación de dependencias para Ollama y el tamaño del modelo Llama2 hacían que el proceso fuese lento y demandante de recursos.

**Resultado:** no logré establecer una arquitectura funcional y confiable entre los contenedores.

---

### **Enfoque 2: Despliegue con 1 contenedor usando Gemini (LLM y embeddings)**

Para simplificar el entorno, opté por usar Google Generative AI (Gemini) tanto para el LLM como para los embeddings (`GoogleGenerativeAIEmbeddings`).

**Ventajas esperadas:**

- Se eliminaba la necesidad de un segundo contenedor.
- Se mejoraba la velocidad de respuesta y se centralizaba la configuración.

**Problemas encontrados:**

- El SDK de Gemini requiere una variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` apuntando a un archivo `.json` con las credenciales.
- En local funcionaba bien, pero al dockerizar la app y desplegarla (por ejemplo, en Azure), ese archivo no se encontraba.
- Intenté múltiples enfoques para incluir el JSON: montarlo como volumen, definirlo como string, pasarlo en `Dockerfile`, etc., sin éxito consistente.
- También aparecieron errores de autenticación como `DefaultCredentialsError`, incluso al haber autenticado con `gcloud`.

**Resultado:** aunque el desarrollo funcionaba localmente, no logré una forma robusta de desplegarlo con credenciales correctamente integradas al contenedor.

---

### **Enfoque 3: Despliegue con 1 contenedor usando Gemini (LLM) y HuggingFaceEmbeddings**

Como alternativa, decidí usar Gemini únicamente como LLM y reemplazar el embedding model por `HuggingFaceEmbeddings`, que no requiere credenciales ni conexión externa.

**Ventajas esperadas:**

- Simplificaba la autenticación con Google.
- Eliminaba la dependencia del archivo `credentials.json` para embeddings.

**Problemas encontrados:**

- HuggingFaceEmbeddings descarga dependencias pesadas.
- Permanecia el problema del SDK de Gemini (`GOOGLE_APPLICATION_CREDENTIALS`), no pude encontar la forma de que Docker detecte la variable de entorno.

**Resultado:** fue el enfoque más simple conceptualmente, pero aún con problemas relacionados a la inicialización de modelos y configuraciones en tiempo de ejecución dentro del contenedor.

---

## Conclusión

A lo largo de este proceso pasé por tres enfoques distintos, enfrentando errores de red, dependencias, autenticación y compatibilidad de bibliotecas.

**Di mi mayor esfuerzo en cada etapa del desarrollo.** Investigué soluciones, cambié de estrategia, rediseñé el flujo, adapté las herramientas y configuraciones para lograr una app funcional y correctamente desplegada.

El desarrollo local fue exitoso. Pude validar que la arquitectura RAG funciona correctamente con la vector store, los embeddings y el LLM elegido. Sin embargo, el despliegue completo en la nube fue el tramo más complejo y no logré finalizarlo de forma estable.

**Me llevo una experiencia profunda y real sobre cómo encarar un proyecto de arquitectura RAG completo con despliegue en cloud, integraciones de LLMs, y desafíos reales de ingeniería.** Si bien no logré terminar el producto final en un entorno productivo, el aprendizaje técnico fue altísimo.
