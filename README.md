```python
markdown_content = """# IA con Aprendizaje por Refuerzo: Presa vs Depredador en Unreal Engine 5 🎮🤖

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Unreal Engine 5](https://img.shields.io/badge/Unreal%20Engine-5.3%2B-black?style=for-the-badge&logo=unrealengine&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-orange?style=for-the-badge)

Este proyecto demuestra cómo el **Aprendizaje por Refuerzo (Reinforcement Learning)** puede dar vida a Inteligencias Artificiales complejas y dinámicas dentro de videojuegos. A través de un enfoque híbrido, se entrena un modelo de toma de decisiones en **Python** para generar tablas de conocimiento (**Q-Tables**), las cuales son posteriormente integradas en **Unreal Engine 5** para guiar el comportamiento de los agentes en un entorno tridimensional interactivo.

---

## 🏛️ Información Institucional

| Campo | Detalle |
| :--- | :--- |
| **Universidad** | Universidad Mayor, Real y Pontificia de San Francisco Xavier de Chuquisaca (**USFX**) |
| **Facultad** | Facultad de Tecnología |
| **Carrera** | Ingeniería de Sistemas / Ciencias de la Computación |
| **Materia** | Inteligencia Artificial II (SIS420) |
| **Docente** | Ing. Walter Pacheco Lora |
| **Estudiante** | Alvaro David Arancibia Estrada |
| **Semestre** | 01/2026 |

---

## 📝 Introducción

El núcleo de este proyecto consiste en modelar un escenario clásico de la teoría de juegos y la ecología matemática: el ecosistema de **Presa y Depredador**. En lugar de utilizar árboles de comportamiento tradicionales (Behavior Trees) o máquinas de estado finitas (FSM) cableadas a mano, las entidades aprenden de forma autónoma a optimizar sus acciones mediante interacciones repetidas con su entorno.

Para lograr esto, el problema se formaliza bajo el marco de los **Procesos de Decisión de Markov (MDP)**, aplicando los siguientes conceptos fundamentales de RL:
* **Agentes:** Las entidades autónomas (Presa y Depredador).
* **Entorno (Environment):** Un espacio matricial simulado donde ocurren las interacciones, movimientos y colisiones.
* **Estados ($S$):** Las configuraciones o posiciones relativas de los agentes en la matriz.
* **Acciones ($A$):** Movimientos posibles (Norte, Sur, Este, Oeste, Quieto).
* **Recompensas ($R$):** Estímulos numéricos positivos o negativos que guían el aprendizaje (ej. el depredador recibe un gran incentivo al capturar a la presa; la presa es penalizada si se acerca al peligro).
* **Funciones de Valor ($Q$):** Estimaciones de la utilidad a largo plazo de realizar una acción específica en un estado determinado.

---

## 🐍 Estructura de Entrenamiento en Python

El proceso de entrenamiento se realiza de forma aislada en un script de Python optimizado. Esto permite ejecutar miles de episodios en milisegundos sin la sobrecarga gráfica de un motor de videojuegos.

### Componentes Clave:
1.  **Clase `Presa` / `Depredador` (Agentes):** Definen la lógica interna de exploración ($\epsilon$-greedy), actualización de tasas de aprendizaje ($\alpha$) y factores de descuento ($\gamma$).
2.  **Clase `Entorno` (Matrix-Based):** Una matriz bidimensional donde se calculan las distancias de Manhattan, se gestionan los límites del mapa y se validan los estados de captura o escape.
3.  **Archivo de Entrenamiento (`train.py`):** El bucle principal que corre las simulaciones, ejecuta el algoritmo de *Q-Learning* clásico y exporta las matrices de conocimiento en formatos legibles (JSON/CSV) llamadas **Q-Tables**.

### 📸 Proceso de Simulación y Gráficas de Aprendizaje
*A continuación se presentan las capturas correspondientes al proceso de entrenamiento, convergencia de recompensas y pérdida a lo largo de los episodios.*


```

```text
File generated successfully.


```

+-----------------------------------------------------------------+
|                                                                 |
|                  [ESPACIO PARA COLOCAR CAPTURAS]                |
|       (Ej: Gráfica de Convergencia de Recompensa vs Episodios)   |
|                                                                 |
+-----------------------------------------------------------------+

