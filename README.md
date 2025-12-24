# 💧 Evaluación Económica: Instalación de Tanque de Agua con Bomba Eléctrica

Sistema web interactivo para evaluar la viabilidad económica de instalar un tanque de agua con bomba eléctrica en una vivienda.

## 🎯 Objetivo General

Determinar si la inversión en un tanque de agua con bomba eléctrica resulta económicamente conveniente en comparación con mantener el sistema actual (baja presión o cortes de agua frecuentes).

## 📚 Conceptos de Ingeniería Económica Aplicados

1. **Tasas de Interés**: Nominal y Efectiva (TNA, TEA)
2. **Valor Actual Neto (VAN)**: Evaluación de rentabilidad del proyecto
3. **Valor Anual Equivalente (VAE)**: Anualidad equivalente del VAN
4. **Tasa Interna de Retorno (TIR)**: Rentabilidad del proyecto
5. **Análisis Beneficio/Costo (B/C)**: Relación entre beneficios y costos
6. **Período de Recuperación (Payback)**: Simple y descontado
7. **TMAR**: Tasa Mínima Aceptable de Retorno
8. **Análisis de Sensibilidad**: Escenarios optimista, probable y pesimista
9. **Análisis Multicriterio**: Comparación de alternativas con múltiples atributos

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
ExamenFinal/
├── app.py              # Aplicación principal de Streamlit
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Documentación del proyecto
```

## 🛠️ Funcionalidades Principales

### 1. 📝 Inicio

- Presentación del proyecto
- Descripción de conceptos aplicados
- Datos base del proyecto

### 2. 💰 Datos de Inversión

- Configuración de costos iniciales:
  - Tanque de agua
  - Bomba eléctrica
  - Instalación
- Parámetros del proyecto:
  - Vida útil
  - Ahorro anual estimado
  - Mantenimiento anual
  - TMAR (Tasa Mínima Aceptable de Retorno)
- Opción de financiamiento:
  - Cálculo de tasa efectiva
  - Simulación de cuotas

### 3. 📊 Análisis Financiero

- Cálculo automático de:
  - VAN (Valor Actual Neto)
  - VAE (Valor Anual Equivalente)
  - TIR (Tasa Interna de Retorno)
  - Relación B/C
  - Payback simple y descontado
- Flujo de caja proyectado
- Gráficos interactivos
- Interpretación de resultados

### 4. 🔍 Análisis de Sensibilidad

- Tres escenarios:
  - Optimista: Aumento en ahorros
  - Probable: Escenario base
  - Pesimista: Reducción en ahorros
- Diagrama de tornado
- Sensibilidad del VAN vs TMAR
- Comparación visual de escenarios

### 5. ⚖️ Análisis Multicriterio

- Comparación de alternativas:
  - Opción A: Sistema económico
  - Opción B: Sistema premium
- Evaluación por criterios:
  - Costo inicial
  - Capacidad/Presión
  - Consumo eléctrico
  - Durabilidad
  - Mantenimiento
- Asignación de pesos ponderados
- Gráfico de radar comparativo

### 6. 📈 Resultados Integrales

- Dashboard de indicadores
- Matriz de decisión
- Conclusión y recomendación final
- Resumen ejecutivo
- Visualizaciones completas

## 💡 Datos de Ejemplo

| Concepto                    | Valor (S/.) |
| --------------------------- | ----------- |
| Tanque de agua (1,100 L)    | 750         |
| Bomba eléctrica ½ HP        | 600         |
| Tuberías e instalación      | 400         |
| **Total inversión inicial** | **1,750**   |
| Ahorro anual estimado       | 600 - 800   |
| Mantenimiento anual         | 100         |
| Vida útil                   | 8 años      |
| TMAR sugerida               | 10%         |

## 📊 Tecnologías Utilizadas

- **Streamlit**: Framework web para aplicaciones de datos
- **Pandas**: Análisis y manipulación de datos
- **NumPy**: Cálculos numéricos
- **Plotly**: Gráficos interactivos
- **NumPy Financial**: Funciones financieras

## 🎓 Aplicación Académica

Este proyecto está diseñado para:

- Estudiantes de Ingeniería Económica
- Evaluación de proyectos de inversión
- Análisis de viabilidad financiera
- Toma de decisiones económicas

## 📝 Cómo Usar

1. **Inicio**: Familiarízate con el proyecto y los conceptos
2. **Datos de Inversión**: Ingresa tus parámetros específicos
3. **Análisis Financiero**: Revisa los indicadores calculados
4. **Sensibilidad**: Explora diferentes escenarios
5. **Multicriterio**: Compara opciones alternativas
6. **Resultados**: Obtén la conclusión y recomendación

## 🤝 Contribuciones

Este es un proyecto académico. Sugerencias y mejoras son bienvenidas.

## 📄 Licencia

Proyecto académico - Ingeniería Económica

---

**Desarrollado con ❤️ usando Streamlit**
