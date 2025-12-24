import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objects as go
import plotly.express as px
from data_manager import DataManager

# Configuración de la página
st.set_page_config(
    page_title="Evaluación Económica - Tanque de Agua",
    page_icon="💧",
    layout="wide"
)

# Inicializar datos usando DataManager
DataManager.initialize()

# Funciones de cálculo
def calcular_tasa_efectiva(tasa_nominal, periodos):
    """Convierte tasa nominal a efectiva"""
    return (1 + tasa_nominal / periodos) ** periodos - 1

def calcular_van(inversion_inicial, flujos_netos, tasa_descuento):
    """Calcula el Valor Actual Neto"""
    van = -inversion_inicial
    for i, flujo in enumerate(flujos_netos):
        van += flujo / ((1 + tasa_descuento) ** (i + 1))
    return van

def calcular_vae(van, tasa, n):
    """Calcula el Valor Anual Equivalente"""
    if tasa == 0:
        return van / n
    return van * (tasa * (1 + tasa)**n) / ((1 + tasa)**n - 1)

def calcular_tir(inversion_inicial, flujos_netos):
    """Calcula la Tasa Interna de Retorno"""
    flujos = [-inversion_inicial] + flujos_netos
    return npf.irr(flujos) if len(flujos) > 1 else 0

def calcular_bc(beneficios, costos, tasa, n):
    """Calcula la relación Beneficio/Costo"""
    vp_beneficios = sum([beneficios / ((1 + tasa) ** (i + 1)) for i in range(n)])
    vp_costos = sum([costos / ((1 + tasa) ** (i + 1)) for i in range(n)])
    return vp_beneficios / vp_costos if vp_costos != 0 else 0

def calcular_payback(inversion_inicial, flujos_netos):
    """Calcula el período de recuperación simple"""
    acumulado = 0
    for i, flujo in enumerate(flujos_netos):
        acumulado += flujo
        if acumulado >= inversion_inicial:
            if flujo == 0:  # Prevenir división por cero
                return i + 1
            return i + 1 + (inversion_inicial - (acumulado - flujo)) / flujo
    return None

def calcular_payback_descontado(inversion_inicial, flujos_netos, tasa):
    """Calcula el período de recuperación descontado"""
    acumulado = 0
    for i, flujo in enumerate(flujos_netos):
        vp_flujo = flujo / ((1 + tasa) ** (i + 1))
        acumulado += vp_flujo
        if acumulado >= inversion_inicial:
            flujo_anterior = acumulado - vp_flujo
            if vp_flujo == 0:  # Prevenir división por cero
                return i + 1
            return i + 1 + (inversion_inicial - flujo_anterior) / vp_flujo
    return None

# Título principal
st.title("💧 Evaluación Económica: Instalación de Tanque de Agua con Bomba Eléctrica")
st.markdown("### Objetivo: Determinar la viabilidad económica de la inversión en comparación con el sistema actual")

# Sidebar
st.sidebar.header("🔧 Menú de Navegación")

# Asegurar que menu_opcion esté inicializado
if "menu_opcion" not in st.session_state:
    st.session_state["menu_opcion"] = "💰 Datos de Inversión"

opcion = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["📝 Inicio", "📖 Glosario", "📚 Manual de Uso", "💰 Datos de Inversión",
     "📊 Análisis Financiero", "🔍 Análisis de Sensibilidad",
     "⚖️ Análisis Multicriterio", "📈 Resultados Integrales"],
    key="menu_opcion"
)