```
*(Tip: Reemplazar este bloque con `![Progreso de Entrenamiento](./capturas/training_chart.png)`)*

---

## 🎮 Estructura de Uso de Q-Tables en Unreal Engine 5

Una vez obtenidas las **Q-Tables** óptimas desde Python, el archivo de datos se importa dentro de **Unreal Engine 5**. Aquí, el motor gráfico se encarga de dar vida física y visual a los agentes entrenados.

### Implementación en el Motor:
* **Lectura de Datos:** Los datos de la Q-Table se parsean mediante estructuras personalizadas en C++ o Blueprints a través de un Data Table o archivos JSON en tiempo de ejecución.
* **Toma de Decisiones en Tiempo Real:** En cada frame o intervalo de tiempo fijo (Tick), la IA del Depredador y de la Presa evalúa su estado actual (coordenadas relativas en el entorno 3D transformadas a la lógica matricial) y consulta la fila correspondiente en la Q-Table para ejecutar la acción con el valor de $Q$ más alto.
* **Componentes Visuales:** Uso del *Character Movement Component* para desplazamientos fluidos, animaciones reactivas según el estado emocional del agente (alerta, persecución, huida) y un entorno visualizado en 3D.

### 📸 Demostración de la IA en Unreal Engine 5
*Visualización del comportamiento de los agentes interactuando dentro del mapa tridimensional utilizando el conocimiento adquirido.*


```

+-----------------------------------------------------------------+
|                                                                 |
|                  [ESPACIO PARA COLOCAR CAPTURAS]                |
|       (Ej: Captura de pantalla del viewport de UE5 mostrando)   |
|             al Depredador persiguiendo dinámicamente)            |
|                                                                 |
+-----------------------------------------------------------------+

```
*(Tip: Reemplazar este bloque con `![Gameplay Render](./capturas/ue5_gameplay.png)`)*

---

## 📂 Estructura del Repositorio

```text
├── python_training/          # Código fuente del entrenamiento
│   ├── train.py              # Script principal de Q-Learning
│   ├── environment.py        # Definición del entorno matricial
│   ├── agents.py             # Clases Presa y Depredador
│   └── outputs/              # Q-Tables generadas (.json / .csv)
│
├── ue5_project/              # Proyecto de Unreal Engine 5
│   ├── Content/
│   │   ├── IA_Reinforcement/ # Blueprints, Q-Tables importadas y Materiales
│   │   └── Maps/             # Escenario de pruebas interactivo
│   └── Source/               # Código C++ para parseo óptimo (opcional)
│
├── capturas/                 # Imágenes de soporte de la documentación
└── README.md                 # El archivo que estás leyendo

```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Fase de Entrenamiento (Python)

Clona el repositorio, navega a la carpeta de entrenamiento e instala las dependencias mínimas (si aplica, como `numpy` o `matplotlib`), luego ejecuta:

```bash
cd python_training
python train.py

```

Esto generará los archivos correspondientes en la carpeta `outputs/`.

### 2. Fase de Visualización (Unreal Engine 5)

1. Copia el archivo `.json` generado en la carpeta de recursos de Unreal Engine.
2. Abre el proyecto `ue5_project/` en Unreal Engine 5.3 o superior.
3. Carga el mapa en `Content/Maps/MainSimulation.umap`.
4. ¡Dale al botón **Play** y observa cómo interactúan los agentes!

---

*© 2026 Alvaro David Arancibia Estrada - Estudiante de Ingeniería de Sistemas en la USFX.*
"""

with open("README.md", "w", encoding="utf-8") as file:
file.write(markdown_content)

print("File generated successfully.")

```
Tu archivo Markdown (`README.md`) para el repositorio de GitHub ha sido generado de manera exitosa y estructurado estéticamente para resaltar todos los requerimientos académicos e informativos de tu materia.

[file-tag: code-generated-file-0-1781009616050207845]

Aquí tienes una vista previa detallada de cómo se estructuró y lucirá en el repositorio:

***

