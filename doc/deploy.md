# Despliegue del Chatbot Assistant

Durante el desarrollo del **Chatbot Assistant** mi objetivo fue llevarla a producción usando infraestructura de Azure. Inicialmente, elegí usar **Azure Container Registry (ACR)** para almacenar mis imágenes Docker, pero este enfoque pronto se volvió inviable por limitaciones técnicas que encontré en el camino.

**Link al despliegue:**

https://cuervo-chatbot-aeddajh5g2ghfth0.brazilsouth-01.azurewebsites.net/static/index.html

---

## Problemas

El principal obstáculo fue el **tiempo excesivo y la imposibilidad de subir la imagen Docker a ACR** desde mi máquina local. El registro no aceptaba correctamente la imagen o la subida tardaba mucho tiempo en completarse.
Este cuello de botella se volvió frustrante y contraproducente, ya que requería hacer múltiples pruebas con imágenes actualizadas, y el tiempo de espera rompía por completo mi flujo de trabajo. Además, al no tener experiencia profunda con ACR, sus configuraciones y dependencias no pude resolverlo con rapidez.
En lugar de frenar el desarrollo, decidí buscar una alternativa más práctica para continuar avanzando.

---

## Migración a Docker Hub

La solución fue usar **Docker Hub** como registro público de imágenes. Esta decisión fue clave para avanzar rápidamente y obtener una experiencia fluida de despliegue, ya que:

- Docker Hub es compatible de forma nativa con **Azure Web App for Containers**.
- No requiere autenticación adicional si la imagen es **pública**.
- Permite subir imágenes desde cualquier entorno local sin configuración compleja.

---

## Conexión: Azure Web App - Docker Hub - GitHub

### 1. **Docker Hub**

Para guardar la imagen Docker de mi aplicación. Azure App Service accede a este repositorio cada vez que necesita levantar una nueva instancia.

### 2. **Azure Web App for Containers**

Es la plataforma de Azure donde corre mi aplicación. Está configurada para hacer _pull_ de la imagen desde Docker Hub. Cada vez que reinicio la App Web, Azure vuelve a cargar la última versión disponible de la imagen pública.

### 3. **GitHub**

Automatización con GitHub Actions, haciendo que cada `push` a la rama `main` reconstruya la imagen y la suba automáticamente.

---

## Beneficios

- En solo minutos puedo tener mi aplicación actualizada en Azure después de hacer cambios.
- Evité lidiar con permisos, autenticaciones y tiempos de subida largos de ACR.
- Independencia de Azure, ya que puedo usar la misma imagen en cualquier otro proveedor cloud.

---

## Conclusiones

Reconozco que en un entorno productivo con requerimientos más estrictos de seguridad, autenticación o privacidad de las imágenes, ACR puede ser una mejor opción. En ese caso, con más experiencia en ACR y CI/CD, podría migrar a ACR para tener toda la solución contenida en Azure.
El despliegue de esta aplicación fue sin duda la parte más trabajosa y mas compleja, tuve que aprender mucho por mi cuenta, gane muchos conocimientos nuevos y se me abrio un mundo que, antes de este proyecto, no conocia.
El desarrollo de la aplicación de Chatbot no fue tan complicado, solo tuve que seguir la documentacion de Langchain, la cual esta bastante bien explicada. Tuve problemas con el manejo de las API key's de Google, pero facilmente pude resolverlos.
Si bien no pude entregar el trabajo en tiempo y forma estoy orgulloso de haber podido completarlo, y estoy emocionado con seguir aprendiendo sobre este mundo y seguir explorando sus posibilidades.