# ==================== INICIO ====================
if opcion == "📝 Inicio":
    st.header("💧 Bienvenido al Sistema de Evaluación Económica")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📌 ¿Qué es este sistema?
        
        Este sistema es una **herramienta web interactiva** diseñada para evaluar la viabilidad 
        económica de proyectos de inversión, específicamente orientada a la instalación de 
        sistemas de agua domésticos (tanque de agua con bomba eléctrica).
        
        ### 👥 ¿A quién está dirigido?
        
        - **Estudiantes** de Ingeniería Económica, Administración y carreras afines
        - **Propietarios de viviendas** que enfrentan problemas de presión o cortes de agua
        - **Profesionales** que requieren evaluar proyectos de inversión pequeños
        - **Inversionistas** que buscan analizar la rentabilidad de mejoras en inmuebles
        - **Consultores** que necesitan herramientas rápidas de evaluación económica
        
        ### 🎯 ¿Para qué se usa?
        
        **Casos de uso principales:**
        
        ✅ **Análisis de inversión doméstica**: Determinar si invertir en un tanque de agua es conveniente
        
        ✅ **Proyectos académicos**: Aplicar conceptos de ingeniería económica en casos reales
        
        ✅ **Comparación de alternativas**: Evaluar diferentes opciones de sistemas de agua
        
        ✅ **Toma de decisiones**: Obtener respaldo cuantitativo para decisiones de inversión
        
        ✅ **Análisis de escenarios**: Evaluar riesgos y oportunidades en diferentes contextos
        
        ### 💡 ¿Cuándo usar esta herramienta?
        
        - Cuando enfrentes **cortes de agua frecuentes** en tu zona
        - Si tu vivienda tiene **baja presión de agua** constante
        - Antes de realizar una **inversión en mejoras del hogar**
        - Para **valorizar tu propiedad** con mejoras justificadas
        - Cuando necesites **justificar económicamente** una compra
        - Para **aprender** conceptos de ingeniería económica con ejemplos prácticos
        
        ### 🔍 ¿Qué te ofrece?
        
        - Cálculos automáticos de indicadores financieros (VAN, TIR, B/C, Payback)
        - Análisis de sensibilidad con múltiples escenarios
        - Comparación de alternativas mediante análisis multicriterio
        - Visualizaciones interactivas y gráficos profesionales
        - Interpretación clara de resultados
        - Recomendaciones fundamentadas
        
        ---
        
        💡 **Consejo**: Si es tu primera vez, te recomendamos revisar el **Glosario** para 
        familiarizarte con los conceptos, y luego el **Manual de Uso** para conocer el flujo 
        de trabajo sugerido.
        """)
    
    with col2:
        st.success("### 🎓 Características")
        st.write("✅ Interfaz intuitiva")
        st.write("✅ Cálculos automáticos")
        st.write("✅ Gráficos interactivos")
        st.write("✅ Análisis completo")
        st.write("✅ Resultados claros")
        
        st.divider()
        
        st.info("### 📋 Datos Base de Ejemplo")
        st.metric("Inversión Estimada", "S/ 1,750")
        st.metric("Ahorro Anual", "S/ 600 - 800")
        st.metric("Vida Útil", "8 años")
        st.metric("Mantenimiento Anual", "S/ 100")
        
        st.divider()
        
        st.warning("### ⚡ Inicio Rápido")
        st.write("1️⃣ Lee el **Glosario**")
        st.write("2️⃣ Revisa el **Manual**")
        st.write("3️⃣ Ingresa tus **Datos**")
        st.write("4️⃣ Analiza los **Resultados**")

# ==================== GLOSARIO ====================
elif opcion == "📖 Glosario":
    st.header("📖 Glosario de Conceptos de Ingeniería Económica")
    st.markdown("Conceptos fundamentales aplicados en este sistema de evaluación")
    
    # Organizar en tabs
    tab1, tab2, tab3 = st.tabs(["📊 Indicadores Principales", "💹 Tasas y Análisis", "🎯 Métodos de Evaluación"])
    
    with tab1:
        st.subheader("Indicadores Financieros Principales")
        
        st.markdown("---")
        st.markdown("### 💵 VAN - Valor Actual Neto (Valor Presente Neto)")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Definición:** Mide la rentabilidad de un proyecto en términos de dinero actual, 
            descontando todos los flujos futuros a valor presente.
            
            **Fórmula:**
            
            $$ VAN = -I_0 + \\sum_{t=1}^{n} \\frac{F_t}{(1+i)^t} $$
            
            Donde:
            - $I_0$ = Inversión inicial
            - $F_t$ = Flujo de caja en el período t
            - $i$ = Tasa de descuento (TMAR)
            - $n$ = Número de períodos
            
            **Criterio de decisión:**
            - VAN > 0 → Proyecto viable (genera valor)
            - VAN = 0 → Indiferente
            - VAN < 0 → Proyecto no viable (destruye valor)
            """)
        with col2:
            st.success("**Ventajas:**")
            st.write("✅ Considera valor del dinero en el tiempo")
            st.write("✅ Fácil interpretación")
            st.write("✅ Permite sumar proyectos")
        
        st.markdown("---")
        st.markdown("### 📈 TIR - Tasa Interna de Retorno")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Definición:** Es la tasa de descuento que hace que el VAN sea igual a cero. 
            Representa la rentabilidad porcentual del proyecto.
            
            **Fórmula:**
            
            $$ 0 = -I_0 + \\sum_{t=1}^{n} \\frac{F_t}{(1+TIR)^t} $$
            
            **Criterio de decisión:**
            - TIR > TMAR → Proyecto rentable
            - TIR = TMAR → Indiferente
            - TIR < TMAR → Proyecto no rentable
            
            **Interpretación:** Si TIR = 15%, significa que el proyecto genera un rendimiento 
            del 15% anual sobre la inversión.
            """)
        with col2:
            st.info("**Aplicación:**")
            st.write("📊 Mide rentabilidad")
            st.write("📊 Compara con TMAR")
            st.write("📊 Independiente de tasa externa")
        
        st.markdown("---")
        st.markdown("### 💰 VAE - Valor Anual Equivalente")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Definición:** Convierte el VAN en una anualidad uniforme equivalente durante 
            la vida del proyecto.
            
            **Fórmula:**
            
            $$ VAE = VAN \\times \\frac{i(1+i)^n}{(1+i)^n - 1} $$
            
            **Utilidad:** Permite comparar proyectos con diferentes vidas útiles al expresar 
            el valor en términos anuales constantes.
            """)
        with col2:
            st.success("**Uso:**")
            st.write("✅ Comparar proyectos")
            st.write("✅ Vidas útiles diferentes")
            st.write("✅ Presupuestos anuales")
    
    with tab2:
        st.subheader("Tasas de Interés y Análisis de Riesgo")
        
        st.markdown("---")
        st.markdown("### 🏦 Tasas de Interés: Nominal vs Efectiva")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Tasa Nominal Anual (TNA):**
            
            Es la tasa de interés anual sin considerar la capitalización de intereses.
            
            **Ejemplo:** TNA = 12% anual
            """)
        with col2:
            st.markdown("""
            **Tasa Efectiva Anual (TEA):**
            
            Considera el efecto de la capitalización de intereses en períodos menores al año.
            
            **Fórmula:**
            
            $$ TEA = \\left(1 + \\frac{TNA}{m}\\right)^m - 1 $$
            
            Donde m = número de capitalizaciones por año
            """)
        
        st.info("""
        **Ejemplo práctico:**
        - TNA = 12% anual con capitalización mensual
        - TEA = (1 + 0.12/12)^12 - 1 = 12.68%
        - La TEA es mayor porque considera el interés compuesto
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 TMAR - Tasa Mínima Aceptable de Retorno")
        st.markdown("""
        **Definición:** Es la tasa mínima de ganancia que un inversionista está dispuesto 
        a aceptar para realizar un proyecto.
        
        **Componentes:**
        
        $$ TMAR = i_f + f + i_f \\times f $$
        
        Donde:
        - $i_f$ = Inflación esperada
        - $f$ = Premio al riesgo
        
        **Factores que la determinan:**
        - Tasa de inflación
        - Riesgo del proyecto
        - Costo de oportunidad
        - Tasa de interés bancaria
        - Rendimiento mínimo esperado
        
        **Uso en este proyecto:** Se utiliza como tasa de descuento para calcular el VAN 
        y como referencia para comparar con la TIR.
        """)
        
        st.markdown("---")
        st.markdown("### 📉 Análisis de Sensibilidad")
        st.markdown("""
        **Definición:** Técnica que permite evaluar cómo cambian los resultados del proyecto 
        ante variaciones en los parámetros clave.
        
        **Tipos de escenarios:**
        
        1. **Optimista:** Aumentan los beneficios o disminuyen los costos
        2. **Probable:** Valores esperados o más probables
        3. **Pesimista:** Disminuyen beneficios o aumentan costos
        
        **Objetivo:** Identificar qué variables tienen mayor impacto en la rentabilidad 
        y evaluar el riesgo del proyecto.
        """)
    
    with tab3:
        st.subheader("Métodos de Evaluación y Comparación")
        
        st.markdown("---")
        st.markdown("### ⚖️ Análisis Beneficio/Costo (B/C)")
        st.markdown("""
        **Definición:** Relación entre el valor presente de los beneficios y el valor 
        presente de los costos.
        
        **Fórmula:**
        
        $$ B/C = \\frac{\\sum_{t=1}^{n} \\frac{B_t}{(1+i)^t}}{\\sum_{t=1}^{n} \\frac{C_t}{(1+i)^t}} $$
        
        **Criterio de decisión:**
        - B/C > 1 → Beneficios superan costos (Proyecto conveniente)
        - B/C = 1 → Beneficios igualan costos (Indiferente)
        - B/C < 1 → Costos superan beneficios (No conveniente)
        
        **Interpretación:** Si B/C = 1.5, por cada sol invertido se obtienen S/ 1.50 
        en beneficios.
        """)
        
        st.markdown("---")
        st.markdown("### ⏱️ Período de Recuperación (Payback)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Payback Simple:**
            
            Tiempo necesario para recuperar la inversión inicial sin considerar el 
            valor del dinero en el tiempo.
            
            **Cálculo:** Se acumulan los flujos hasta igualar la inversión inicial.
            """)
        with col2:
            st.markdown("""
            **Payback Descontado:**
            
            Tiempo necesario para recuperar la inversión considerando el valor del 
            dinero en el tiempo (flujos descontados).
            
            **Ventaja:** Más realista que el payback simple.
            """)
        
        st.warning("""
        **Limitaciones del Payback:**
        - No considera flujos después del período de recuperación
        - No mide rentabilidad, solo liquidez
        - Debe usarse como complemento, no como único criterio
        """)
        
        st.markdown("---")
        st.markdown("### 🏆 Análisis Multicriterio (Método de Pesos Ponderados)")
        st.markdown("""
        **Definición:** Técnica de decisión que permite comparar alternativas considerando 
        múltiples criterios (no solo económicos).
        
        **Proceso:**
        
        1. **Identificar criterios:** Costo, calidad, durabilidad, etc.
        2. **Asignar pesos:** Según importancia de cada criterio (suma = 1.0)
        3. **Calificar alternativas:** Puntuar cada opción en cada criterio
        4. **Calcular puntaje ponderado:**
        
        $$ P = \\sum_{i=1}^{n} w_i \\times c_i $$
        
        Donde:
        - $P$ = Puntaje total
        - $w_i$ = Peso del criterio i
        - $c_i$ = Calificación en el criterio i
        
        5. **Seleccionar:** La alternativa con mayor puntaje
        
        **Ventajas:**
        - Considera aspectos cualitativos y cuantitativos
        - Estructura la toma de decisiones
        - Permite involucrar múltiples stakeholders
        """)
    
    st.divider()
    st.info("""
    💡 **Nota importante:** Todos estos conceptos están implementados en las diferentes 
    secciones de esta aplicación. Puedes verlos en acción ingresando tus datos y 
    navegando por las opciones del menú.
    """)

# ==================== MANUAL DE USO ====================
elif opcion == "📚 Manual de Uso":
    st.header("📚 Manual de Uso del Sistema")
    st.markdown("Guía paso a paso para utilizar correctamente esta herramienta")
    
    st.divider()
    
    # Flujo de trabajo
    st.subheader("🔄 Flujo de Trabajo Recomendado")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 📖 PASO 1
        **Familiarización**
        
        1. Lee la sección **Inicio**
        2. Revisa el **Glosario**
        3. Comprende los conceptos
        """)
    
    with col2:
        st.success("""
        ### 💰 PASO 2
        **Ingreso de Datos**
        
        1. Ve a **Datos de Inversión**
        2. Configura los costos
        3. Define parámetros
        4. Guarda los datos
        """)
    
    with col3:
        st.warning("""
        ### 📊 PASO 3
        **Análisis de Resultados**
        
        1. Revisa **Análisis Financiero**
        2. Explora **Sensibilidad**
        3. Compara en **Multicriterio**
        4. Lee **Resultados Integrales**
        """)
    
    st.divider()
    
    # Instrucciones detalladas por sección
    st.subheader("📋 Instrucciones Detalladas por Sección")
    
    with st.expander("💰 Cómo usar: DATOS DE INVERSIÓN", expanded=True):
        st.markdown("""
        Esta es la sección más importante porque aquí defines todos los parámetros de tu proyecto.
        
        **1. Costos Iniciales:**
        - Ingresa el costo del **tanque de agua** (ejemplo: S/ 750)
        - Ingresa el costo de la **bomba eléctrica** (ejemplo: S/ 600)
        - Ingresa el costo de **tuberías e instalación** (ejemplo: S/ 400)
        - El sistema calculará automáticamente la **inversión total**
        
        **2. Parámetros del Proyecto:**
        - **Vida Útil:** Años que durará funcionando el sistema (típicamente 8-10 años)
        - **Ahorro Anual:** Cuánto dinero ahorrarás por año (ejemplo: S/ 700)
          - Considera: menor compra de agua, menos problemas, etc.
        - **Mantenimiento Anual:** Costo anual de mantenimiento (ejemplo: S/ 100)
        - **TMAR:** Tasa mínima que esperas ganar (10-12% es típico para proyectos domésticos)
        
        **3. Financiamiento (Opcional):**
        - Marca la casilla si vas a financiar la inversión
        - Ingresa la **tasa nominal** del préstamo
        - Define los **períodos de capitalización** (mensual = 12)
        - Indica el **plazo del préstamo** en meses
        - El sistema calculará la cuota mensual y tasa efectiva
        
        **4. Verificación:**
        - Revisa la **tabla resumen** al final
        - Verifica que todos los datos sean correctos
        - Los datos se guardan automáticamente
        
        ⚠️ **Importante:** Todos los datos que ingreses aquí se usarán en las demás secciones.
        """)
    
    with st.expander("📊 Cómo usar: ANÁLISIS FINANCIERO"):
        st.markdown("""
        Esta sección calcula automáticamente todos los indicadores financieros.
        
        **Qué encontrarás:**
        
        1. **Métricas Principales (tarjetas superiores):**
           - VAN: Si es positivo, el proyecto genera valor ✅
           - TIR: Compárala con tu TMAR. Si TIR > TMAR → viable ✅
           - B/C: Si es mayor a 1, es conveniente ✅
           - Payback: Cuánto tiempo tardas en recuperar tu inversión
        
        2. **Interpretación de Resultados:**
           - Cajas de color con explicaciones claras
           - Verde ✅ = bueno, Rojo ❌ = malo
           - Lee cada interpretación cuidadosamente
        
        3. **Flujo de Caja Proyectado:**
           - Tabla detallada año por año
           - Gráfico interactivo con barras y líneas
           - Puedes hacer hover para ver valores exactos
        
        **Cómo interpretar:**
        - Si VAN, TIR y B/C son favorables → **Proyecto viable**
        - Si la mayoría son desfavorables → **Revisar datos o no invertir**
        - Si hay resultados mixtos → **Revisar en análisis de sensibilidad**
        """)
    
    with st.expander("🔍 Cómo usar: ANÁLISIS DE SENSIBILIDAD"):
        st.markdown("""
        Aquí evaluarás qué pasa si las cosas no salen exactamente como planeaste.
        
        **Escenarios:**
        
        1. **Optimista (😃):**
           - Ajusta el slider para ver qué pasa si ahorras MÁS de lo esperado
           - Ejemplo: +15% = en vez de ahorrar S/ 700, ahorras S/ 805
        
        2. **Probable (😐):**
           - Es el escenario base con tus datos originales
           - Sin cambios
        
        3. **Pesimista (😟):**
           - Ajusta el slider para ver qué pasa si ahorras MENOS
           - Ejemplo: -15% = en vez de S/ 700, solo ahorras S/ 595
        
        **Análisis:**
        - Compara los tres escenarios en la tabla
        - Revisa el **Diagrama de Tornado** (gráfico de barras horizontal)
        - Observa el gráfico **VAN vs TMAR**
        
        **Pregunta clave:** ¿El proyecto sigue siendo viable incluso en el escenario pesimista?
        - Si SÍ → Proyecto muy robusto ✅
        - Si NO → Proyecto riesgoso ⚠️
        """)
    
    with st.expander("⚖️ Cómo usar: ANÁLISIS MULTICRITERIO"):
        st.markdown("""
        Compara diferentes alternativas considerando múltiples factores, no solo el costo.
        
        **Paso 1: Asignar Pesos**
        - Usa los sliders de la izquierda
        - Distribuye 1.0 (100%) entre los criterios
        - Si el costo es muy importante, dale más peso (ej: 0.40)
        - La suma DEBE ser 1.0 ✅
        
        **Paso 2: Calificar Alternativas**
        - **Opción A** (Sistema Económico): califica del 1 al 10 cada criterio
        - **Opción B** (Sistema Premium): califica del 1 al 10 cada criterio
        - Mientras más alto el número, mejor
        
        **Criterios típicos:**
        - **Costo:** 10 = muy barato, 1 = muy caro
        - **Capacidad:** 10 = excelente presión/capacidad, 1 = baja
        - **Consumo eléctrico:** 10 = consume poco, 1 = consume mucho
        - **Durabilidad:** 10 = dura muchos años, 1 = se daña rápido
        - **Mantenimiento:** 10 = casi no requiere, 1 = requiere mucho
        
        **Resultado:**
        - El sistema calcula el puntaje ponderado
        - Gana la opción con mayor puntaje
        - Revisa el **gráfico de radar** para ver visualmente las diferencias
        """)
    
    with st.expander("📈 Cómo usar: RESULTADOS INTEGRALES"):
        st.markdown("""
        Esta es la sección final donde obtienes la decisión y recomendación.
        
        **Dashboard de Indicadores:**
        - Resumen visual de todas las métricas
        - Fácil de leer y compartir
        
        **Matriz de Decisión:**
        - Verifica cuántos criterios cumple el proyecto
        - Si cumple 3 o 4 de 4 → **Altamente recomendado** ✅
        - Si cumple 2 → **Viable con condiciones** ⚠️
        - Si cumple 0 o 1 → **No recomendado** ❌
        
        **Conclusión Final:**
        - Lee la recomendación completa
        - Incluye justificación detallada
        - Considera beneficios no económicos (calidad de vida, valorización, etc.)
        
        **Resumen Ejecutivo:**
        - Tabla final con todos los datos
        - Puedes tomar captura de pantalla para presentar
        - Útil para decisiones en familia o asesorías
        """)
    
    st.divider()
    
    st.subheader("💡 Consejos y Mejores Prácticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✅ HACER:
        
        - **Datos realistas:** Usa costos y ahorros verificables
        - **Consultar precios:** Cotiza en ferreterías reales
        - **Estimar conservador:** Es mejor subestimar ahorros que sobreestimarlos
        - **Revisar todos los escenarios:** No solo el probable
        - **Documentar fuentes:** Anota de dónde sacaste los datos
        - **Comparar alternativas:** Evalúa al menos 2 opciones
        - **Considerar no económicos:** Calidad de vida, comodidad, salud
        - **Guardar resultados:** Toma capturas de pantalla
        """)
    
    with col2:
        st.error("""
        ### ❌ NO HACER:
        
        - **Datos inventados:** No uses valores al azar
        - **Solo ver el VAN:** Revisa todos los indicadores
        - **Ignorar el riesgo:** Siempre haz análisis de sensibilidad
        - **TMAR muy baja:** Ser realista (10-15% típico)
        - **Olvidar mantenimiento:** Siempre hay costos recurrentes
        - **Vida útil exagerada:** Ser conservador (8-10 años)
        - **Decisión apresurada:** Analiza bien todos los resultados
        - **Ignorar advertencias:** Si sale rojo ❌, hay un problema
        """)
    
    st.divider()
    
    st.subheader("❓ Preguntas Frecuentes (FAQ)")
    
    with st.expander("¿Qué hago si el VAN es negativo?"):
        st.markdown("""
        Si el VAN es negativo, el proyecto NO es viable económicamente. Opciones:
        
        1. **Reducir costos iniciales:** Busca proveedores más baratos
        2. **Aumentar ahorros:** Identifica más beneficios (¿vender agua a vecinos?)
        3. **Extender vida útil:** ¿Puede durar más de 8 años con buen mantenimiento?
        4. **Reducir TMAR:** ¿Es muy alta tu expectativa de retorno?
        5. **Considerar NO invertir:** A veces es la mejor decisión
        """)
    
    with st.expander("¿Cómo sé si mis datos son buenos?"):
        st.markdown("""
        **Para costos:**
        - Cotiza en al menos 3 ferreterías
        - Suma TODOS los costos (incluye transporte, instalador, accesorios)
        - Agrega 10-15% de imprevistos
        
        **Para ahorros:**
        - Calcula cuánto gastas en agua por cisterna
        - Estima pérdidas por no tener agua (tiempo, productos dañados)
        - Considera mejora en calidad de vida (difícil de cuantificar)
        - Sé conservador, mejor subestimar que sobreestimar
        """)
    
    with st.expander("¿Qué TMAR debo usar?"):
        st.markdown("""
        **Guía para elegir TMAR:**
        
        - **8-10%:** Si es tu casa y valoras mucho la comodidad
        - **10-12%:** Típico para proyectos domésticos
        - **12-15%:** Si tienes otras opciones de inversión
        - **15-20%:** Si el proyecto es riesgoso
        
        **Referencia:** Si podrías invertir ese dinero en un plazo fijo al 8%, 
        tu TMAR debería ser al menos 8% + premio al riesgo (2-4%).
        """)
    
    with st.expander("¿Puedo usar esto para otros proyectos?"):
        st.markdown("""
        Sí, aunque está diseñado para tanques de agua, la metodología aplica a:
        
        ✅ Paneles solares
        ✅ Sistemas de ahorro de energía
        ✅ Mejoras en el hogar (ventanas, aislamiento)
        ✅ Equipos que generen ahorros recurrentes
        ✅ Proyectos pequeños de negocio
        
        Solo ajusta los nombres y valores según tu proyecto.
        """)
    
    st.divider()
    
    st.info("""
    ### 🎓 Recursos Adicionales
    
    **Para profundizar en los conceptos:**
    - Revisa el **Glosario** para definiciones completas
    - Busca videos de ingeniería económica en YouTube
    - Consulta libros: "Ingeniería Económica" de Blank & Tarquin
    
    **Para obtener datos:**
    - Ferreterías locales (Sodimac, Maestro, etc.)
    - Cotizaciones de plomeros/instaladores
    - Recibos de agua de los últimos meses
    - Consulta a vecinos con sistemas similares
    """)

# ==================== DATOS DE INVERSIÓN ====================
elif opcion == "💰 Datos de Inversión":
    st.header("💰 Configuración de Datos de Inversión")
    
    st.info("ℹ️ **Los valores que ingreses aquí se guardarán automáticamente y se mantendrán al cambiar entre páginas.**")

    st.subheader("🔧 Costos Iniciales")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.number_input(
            "Tanque de Agua (1,100 L) - S/",
            min_value=0.0,
            step=50.0,
            key="costo_tanque",
            on_change=DataManager.update_inversion_inicial,
            help="Este valor se guardará automáticamente"
        )

    with col2:
        st.number_input(
            "Bomba Eléctrica ½ HP - S/",
            min_value=0.0,
            step=50.0,
            key="costo_bomba",
            on_change=DataManager.update_inversion_inicial,
            help="Este valor se guardará automáticamente"
        )

    with col3:
        st.number_input(
            "Tuberías e Instalación - S/",
            min_value=0.0,
            step=50.0,
            key="costo_instalacion",
            on_change=DataManager.update_inversion_inicial,
            help="Este valor se guardará automáticamente"
        )

    # Actualizar inversión inicial
    DataManager.update_inversion_inicial()

    st.success(
        f"### 💵 Inversión Inicial Total: S/ {st.session_state['inversion_inicial']:,.2f}"
    )

    st.divider()

    st.subheader("📅 Parámetros del Proyecto")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.number_input(
            "Vida Útil (años)",
            min_value=1,
            max_value=20,
            key="vida_util",
            help="Este valor se guardará automáticamente"
        )

    with col2:
        st.number_input(
            "Ahorro Anual Estimado - S/",
            min_value=0.0,
            step=50.0,
            key="ahorro_anual",
            help="Este valor se guardará automáticamente"
        )

    with col3:
        st.number_input(
            "Mantenimiento Anual - S/",
            min_value=0.0,
            step=10.0,
            key="mantenimiento_anual",
            help="Este valor se guardará automáticamente"
        )

    with col4:
        st.number_input(
            "TMAR (%)",
            min_value=0.0,
            max_value=50.0,
            step=0.5,
            key="tmar_porcentaje",
            on_change=DataManager.update_tmar,
            help="Este valor se guardará automáticamente"
        )

    # Actualizar TMAR
    DataManager.update_tmar()

    st.divider()

    st.subheader("🏦 Financiamiento (Opcional)")
    st.checkbox(
        "¿El proyecto será financiado?",
        key="financiado",
        help="Este valor se guardará automáticamente"
    )

    st.divider()
    
    # Validación de datos
    errores = DataManager.validate_data()
    if errores:
        st.warning("⚠️ **Advertencias:**")
        for error in errores:
            st.warning(f"• {error}")

    st.divider()

    st.subheader("📊 Resumen de Datos Ingresados")
    
    # Obtener datos actuales
    datos = DataManager.get_all_data()
    
    df_resumen = pd.DataFrame({
        "Concepto": [
            "Tanque de Agua",
            "Bomba Eléctrica",
            "Instalación",
            "TOTAL INVERSIÓN",
            "Ahorro Anual",
            "Mantenimiento Anual",
            "Flujo Neto Anual",
            "Vida Útil",
            "TMAR"
        ],
        "Valor": [
            f"S/ {datos['costo_tanque']:,.2f}",
            f"S/ {datos['costo_bomba']:,.2f}",
            f"S/ {datos['costo_instalacion']:,.2f}",
            f"S/ {datos['inversion_inicial']:,.2f}",
            f"S/ {datos['ahorro_anual']:,.2f}",
            f"S/ {datos['mantenimiento_anual']:,.2f}",
            f"S/ {datos['ahorro_anual'] - datos['mantenimiento_anual']:,.2f}",
            f"{datos['vida_util']} años",
            f"{datos['tmar']*100:.2f}%"
        ]
    })

    st.dataframe(df_resumen, width='stretch', hide_index=True)
    
    # Botón para resetear valores
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Resetear a valores por defecto", type="secondary"):
            DataManager.reset_to_defaults()
            st.rerun()
    with col2:
        st.success("✅ Todos los cambios se guardan automáticamente")


# ==================== ANÁLISIS FINANCIERO ====================
elif opcion == "📊 Análisis Financiero":
    st.header("📊 Análisis Financiero del Proyecto")
    
    # Recuperar datos
    if 'inversion_inicial' not in st.session_state:
        st.warning("⚠️ Por favor, primero ingresa los datos en la sección 'Datos de Inversión'")
    else:
        inversion_inicial = st.session_state['inversion_inicial']
        vida_util = st.session_state['vida_util']
        ahorro_anual = st.session_state['ahorro_anual']
        mantenimiento_anual = st.session_state['mantenimiento_anual']
        tmar = st.session_state['tmar']
        
        flujo_neto_anual = ahorro_anual - mantenimiento_anual
        flujos_netos = [flujo_neto_anual] * vida_util
        
        # Cálculos
        van = calcular_van(inversion_inicial, flujos_netos, tmar)
        vae = calcular_vae(van, tmar, vida_util)
        tir = calcular_tir(inversion_inicial, flujos_netos)
        bc = calcular_bc(ahorro_anual, mantenimiento_anual, tmar, vida_util)
        payback_simple = calcular_payback(inversion_inicial, flujos_netos)
        payback_desc = calcular_payback_descontado(inversion_inicial, flujos_netos, tmar)
        
        # Métricas principales
        st.subheader("📈 Indicadores Financieros Principales")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Valor Actual Neto (VAN)", f"S/ {van:,.2f}", 
                     "✅ Proyecto Viable" if van > 0 else "❌ No Viable")
            st.metric("Valor Anual Equivalente (VAE)", f"S/ {vae:,.2f}")
        
        with col2:
            st.metric("Tasa Interna de Retorno (TIR)", f"{tir*100:.2f}%",
                     f"{'✅' if tir > tmar else '❌'} TMAR: {tmar*100:.2f}%")
            st.metric("Relación B/C", f"{bc:.3f}",
                     "✅ Conveniente" if bc > 1 else "❌ No Conveniente")
        
        with col3:
            st.metric("Payback Simple", f"{payback_simple:.2f} años" if payback_simple else "N/A")
            st.metric("Payback Descontado", f"{payback_desc:.2f} años" if payback_desc else "N/A")
        
        st.divider()
        
        # Interpretación
        st.subheader("📝 Interpretación de Resultados")
        
        if van > 0:
            st.success(f"""
            ✅ **VAN = S/ {van:,.2f}** (Positivo)
            - El proyecto es **económicamente viable**
            - Se genera valor adicional de S/ {van:,.2f} en términos actuales
            """)
        else:
            st.error(f"""
            ❌ **VAN = S/ {van:,.2f}** (Negativo)
            - El proyecto **NO es económicamente viable**
            - Se perdería S/ {abs(van):,.2f} en términos actuales
            """)
        
        if tir > tmar:
            st.success(f"""
            ✅ **TIR = {tir*100:.2f}%** > **TMAR = {tmar*100:.2f}%**
            - El proyecto es **rentable**
            - La rentabilidad supera la tasa mínima requerida
            """)
        else:
            st.error(f"""
            ❌ **TIR = {tir*100:.2f}%** < **TMAR = {tmar*100:.2f}%**
            - El proyecto **NO es rentable**
            - No alcanza la tasa mínima de retorno esperada
            """)
        
        if bc > 1:
            st.success(f"""
            ✅ **B/C = {bc:.3f}** (Mayor a 1)
            - Por cada sol invertido, se recibe S/ {bc:.2f}
            - El proyecto es **conveniente**
            """)
        else:
            st.error(f"""
            ❌ **B/C = {bc:.3f}** (Menor a 1)
            - Por cada sol invertido, se recibe S/ {bc:.2f}
            - El proyecto **NO es conveniente**
            """)
        
        st.divider()
        
        # Flujo de Caja
        st.subheader("💰 Flujo de Caja Proyectado")
        
        años = list(range(0, vida_util + 1))
        flujos = [-inversion_inicial] + flujos_netos
        flujos_acumulados = [flujos[0]]
        for i in range(1, len(flujos)):
            flujos_acumulados.append(flujos_acumulados[-1] + flujos[i])
        
        df_flujos = pd.DataFrame({
            'Año': años,
            'Ahorro': [0] + [ahorro_anual] * vida_util,
            'Mantenimiento': [0] + [mantenimiento_anual] * vida_util,
            'Flujo Neto': flujos,
            'Flujo Acumulado': flujos_acumulados
        })
        
        st.dataframe(df_flujos.style.format({
            'Ahorro': 'S/ {:,.2f}',
            'Mantenimiento': 'S/ {:,.2f}',
            'Flujo Neto': 'S/ {:,.2f}',
            'Flujo Acumulado': 'S/ {:,.2f}'
        }), width='stretch', hide_index=True)
        
        # Gráfico de flujos
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_flujos['Año'], y=df_flujos['Flujo Neto'], 
                            name='Flujo Neto Anual',
                            marker_color=['red' if x < 0 else 'green' for x in df_flujos['Flujo Neto']]))
        fig.add_trace(go.Scatter(x=df_flujos['Año'], y=df_flujos['Flujo Acumulado'], 
                                name='Flujo Acumulado',
                                mode='lines+markers', line=dict(color='blue', width=3)))
        
        fig.update_layout(
            title="Flujo de Caja del Proyecto",
            xaxis_title="Año",
            yaxis_title="Monto (S/)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, width='stretch')

# ==================== ANÁLISIS DE SENSIBILIDAD ====================
elif opcion == "🔍 Análisis de Sensibilidad":
    st.header("🔍 Análisis de Sensibilidad")
    st.markdown("Evalúa cómo cambian los resultados ante variaciones en los parámetros clave")
    
    if 'inversion_inicial' not in st.session_state:
        st.warning("⚠️ Por favor, primero ingresa los datos en la sección 'Datos de Inversión'")
    else:
        inversion_inicial = st.session_state['inversion_inicial']
        vida_util = st.session_state['vida_util']
        ahorro_anual_base = st.session_state['ahorro_anual']
        mantenimiento_anual = st.session_state['mantenimiento_anual']
        tmar = st.session_state['tmar']
        
        st.subheader("🎲 Escenarios de Análisis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("### 😃 Escenario Optimista")
            var_optimista = st.slider("Ahorro aumenta:", 0, 30, 15, key='opt') / 100
            ahorro_opt = ahorro_anual_base * (1 + var_optimista)
            flujo_opt = ahorro_opt - mantenimiento_anual
            flujos_opt = [flujo_opt] * vida_util
            van_opt = calcular_van(inversion_inicial, flujos_opt, tmar)
            tir_opt = calcular_tir(inversion_inicial, flujos_opt)
            
            st.metric("Ahorro Anual", f"S/ {ahorro_opt:,.2f}")
            st.metric("VAN", f"S/ {van_opt:,.2f}")
            st.metric("TIR", f"{tir_opt*100:.2f}%")
        
        with col2:
            st.warning("### 😐 Escenario Probable")
            ahorro_prob = ahorro_anual_base
            flujo_prob = ahorro_prob - mantenimiento_anual
            flujos_prob = [flujo_prob] * vida_util
            van_prob = calcular_van(inversion_inicial, flujos_prob, tmar)
            tir_prob = calcular_tir(inversion_inicial, flujos_prob)
            
            st.metric("Ahorro Anual", f"S/ {ahorro_prob:,.2f}")
            st.metric("VAN", f"S/ {van_prob:,.2f}")
            st.metric("TIR", f"{tir_prob*100:.2f}%")
        
        with col3:
            st.error("### 😟 Escenario Pesimista")
            var_pesimista = st.slider("Ahorro disminuye:", 0, 30, 15, key='pes') / 100
            ahorro_pes = ahorro_anual_base * (1 - var_pesimista)
            flujo_pes = ahorro_pes - mantenimiento_anual
            flujos_pes = [flujo_pes] * vida_util
            van_pes = calcular_van(inversion_inicial, flujos_pes, tmar)
            tir_pes = calcular_tir(inversion_inicial, flujos_pes)
            
            st.metric("Ahorro Anual", f"S/ {ahorro_pes:,.2f}")
            st.metric("VAN", f"S/ {van_pes:,.2f}")
            st.metric("TIR", f"{tir_pes*100:.2f}%")
        
        st.divider()
        
        # Tabla comparativa
        st.subheader("📊 Comparación de Escenarios")
        df_escenarios = pd.DataFrame({
            'Escenario': ['Optimista', 'Probable', 'Pesimista'],
            'Ahorro Anual': [ahorro_opt, ahorro_prob, ahorro_pes],
            'VAN': [van_opt, van_prob, van_pes],
            'TIR (%)': [tir_opt*100, tir_prob*100, tir_pes*100],
            'Decisión': [
                '✅ Viable' if van_opt > 0 else '❌ No Viable',
                '✅ Viable' if van_prob > 0 else '❌ No Viable',
                '✅ Viable' if van_pes > 0 else '❌ No Viable'
            ]
        })
        
        st.dataframe(df_escenarios.style.format({
            'Ahorro Anual': 'S/ {:,.2f}',
            'VAN': 'S/ {:,.2f}',
            'TIR (%)': '{:.2f}%'
        }), width='stretch', hide_index=True)
        
        # Gráfico de tornado
        st.subheader("🌪️ Diagrama de Tornado - Sensibilidad del VAN")
        
        fig = go.Figure()
        
        escenarios = ['Pesimista', 'Probable', 'Optimista']
        vans = [van_pes, van_prob, van_opt]
        colores = ['red', 'orange', 'green']
        
        fig.add_trace(go.Bar(
            y=escenarios,
            x=vans,
            orientation='h',
            marker=dict(color=colores),
            text=[f'S/ {v:,.0f}' for v in vans],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Sensibilidad del VAN según Escenarios",
            xaxis_title="VAN (S/)",
            yaxis_title="Escenario",
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
        
        st.divider()
        
        # Análisis de variación de TMAR
        st.subheader("📉 Sensibilidad del VAN vs TMAR")
        
        tasas = np.linspace(0.05, 0.25, 20)
        vans_tasas = [calcular_van(inversion_inicial, flujos_prob, t) for t in tasas]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=tasas*100, y=vans_tasas, mode='lines+markers',
                                 name='VAN', line=dict(color='blue', width=3)))
        fig2.add_hline(y=0, line_dash="dash", line_color="red", 
                      annotation_text="VAN = 0")
        fig2.add_vline(x=tmar*100, line_dash="dash", line_color="green",
                      annotation_text=f"TMAR actual: {tmar*100:.1f}%")
        
        fig2.update_layout(
            title="Variación del VAN según Tasa de Descuento",
            xaxis_title="Tasa de Descuento (%)",
            yaxis_title="VAN (S/)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig2, width='stretch')

# ==================== ANÁLISIS MULTICRITERIO ====================
elif opcion == "⚖️ Análisis Multicriterio":
    st.header("⚖️ Análisis Multicriterio - Comparación de Alternativas")
    st.markdown("Compara diferentes opciones de tanques y bombas considerando múltiples atributos")
    
    st.subheader("🎯 Definición de Criterios y Pesos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Asigna pesos a cada criterio")
        peso_costo = st.slider("Costo Inicial", 0.0, 1.0, 0.30, 0.05)
        peso_capacidad = st.slider("Capacidad/Presión", 0.0, 1.0, 0.25, 0.05)
        peso_consumo = st.slider("Consumo Eléctrico", 0.0, 1.0, 0.20, 0.05)
        peso_durabilidad = st.slider("Durabilidad", 0.0, 1.0, 0.15, 0.05)
        peso_mantenimiento = st.slider("Bajo Mantenimiento", 0.0, 1.0, 0.10, 0.05)
        
        suma_pesos = peso_costo + peso_capacidad + peso_consumo + peso_durabilidad + peso_mantenimiento
        
        if abs(suma_pesos - 1.0) > 0.01:
            st.error(f"⚠️ La suma de pesos debe ser 1.0 (actual: {suma_pesos:.2f})")
        else:
            st.success(f"✅ Suma de pesos: {suma_pesos:.2f}")
    
    with col2:
        st.markdown("#### Descripción de Alternativas")
        st.info("""
        **Opción A: Sistema Económico**
        - Tanque plástico 1,100 L
        - Bomba pequeña ½ HP
        - Menor costo inicial
        - Capacidad estándar
        
        **Opción B: Sistema Premium**
        - Tanque reforzado 1,500 L
        - Bomba potente ¾ HP
        - Mayor inversión
        - Mayor capacidad y durabilidad
        """)
    
    st.divider()
    
    st.subheader("📊 Evaluación de Alternativas")
    st.markdown("Califica cada alternativa del 1 al 10 para cada criterio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔵 Opción A: Sistema Económico")
        a_costo = st.slider("Costo (A)", 1, 10, 9, key='a_cost')
        a_capacidad = st.slider("Capacidad (A)", 1, 10, 7, key='a_cap')
        a_consumo = st.slider("Consumo (A)", 1, 10, 9, key='a_cons')
        a_durabilidad = st.slider("Durabilidad (A)", 1, 10, 8, key='a_dur')
        a_mantenimiento = st.slider("Mantenimiento (A)", 1, 10, 9, key='a_mant')
    
    with col2:
        st.markdown("### 🟢 Opción B: Sistema Premium")
        b_costo = st.slider("Costo (B)", 1, 10, 7, key='b_cost')
        b_capacidad = st.slider("Capacidad (B)", 1, 10, 10, key='b_cap')
        b_consumo = st.slider("Consumo (B)", 1, 10, 8, key='b_cons')
        b_durabilidad = st.slider("Durabilidad (B)", 1, 10, 10, key='b_dur')
        b_mantenimiento = st.slider("Mantenimiento (B)", 1, 10, 7, key='b_mant')
    
    # Cálculo de puntuaciones ponderadas
    if abs(suma_pesos - 1.0) <= 0.01:
        puntaje_a = (a_costo * peso_costo + 
                    a_capacidad * peso_capacidad + 
                    a_consumo * peso_consumo + 
                    a_durabilidad * peso_durabilidad + 
                    a_mantenimiento * peso_mantenimiento)
        
        puntaje_b = (b_costo * peso_costo + 
                    b_capacidad * peso_capacidad + 
                    b_consumo * peso_consumo + 
                    b_durabilidad * peso_durabilidad + 
                    b_mantenimiento * peso_mantenimiento)
        
        st.divider()
        
        st.subheader("🏆 Resultados del Análisis Multicriterio")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.metric("Puntuación Opción A", f"{puntaje_a:.2f}")
        
        with col2:
            st.metric("Puntuación Opción B", f"{puntaje_b:.2f}")
        
        with col3:
            if puntaje_a > puntaje_b:
                st.success("🏆 **Ganador: Opción A**")
                st.metric("Diferencia", f"+{puntaje_a - puntaje_b:.2f}")
            elif puntaje_b > puntaje_a:
                st.success("🏆 **Ganador: Opción B**")
                st.metric("Diferencia", f"+{puntaje_b - puntaje_a:.2f}")
            else:
                st.info("🤝 **Empate**")
        
        # Tabla detallada
        st.subheader("📋 Tabla de Evaluación Detallada")
        
        df_multi = pd.DataFrame({
            'Criterio': ['Costo Inicial', 'Capacidad/Presión', 'Consumo Eléctrico', 
                        'Durabilidad', 'Bajo Mantenimiento', 'TOTAL PONDERADO'],
            'Peso': [peso_costo, peso_capacidad, peso_consumo, peso_durabilidad, 
                    peso_mantenimiento, 1.0],
            'Opción A (Calificación)': [a_costo, a_capacidad, a_consumo, a_durabilidad, 
                                       a_mantenimiento, 0],
            'Opción A (Ponderado)': [
                a_costo * peso_costo,
                a_capacidad * peso_capacidad,
                a_consumo * peso_consumo,
                a_durabilidad * peso_durabilidad,
                a_mantenimiento * peso_mantenimiento,
                puntaje_a
            ],
            'Opción B (Calificación)': [b_costo, b_capacidad, b_consumo, b_durabilidad, 
                                       b_mantenimiento, 0],
            'Opción B (Ponderado)': [
                b_costo * peso_costo,
                b_capacidad * peso_capacidad,
                b_consumo * peso_consumo,
                b_durabilidad * peso_durabilidad,
                b_mantenimiento * peso_mantenimiento,
                puntaje_b
            ]
        })
        
        st.dataframe(df_multi.style.format({
            'Peso': '{:.2f}',
            'Opción A (Ponderado)': '{:.2f}',
            'Opción B (Ponderado)': '{:.2f}'
        }), width='stretch', hide_index=True)
        
        # Gráfico radar
        st.subheader("📡 Gráfico de Radar - Comparación Visual")
        
        categorias = ['Costo', 'Capacidad', 'Consumo', 'Durabilidad', 'Mantenimiento']
        valores_a = [a_costo, a_capacidad, a_consumo, a_durabilidad, a_mantenimiento]
        valores_b = [b_costo, b_capacidad, b_consumo, b_durabilidad, b_mantenimiento]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valores_a + [valores_a[0]],
            theta=categorias + [categorias[0]],
            fill='toself',
            name='Opción A',
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=valores_b + [valores_b[0]],
            theta=categorias + [categorias[0]],
            fill='toself',
            name='Opción B',
            line=dict(color='green')
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            height=500,
            title="Comparación de Atributos"
        )
        
        st.plotly_chart(fig, width='stretch')

# ==================== RESULTADOS INTEGRALES ====================
elif opcion == "📈 Resultados Integrales":
    st.header("📈 Resultados Integrales y Conclusiones")
    
    if 'inversion_inicial' not in st.session_state:
        st.warning("⚠️ Por favor, primero ingresa los datos en la sección 'Datos de Inversión'")
    else:
        inversion_inicial = st.session_state['inversion_inicial']
        vida_util = st.session_state['vida_util']
        ahorro_anual = st.session_state['ahorro_anual']
        mantenimiento_anual = st.session_state['mantenimiento_anual']
        tmar = st.session_state['tmar']
        
        flujo_neto_anual = ahorro_anual - mantenimiento_anual
        flujos_netos = [flujo_neto_anual] * vida_util
        
        # Cálculos
        van = calcular_van(inversion_inicial, flujos_netos, tmar)
        vae = calcular_vae(van, tmar, vida_util)
        tir = calcular_tir(inversion_inicial, flujos_netos)
        bc = calcular_bc(ahorro_anual, mantenimiento_anual, tmar, vida_util)
        payback_simple = calcular_payback(inversion_inicial, flujos_netos)
        payback_desc = calcular_payback_descontado(inversion_inicial, flujos_netos, tmar)
        
        # Dashboard de métricas
        st.subheader("📊 Dashboard de Indicadores")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("VAN", f"S/ {van:,.2f}", 
                     "Viable" if van > 0 else "No Viable",
                     delta_color="normal" if van > 0 else "inverse")
        
        with col2:
            st.metric("TIR", f"{tir*100:.2f}%",
                     f"vs TMAR {tmar*100:.2f}%",
                     delta_color="normal" if tir > tmar else "inverse")
        
        with col3:
            st.metric("B/C", f"{bc:.3f}",
                     "Conveniente" if bc > 1 else "No Conveniente",
                     delta_color="normal" if bc > 1 else "inverse")
        
        with col4:
            st.metric("Payback", f"{payback_desc:.1f} años" if payback_desc else "N/A",
                     f"de {vida_util} años")
        
        st.divider()
        
        # Matriz de decisión
        st.subheader("✅ Matriz de Decisión")
        
        criterios_cumplidos = 0
        total_criterios = 4
        
        col1, col2 = st.columns(2)
        
        with col1:
            if van > 0:
                st.success("✅ VAN > 0: Proyecto crea valor")
                criterios_cumplidos += 1
            else:
                st.error("❌ VAN < 0: Proyecto destruye valor")
            
            if tir > tmar:
                st.success(f"✅ TIR ({tir*100:.2f}%) > TMAR ({tmar*100:.2f}%)")
                criterios_cumplidos += 1
            else:
                st.error(f"❌ TIR ({tir*100:.2f}%) < TMAR ({tmar*100:.2f}%)")
        
        with col2:
            if bc > 1:
                st.success(f"✅ B/C ({bc:.2f}) > 1: Beneficios superan costos")
                criterios_cumplidos += 1
            else:
                st.error(f"❌ B/C ({bc:.2f}) < 1: Costos superan beneficios")
            
            if payback_desc and payback_desc < vida_util:
                st.success(f"✅ Payback ({payback_desc:.1f} años) < Vida Útil ({vida_util} años)")
                criterios_cumplidos += 1
            else:
                st.warning("⚠️ Payback muy largo o indefinido")
        
        st.divider()
        
        # Conclusión final
        st.subheader("🎯 Conclusión y Recomendación Final")
        
        porcentaje_aprobacion = (criterios_cumplidos / total_criterios) * 100
        
        if porcentaje_aprobacion >= 75:
            st.success(f"""
            ### ✅ PROYECTO ALTAMENTE RECOMENDADO
            
            **Criterios cumplidos: {criterios_cumplidos} de {total_criterios} ({porcentaje_aprobacion:.0f}%)**
            
            #### Justificación:
            - El proyecto presenta indicadores financieros favorables
            - La inversión de S/ {inversion_inicial:,.2f} se recupera en {payback_desc:.1f} años
            - Se genera un valor actual neto de S/ {van:,.2f}
            - La rentabilidad ({tir*100:.2f}%) supera ampliamente el mínimo requerido ({tmar*100:.2f}%)
            - Por cada sol invertido se obtienen S/ {bc:.2f} en beneficios
            
            #### Recomendación:
            **PROCEDER CON LA INVERSIÓN**. El proyecto no solo es viable económicamente, 
            sino que además proporcionará beneficios adicionales como:
            - Mejora en la calidad de vida (agua con presión constante)
            - Independencia de cortes de servicio
            - Valorización de la vivienda
            """)
        elif porcentaje_aprobacion >= 50:
            st.warning(f"""
            ### ⚠️ PROYECTO VIABLE CON CONDICIONES
            
            **Criterios cumplidos: {criterios_cumplidos} de {total_criterios} ({porcentaje_aprobacion:.0f}%)**
            
            #### Situación:
            - El proyecto cumple algunos criterios de viabilidad
            - Existen riesgos que deben considerarse
            - VAN: S/ {van:,.2f}
            - TIR: {tir*100:.2f}% vs TMAR: {tmar*100:.2f}%
            
            #### Recomendación:
            **EVALUAR OPCIONES**:
            - Considerar financiamiento si es posible
            - Buscar proveedores con mejores precios
            - Evaluar alternativas de menor costo
            - Realizar análisis de sensibilidad detallado
            """)
        else:
            st.error(f"""
            ### ❌ PROYECTO NO RECOMENDADO
            
            **Criterios cumplidos: {criterios_cumplidos} de {total_criterios} ({porcentaje_aprobacion:.0f}%)**
            
            #### Problemas identificados:
            - La mayoría de indicadores financieros son desfavorables
            - VAN: S/ {van:,.2f} (Negativo)
            - TIR: {tir*100:.2f}% (Inferior a TMAR)
            - La inversión no se justifica económicamente
            
            #### Recomendación:
            **NO PROCEDER** con la inversión actual. Considerar:
            - Reevaluar costos de inversión
            - Buscar alternativas más económicas
            - Esperar a que mejoren las condiciones
            - Explorar otras soluciones al problema de agua
            """)
        
        st.divider()
        
        # Gráfico de resumen
        st.subheader("📊 Resumen Visual de Indicadores")
        
        fig = go.Figure()
        
        # Normalizar valores para visualización
        van_norm = min(van / 1000, 10) if van > 0 else 0
        tir_norm = min(tir * 100 / 10, 10)
        bc_norm = min(bc * 3, 10)
        payback_norm = 10 - min(payback_desc / vida_util * 10, 10) if payback_desc else 0
        
        valores = [van_norm, tir_norm, bc_norm, payback_norm]
        indicadores = ['VAN<br>(normalizado)', 'TIR<br>(%)', 'B/C<br>(x3)', 'Payback<br>(invertido)']
        
        colores = ['green' if v >= 5 else 'orange' if v >= 3 else 'red' for v in valores]
        
        fig.add_trace(go.Bar(
            x=indicadores,
            y=valores,
            marker=dict(color=colores),
            text=[f'{v:.1f}' for v in valores],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Indicadores Clave del Proyecto (Valores Normalizados 0-10)",
            yaxis_title="Puntuación",
            height=400,
            yaxis=dict(range=[0, 10])
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Tabla de resumen ejecutivo
        st.subheader("📋 Resumen Ejecutivo")
        
        df_ejecutivo = pd.DataFrame({
            'Concepto': [
                'Inversión Inicial',
                'Vida Útil del Proyecto',
                'Ahorro Anual Bruto',
                'Mantenimiento Anual',
                'Flujo Neto Anual',
                'TMAR',
                '',
                'VAN',
                'VAE',
                'TIR',
                'Relación B/C',
                'Payback Simple',
                'Payback Descontado',
                '',
                'DECISIÓN'
            ],
            'Valor': [
                f'S/ {inversion_inicial:,.2f}',
                f'{vida_util} años',
                f'S/ {ahorro_anual:,.2f}',
                f'S/ {mantenimiento_anual:,.2f}',
                f'S/ {flujo_neto_anual:,.2f}',
                f'{tmar*100:.2f}%',
                '',
                f'S/ {van:,.2f}',
                f'S/ {vae:,.2f}',
                f'{tir*100:.2f}%',
                f'{bc:.3f}',
                f'{payback_simple:.2f} años' if payback_simple else 'N/A',
                f'{payback_desc:.2f} años' if payback_desc else 'N/A',
                '',
                '✅ VIABLE' if criterios_cumplidos >= 3 else '⚠️ REVISAR' if criterios_cumplidos >= 2 else '❌ NO VIABLE'
            ]
        })
        
        st.dataframe(df_ejecutivo, width='stretch', hide_index=True)

# Footer
st.divider()
st.caption("💧 Evaluación Económica - Tanque de Agua | Ingeniería Económica | Desarrollado con Streamlit")
