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
| **Carrera** | Ingeniería en Ciencias de la Computación |
| **Materia** | Inteligencia Artificial I (SIS420) |
| **Docente** | Ing. Carlos Walter Pacheco Lora |
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


Proceso de entrenamiento en Python










 <img width="490" height="580" alt="image" src="https://github.com/user-attachments/assets/dc8ef869-43fd-4af7-b385-4c2c3737063e" />



<img width="1103" height="68" alt="image" src="https://github.com/user-attachments/assets/b2417b90-95c9-427d-9045-f7d26e7d7c43" />