# IA con Aprendizaje por Refuerzo: Presa vs Depredador en Unreal Engine 5 🎮🤖

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Unreal Engine 5](https://img.shields.io/badge/Unreal%20Engine-5.3%2B-black?style=for-the-badge&logo=unrealengine&logoColor=white)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-orange?style=for-the-badge)

Este proyecto demuestra cómo el **Aprendizaje por Refuerzo (Reinforcement Learning)** puede dar vida a Inteligencias Artificiales complejas y dinámicas dentro de videojuegos. A través de un enfoque híbrido, se entrena un modelo de toma de decisiones en **Python** para generar tablas de conocimiento (**Q-Tables**), las cuales son posteriormente integradas en **Unreal Engine 5** para guiar el comportamiento de los agentes en un entorno tridimensional interactivo.

---

## 🏛️ Información Institucional

| Campo | Detalle |
| :--- | :--- |
| **Universidad** | Universidad Mayor, Real y Pontificia de San Francisco Xavier de Chuquisaca (**USFX**) |
| **Facultad** | Facultad de Tecnología |
| **Carrera** | Ingeniería de Sistemas / Ciencias de la Computación |
| **Materia** | Inteligencia Artificial II (SIS420) |
| **Docente** | Ing. Walter Pacheco Lora |
| **Estudiante** | Alvaro David Arancibia Estrada |
| **Semestre** | 01/2026 |

---

## 📝 Introducción

El núcleo de este proyecto consiste en modelar un escenario clásico de la teoría de juegos y la ecología matemática: el ecosistema de **Presa y Depredador**. En lugar de utilizar árboles de comportamiento tradicionales (Behavior Trees) o máquinas de estado finitas (FSM) programadas rígidamente a mano, las entidades aprenden de forma autónoma a optimizar sus acciones mediante interacciones repetidas con su entorno.

Para lograr esto, el problema se formaliza bajo el marco de los **Procesos de Decisión de Markov (MDP)**, aplicando los siguientes conceptos fundamentales de Aprendizaje por Refuerzo:
* **Agentes:** Las entidades autónomas (Presa y Depredador).
* **Entorno (Environment):** Un espacio matricial simulado donde ocurren las interacciones, movimientos y colisiones.
* **Estados ($S$):** Las configuraciones o posiciones relativas de los agentes dentro de la matriz.
* **Acciones ($A$):** Movimientos posibles (Norte, Sur, Este, Oeste, Quieto).
* **Recompensas ($R$):** Estímulos numéricos positivos o negativos que guían el aprendizaje (ej. el depredador recibe un gran incentivo al capturar a la presa; la presa es penalizada si se acerca al peligro).
* **Funciones de Valor ($Q$):** Estimaciones de la utilidad a largo plazo de realizar una acción específica en un estado determinado.

---

## 🐍 Estructura de Entrenamiento en Python

El proceso de entrenamiento se realiza de forma aislada en un script de Python optimizado. Esto permite ejecutar miles de episodios en milisegundos sin la sobrecarga gráfica de un motor de videojuegos.

### Componentes Clave:
1. **Clase `Presa` / `Depredador` (Agentes):** Definen la lógica interna de exploración ($\epsilon$-greedy), actualización de tasas de aprendizaje ($\alpha$) y factores de descuento ($\gamma$).
2. **Clase `Entorno` (Matrix-Based):** Una matriz bidimensional donde se calculan las distancias de Manhattan, se gestionan los límites del mapa y se validan los estados de captura o escape.
3. **Archivo de Entrenamiento (`train.py`):** El bucle principal que corre las simulaciones, ejecuta el algoritmo de *Q-Learning* clásico y exporta las matrices de conocimiento en formatos legibles (JSON/CSV) llamadas **Q-Tables**.

### 📸 Proceso de Simulación y Gráficas de Aprendizaje
*A continuación se presentan las capturas correspondientes al proceso de entrenamiento, convergencia de recompensas y pérdidas a lo largo de los episodios.*

```text
+-----------------------------------------------------------------+
|                                                                 |
|                  [ESPACIO PARA COLOCAR CAPTURAS]                |
|       (Ej: Gráfica de Convergencia de Recompensa vs Episodios)   |
|                                                                 |
+-----------------------------------------------------------------+

```

*(Tip sugerido para GitHub: Reemplazar este bloque con `![Progreso de Entrenamiento](./capturas/training_chart.png)`)*

---

## 🎮 Estructura de Uso de Q-Tables en Unreal Engine 5

Una vez obtenidas las **Q-Tables** óptimas desde Python, el archivo de datos se importa dentro de **Unreal Engine 5**. Aquí, el motor gráfico se encarga de dar vida física y visual a los agentes entrenados.

### Implementación en el Motor:

* **Lectura de Datos:** Los datos de la Q-Table se parsean mediante estructuras personalizadas en C++ o Blueprints a través de un Data Table o archivos JSON en tiempo de ejecución.
* **Toma de Decisiones en Tiempo Real:** En cada frame o intervalo de tiempo fijo (Tick), la IA del Depredador y de la Presa evalúa su estado actual (coordenadas relativas en el entorno 3D transformadas a la lógica matricial) y consulta la fila correspondiente en la Q-Table para ejecutar la acción con el valor de $Q$ más alto.
* **Componentes Visuales:** Uso del *Character Movement Component* para desplazamientos fluidos, animaciones reactivas según el comportamiento del agente (alerta, persecución, huida) y un entorno visualizado completamente en 3D.

### 📸 Demostración de la IA en Unreal Engine 5

*Visualización del comportamiento de los agentes interactuando dentro del mapa tridimensional utilizando el conocimiento adquirido de las tablas.*

```text
+-----------------------------------------------------------------+
|                                                                 |
|                  [ESPACIO PARA COLOCAR CAPTURAS]                |
|       (Ej: Captura de pantalla del viewport de UE5 mostrando)   |
|             al Depredador persiguiendo dinámicamente)           |
|                                                                 |
+-----------------------------------------------------------------+

```

*(Tip sugerido para GitHub: Reemplazar este bloque con `![Gameplay Render](./capturas/ue5_gameplay.png)`)*

---

## 📂 Estructura del Repositorio

```text
├── python_training/          # Código fuente del entrenamiento
│   ├── train.py              # Script principal de Q-Learning
│   ├── environment.py        # Definición del entorno matricial
│   ├── agents.py             # Clases Presa y Depredador
│   └── outputs/              # Q-Tables generadas (.json / .csv)
│
├── ue5_project/              # Proyecto de Unreal Engine 5
│   ├── Content/
│   │   ├── IA_Reinforcement/ # Blueprints, Q-Tables importadas y Materiales
│   │   └── Maps/             # Escenario de pruebas interactivo
│   └── Source/               # Código C++ para parseo óptimo (opcional)
│
├── capturas/                 # Imágenes de soporte de la documentación
└── README.md                 # El archivo que estás leyendo

```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Fase de Entrenamiento (Python)

Clona el repositorio, navega a la carpeta de entrenamiento e instala las dependencias mínimas (ej. `numpy` o `matplotlib`), luego ejecuta:

```bash
cd python_training
python train.py

```

Esto generará los archivos correspondientes en la carpeta `outputs/`.

### 2. Fase de Visualización (Unreal Engine 5)

1. Copia el archivo `.json` generado en la carpeta de recursos de Unreal Engine.
2. Abre el archivo de proyecto `ue5_project/` en Unreal Engine 5.3 o superior.
3. Carga el mapa principal localizado en `Content/Maps/MainSimulation.umap`.
4. ¡Haz clic en el botón **Play** y observa cómo interactúan tus agentes entrenados!

---

*© 2026 Alvaro David Arancibia Estrada - Estudiante de Ingeniería de Sistemas en la USFX.*

---

### 🛠️ Recomendaciones para su uso en GitHub:

1. Crea una carpeta llamada `capturas/` en la raíz de tu proyecto.
2. Guarda tus capturas de pantalla de Python (gráficos o terminal) con el nombre `training_chart.png` y las de Unreal con `ue5_gameplay.png`.
3. Al colocarlas en esa ruta, las imágenes se cargarán y renderizarán automáticamente reemplazando los bloques de texto indicados.
