import datetime
import random
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# ==========================================
st.set_page_config(
    page_title="Programa de Rehabilitación Cognitiva y Adherencia",
    page_icon="🧠",
    layout="wide",
)

# Significado práctico de fichas (Opción 2 - uso exclusivamente simulado)
FICHAS_OPCIONES = {
    "Azul — Rutina / toma simulada normal": "Azul (Rutina / toma normal)",
    "Verde — Sin ayuda o tras pausa/regulación": "Verde (Sin ayuda / tras pausa)",
    "Naranja — Tras interrupción o con apoyo/pista": "Naranja (Interrupción / con apoyo)",
    "Sin ficha": "Sin ficha",
}

# Inicializar variables de memoria de la sesión
if "registros" not in st.session_state:
  st.session_state.registros = []
if "alarma_activa" not in st.session_state:
  st.session_state.alarma_activa = False
if "inicio_alarma" not in st.session_state:
  st.session_state.inicio_alarma = None
if "conteo_brujula" not in st.session_state:
  st.session_state.conteo_brujula = 0
if "matriz_regla" not in st.session_state:
  st.session_state.matriz_regla = "Tachar todos los CÍRCULOS AZULES (🔵)"
if "matriz_items" not in st.session_state:
  simbolos = ["🔵", "🔴", "🟢", "🔺", "🟥", "🟩"]
  st.session_state.matriz_items = [random.choice(simbolos) for _ in range(24)]
if "sonar_alarma" not in st.session_state:
  st.session_state.sonar_alarma = False
if "sonar_senal" not in st.session_state:
  st.session_state.sonar_senal = False


def reproducir_tono(frecuencia=880, duracion_seg=0.45, repeticiones=2):
  """Genera un sonido de alarma o señal directamente en el navegador."""
  codigo_audio = f"""
    <script>
    (function() {{
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        for (let i = 0; i < {repeticiones}; i++) {{
            const startTime = ctx.currentTime + i * ({duracion_seg} + 0.15);
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime({frecuencia}, startTime);
            gain.gain.setValueAtTime(0.25, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + {duracion_seg});
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(startTime);
            osc.stop(startTime + {duracion_seg});
        }}
    }})();
    </script>
    """
  components.html(codigo_audio, height=0)


def registrar_evento(modulo, actividad, detalle, bateria_actual):
  hora = datetime.datetime.now().strftime("%H:%M:%S")
  st.session_state.registros.append({
      "Hora": hora,
      "Módulo": modulo,
      "Actividad": actividad,
      "Detalle / Resultado": detalle,
      "Batería Mental": f"{bateria_actual}/10",
  })


def mostrar_tarjeta_registro(bateria_actual, ubicacion_key="sidebar"):
  """Renderiza una ficha visual para registrar ficha, hora, señal y comprobación."""
  with st.container(border=True):
    st.markdown("### 🗂️ Tarjeta de Registro")
    st.caption(
        "🔵 Azul: rutina/toma normal | 🟢 Verde: sin ayuda o tras pausa |"
        " 🟠 Naranja: interrupción o con apoyo"
    )

    c1, c2 = st.columns(2)
    with c1:
      hora_ficha = st.text_input(
          "Hora registrada:",
          value=datetime.datetime.now().strftime("%H:%M"),
          key=f"hora_ficha_{ubicacion_key}",
      )
    with c2:
      etiqueta_ficha = st.selectbox(
          "Ficha:",
          list(FICHAS_OPCIONES.keys()),
          key=f"color_ficha_{ubicacion_key}",
      )
      color_ficha = FICHAS_OPCIONES[etiqueta_ficha]

    senal_ficha = st.selectbox(
        "Señal o actividad:",
        [
            "Alarma ficticia",
            "Misión «brújula»",
            "Interrupción de tarea",
            "Rutina / agenda",
        ],
        key=f"senal_ficha_{ubicacion_key}",
    )

    verificado = st.checkbox(
        "Verifiqué la indicación y registré la toma/acción simulada",
        key=f"verificado_{ubicacion_key}",
    )
    observacion = st.text_input(
        "Nota / apoyo requerido:",
        placeholder="Ej. Sin ayuda / con pista",
        key=f"obs_ficha_{ubicacion_key}",
    )

    if st.button(
        "➕ Guardar Tarjeta",
        key=f"btn_guardar_ficha_{ubicacion_key}",
        use_container_width=True,
    ):
      registrar_evento(
          "Tarjeta de Registro",
          f"Ficha {color_ficha} ({senal_ficha})",
          (
              f"Hora: {hora_ficha} | Verificado: {verificado} | Nota:"
              f" {observacion}"
          ),
          bateria_actual,
      )
      st.success("Tarjeta guardada en la bitácora.")


# Disparar audio si se activó en este ciclo
if st.session_state.sonar_alarma:
  reproducir_tono(frecuencia=920, duracion_seg=0.35, repeticiones=3)
  st.session_state.sonar_alarma = False

if st.session_state.sonar_senal:
  reproducir_tono(frecuencia=620, duracion_seg=0.25, repeticiones=1)
  st.session_state.sonar_senal = False


# ==========================================
# ENCABEZADO Y PANEL TRANSVERSAL (BATERÍA + ALARMA)
# ==========================================
st.title("🧠 Programa Integral de Entrenamiento Cognitivo y Adherencia")
st.caption(
    "Herramienta interactiva de apoyo clínico y entrenamiento funcional"
    " (Sesiones 1 a 12 — actividad exclusivamente simulada)"
)

col1, col2, col3 = st.columns([2.2, 1, 1.2])

with col1:
  bateria = st.slider(
      "🔋 Escala de Batería Mental / Fatiga (0 = Sin fatiga | 10 = Máxima"
      " fatiga)",
      min_value=0,
      max_value=10,
      value=4,
  )
  if bateria <= 3:
    st.caption("🟢 Estado óptimo: Continuar con normalidad.")
  elif bateria <= 6:
    st.caption(
        "🟡 Precaución: Monitorear señales de cansancio o programar pausa."
    )
  else:
    st.caption(
        "🔴 Fatiga elevada: Reducir dificultad, hacer pausa o pedir apoyo."
    )

with col2:
  st.write("")
  if st.button("🔔 Activar Alarma Ficticia", use_container_width=True):
    st.session_state.alarma_activa = True
    st.session_state.sonar_alarma = True
    st.session_state.inicio_alarma = time.time()
    registrar_evento(
        "Transversal",
        "Alarma de adherencia",
        "Alarma ficticia activada (con sonido)",
        bateria,
    )
    st.rerun()

with col3:
  st.write("")
  if st.session_state.alarma_activa:
    if st.button(
        "✅ Completar Cadena y Retomar",
        type="primary",
        use_container_width=True,
    ):
      tiempo_reaccion = round(time.time() - st.session_state.inicio_alarma, 1)
      st.session_state.alarma_activa = False
      registrar_evento(
          "Transversal",
          "Cadena de adherencia completada",
          f"Tiempo de respuesta: {tiempo_reaccion} seg",
          bateria,
      )
      st.toast(f"Cadena registrada en {tiempo_reaccion}s. ¡Retoma tu tarea!")
      st.rerun()

if st.session_state.alarma_activa:
  st.error(
      "🚨 **¡ALARMA DE MEDICACIÓN SIMULADA!**\n\n"
      "1. **Detén** la actividad actual y señala dónde te quedaste.\n"
      "2. **Consulta** tu tarjeta de indicación.\n"
      "3. **Simula** la toma con la ficha correspondiente.\n"
      "4. **Marca** tu bitácora y presiona *'Completar Cadena y Retomar'*."
  )

st.divider()

# ==========================================
# MENÚ LATERAL DE MÓDULOS Y TARJETA DE REGISTRO
# ==========================================
st.sidebar.header("📋 Módulos del Programa")
modulo = st.sidebar.radio(
    "Selecciona el área de trabajo:",
    [
        "1. Atención, Señales y Rutina (S1, S2, S7)",
        "2. Fatiga y Autorregulación (S3, S11)",
        "3. Memoria de Trabajo y Ejecutivas (S4, S5, S6)",
        "4. Memoria Episódica y Comunicación (S8, S9)",
        "5. Circuito Integrador Final (S10, S12)",
        "📊 Bitácora y Descarga de Resultados",
    ],
)

st.sidebar.divider()
mostrar_tarjeta_registro(bateria, ubicacion_key="sidebar")


# ==========================================
# MÓDULO 1: ATENCIÓN, SEÑALES Y RUTINA
# ==========================================
if modulo == "1. Atención, Señales y Rutina (S1, S2, S7)":
  tab1, tab2, tab3 = st.tabs([
      "🚦 Semáforo y Pasos de Rutina (S1)",
      "🧭 Misión del Explorador (S2)",
      "🔄 Matrices de Alternancia (S7)",
  ])

  with tab1:
    st.subheader("El Semáforo de mi Rutina")
    st.write(
        "Clasifica cada situación según cómo impacta en el cumplimiento de la"
        " rutina:"
    )

    situaciones = [
        "Dormir bien y descansar toda la noche",
        "Estar en una reunión o ocupado cuando suena la alarma",
        "Sentir estrés o fatiga acumulada",
        "Tener el pastillero y la tarjeta de registro a la vista",
        "Salir de casa con prisa sin revisar la agenda",
        "Contar con recordatorios tranquilos de un familiar",
    ]
    clasificaciones = {}
    cols = st.columns(2)
    for i, sit in enumerate(situaciones):
      with cols[i % 2]:
        clasificaciones[sit] = st.selectbox(
            sit,
            [
                "Sin clasificar",
                "🟢 Verde (Me ayuda)",
                "🟡 Amarillo (Debo prestar atención)",
                "🔴 Rojo (Puede dificultar)",
            ],
            key=f"sem_{i}",
        )

    st.markdown("#### Ordena los 4 pasos de una rutina segura")
    pasos_ordenados = st.multiselect(
        "Selecciona los pasos en el orden correcto (del 1 al 4):",
        [
            "Realizar la actividad / toma simulada",
            "Comprobar y marcar en el registro",
            "Recibir recordatorio o alarma",
            "Revisar indicación en la tarjeta",
        ],
    )
    nota_s1 = st.text_input(
        "Estrategias de apoyo que utiliza habitualmente (alarma, agenda,"
        " notas, etc.):"
    )

    if st.button("Guardar Actividad Sesión 1"):
      orden_correcto = pasos_ordenados == [
          "Recibir recordatorio o alarma",
          "Revisar indicación en la tarjeta",
          "Realizar la actividad / toma simulada",
          "Comprobar y marcar en el registro",
      ]
      registrar_evento(
          "Módulo 1",
          "Semáforo y Orden de Rutina",
          f"Orden correcto: {orden_correcto} | Apoyos: {nota_s1}",
          bateria,
      )
      st.success("Actividad guardada en bitácora.")

  with tab2:
    st.subheader("La Misión del Explorador: Escucha, Presiona y Registra")
    st.info(
        "**Relato:** «Al amanecer, el explorador guardó su **brújula** antes"
        " de cruzar el puente. Caminó entre los árboles observando el mapa."
        " Al mediodía, sacó la **brújula** para confirmar el norte, anotó la"
        " hora en su libreta y descansó junto al lago. Por la tarde, una"
        " neblina cubrió el sendero, así que usó nuevamente su **brújula** y"
        " finalmente llegó al refugio antes de anochecer.» *(Total real: 3"
        " menciones)*"
    )

    c1, c2, c3 = st.columns(3)
    with c1:
      if st.button(
          "🔘 ¡ESCUCHÉ «BRÚJULA»!", type="primary", use_container_width=True
      ):
        st.session_state.conteo_brujula += 1
        registrar_evento(
            "Módulo 1",
            "Detección «brújula»",
            f"Detección #{st.session_state.conteo_brujula}",
            bateria,
        )
    with c2:
      st.metric("Detecciones registradas", st.session_state.conteo_brujula)
    with c3:
      if st.button("Reiniciar contador"):
        st.session_state.conteo_brujula = 0
        st.rerun()

    col_f1, col_f2 = st.columns(2)
    with col_f1:
      etiqueta_ficha_s2 = st.selectbox(
          "Ficha ficticia registrada:", list(FICHAS_OPCIONES.keys())[:3]
      )
      ficha_sel = FICHAS_OPCIONES[etiqueta_ficha_s2]
    with col_f2:
      errores_s2 = st.number_input(
          "Falsas alarmas u omisiones:", min_value=0, step=1
      )

    if st.button("Guardar Misión del Explorador"):
      registrar_evento(
          "Módulo 1",
          "Cierre Misión Explorador",
          (
              f"Aciertos: {st.session_state.conteo_brujula}/3 | Ficha:"
              f" {ficha_sel} | Errores: {errores_s2}"
          ),
          bateria,
      )
      st.success("Resultados de exploración guardados.")

    st.write("")
    mostrar_tarjeta_registro(bateria, ubicacion_key="mision_explorador")

  with tab3:
    st.subheader("Mi Atención en Acción: Matrices de Alternancia")
    st.write(
        "Haz clic en los símbolos que cumplan la regla actual. Al presionar el"
        " botón de señal sonora sonará un tono y cambiará la regla."
    )

    reglas = [
        "Tachar todos los CÍRCULOS AZULES (🔵)",
        "Cambiar regla: Tachar todos los TRIÁNGULOS ROJOS (🔺)",
        "Cambiar regla: Tachar cualquier figura VERDE (🟢 o 🟩)",
        "Cambiar regla: Tachar todos los CUADRADOS (🟥 o 🟩)",
    ]

    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
      st.warning(f"📌 **REGLA ACTIVA:** {st.session_state.matriz_regla}")
    with col_r2:
      if st.button("🔊 Cambiar Regla (Señal Sonora)"):
        otras = [r for r in reglas if r != st.session_state.matriz_regla]
        st.session_state.matriz_regla = random.choice(otras)
        st.session_state.sonar_senal = True
        st.rerun()

    seleccionados = []
    grid = st.columns(6)
    for idx, simbolo in enumerate(st.session_state.matriz_items):
      with grid[idx % 6]:
        if st.checkbox(f"{simbolo}", key=f"mat_{idx}"):
          seleccionados.append(simbolo)

    perseveraciones = st.number_input(
        "Errores por perseveración (siguió con la regla anterior):",
        min_value=0,
        step=1,
    )
    if st.button("Guardar Matriz de Alternancia"):
      registrar_evento(
          "Módulo 1",
          "Matriz de Alternancia",
          (
              f"Marcados: {len(seleccionados)} | Perseveraciones:"
              f" {perseveraciones}"
          ),
          bateria,
      )
      st.success("Desempeño de alternancia registrado.")


# ==========================================
# MÓDULO 2: FATIGA Y AUTORREGULACIÓN
# ==========================================
elif modulo == "2. Fatiga y Autorregulación (S3, S11)":
  tab1, tab2 = st.tabs([
      "🔋 Búsqueda Antes y Después de Pausa (S3)",
      "🧘 Pausa, Pienso y Sigo (S11)",
  ])

  with tab1:
    st.subheader("Comparación de Rendimiento con Pausa Estratégica")
    c_antes, c_despues = st.columns(2)
    with c_antes:
      st.markdown("#### Bloque 1: Antes de la pausa")
      fatiga_antes = st.slider("Fatiga antes de iniciar (0-10)", 0, 10, 5)
      aciertos_antes = st.number_input(
          "Diferencias / aciertos encontrados (Bloque 1):", min_value=0, step=1
      )
      st.info(
          "⏸️ **Pausa programada:** Toma 3 minutos de descanso visual y"
          " respiratorio antes del Bloque 2."
      )

    with c_despues:
      st.markdown("#### Bloque 2: Después de la pausa de 3 min")
      fatiga_despues = st.slider("Fatiga después de la pausa (0-10)", 0, 10, 3)
      aciertos_despues = st.number_input(
          "Diferencias / aciertos encontrados (Bloque 2):", min_value=0, step=1
      )

    senales = st.multiselect(
        "Señales corporales o mentales de fatiga identificadas:",
        [
            "Vista cansada",
            "Lentitud al leer",
            "Irritabilidad",
            "Distracción fácil",
            "Tensión en cuello/hombros",
        ],
    )

    if st.button("Guardar Comparativa de Fatiga"):
      registrar_evento(
          "Módulo 2",
          "Batería Mental y Pausa",
          (
              f"Antes: {aciertos_antes} aciertos (Fatiga {fatiga_antes}) |"
              f" Después: {aciertos_despues} aciertos (Fatiga"
              f" {fatiga_despues}) | Señales: {', '.join(senales)}"
          ),
          bateria,
      )
      st.success("Comparativa guardada.")

  with tab2:
    st.subheader(
        "Autorregulación Emocional: Pausa → Emoción → Prioridad → Respuesta"
    )
    imprevisto = st.selectbox(
        "Situación imprevista simulada:",
        [
            "No encuentro mis llaves o mi libreta al salir",
            "Un familiar me pregunta varias veces si ya tomé mi medicamento",
            "Suena la alarma en medio de una actividad importante",
            "Olvidé anotar un pendiente en mi agenda",
        ],
    )
    col_e1, col_e2 = st.columns(2)
    with col_e1:
      emocion = st.selectbox(
          "1. Emoción detectada (sin juzgar):",
          [
              "Frustración",
              "Estrés / Prisa",
              "Irritabilidad",
              "Inseguridad",
              "Calma",
          ],
      )
      prioridad = st.text_input(
          "2. ¿Cuál es la prioridad en este momento?",
          placeholder="Ej. Mantener la calma y revisar mi registro",
      )
    with col_e2:
      respuesta = st.text_area(
          "3. Respuesta verbal tranquila / asertiva:",
          value="Gracias, dame un momento para comprobarlo en mi registro.",
      )

    if st.button("Guardar Secuencia de Regulación"):
      registrar_evento(
          "Módulo 2",
          "Pausa, Pienso y Sigo",
          (
              f"Situación: {imprevisto} | Emoción: {emocion} | Respuesta:"
              f" {respuesta}"
          ),
          bateria,
      )
      st.success("Secuencia emocional registrada.")


# ==========================================
# MÓDULO 3: MEMORIA DE TRABAJO Y FUNCIONES EJECUTIVAS
# ==========================================
elif modulo == "3. Memoria de Trabajo y Ejecutivas (S4, S5, S6)":
  tab1, tab2, tab3 = st.tabs([
      "🔐 Escape de Instrucciones (S4)",
      "🛒 Memoria de Trabajo y Categorías (S5)",
      "🧩 Soluciono Problemas (S6)",
  ])

  with tab1:
    st.subheader("Escape de Instrucciones Multinivel")
    nivel = st.radio(
        "Nivel de complejidad:",
        ["Nivel 1 (3 pasos)", "Nivel 2 (4 pasos - solo si fatiga es baja)"],
        horizontal=True,
    )

    if nivel == "Nivel 1 (3 pasos)":
      st.info(
          "🗣️ **Consigna:** «1) Toma la tarjeta azul, 2) colócala debajo del"
          " sobre 2 y 3) señala el círculo en la hoja.»"
      )
    else:
      st.info(
          "🗣️ **Consigna:** «1) Abre el sobre 1, 2) saca la ficha verde, 3)"
          " colócala junto al reloj y 4) marca una X en la hoja.»"
      )

    st.write(
        "**Estrategia de agrupación:** *Preparar → Hacer → Revisar*. (Puedes"
        " usar el botón superior de Alarma Ficticia a mitad de la tarea para"
        " evaluar si retoma sin reiniciar)."
    )

    c1, c2 = st.columns(2)
    with c1:
      pasos_ok = st.number_input("Pasos completados correctamente:", 0, 4, 3)
    with c2:
      retomo = st.selectbox(
          "¿Retomó el paso exacto tras interrupción?",
          ["Sí, sin ayuda", "Sí, con pista verbal", "Reinició desde cero"],
      )

    if st.button("Guardar Escape de Instrucciones"):
      registrar_evento(
          "Módulo 3",
          "Escape de Instrucciones",
          f"{nivel} | Pasos correctos: {pasos_ok} | Retoma: {retomo}",
          bateria,
      )
      st.success("Resultado guardado.")

  with tab2:
    st.subheader("Memoria de Trabajo con Información Funcional")
    mostrar_lista = st.checkbox(
        "Mostrar lista de compras desordenada", value=True
    )
    if mostrar_lista:
      st.warning(
          "📝 **Lista:** Manzana • Detergente • Leche • Plátano • Jabón •"
          " Yogurt"
      )
    else:
      st.write("*(Lista oculta para recuerdo)*")

    st.write(
        "Clasifica y escribe de memoria los productos agrupados por categoría:"
    )
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
      frutas = st.text_input("Frutas:")
    with col_m2:
      lacteos = st.text_input("Lácteos:")
    with col_m3:
      limpieza = st.text_input("Artículos de limpieza:")

    tecnica = st.text_input("¿Qué técnica mental usaste para no olvidarlos?")
    if st.button("Guardar Memoria de Trabajo"):
      registrar_evento(
          "Módulo 3",
          "Memoria de Trabajo",
          (
              f"Frutas: {frutas} | Lácteos: {lacteos} | Limpieza: {limpieza} |"
              f" Técnica: {tecnica}"
          ),
          bateria,
      )
      st.success("Ejercicio guardado.")

  with tab3:
    st.subheader("Resolución de Problemas: Detenerme → Analizar → Decidir")
    problema = st.selectbox(
        "Selecciona un problema cotidiano:",
        [
            "Llegas al trabajo y olvidaste llevar un documento importante",
            "Suena tu alarma de medicamento en medio de una reunión importante",
            "Revisas tu pastillero en la noche y notas que solo quedan dosis"
            " para 2 días",
        ],
    )
    p_real = st.text_input("1. ¿Cuál es el problema exacto y su urgencia?")
    alternativas = st.text_area("2. Genera 2 o 3 alternativas de solución:")
    eleccion = st.text_input(
        "3. Mejor alternativa elegida (menor estrés y mayor autonomía):"
    )

    if st.button("Guardar Análisis de Problema"):
      registrar_evento(
          "Módulo 3",
          "Resolución de Problemas",
          f"Caso: {problema} | Decisión: {eleccion}",
          bateria,
      )
      st.success("Análisis guardado.")


# ==========================================
# MÓDULO 4: MEMORIA EPISÓDICA Y COMUNICACIÓN
# ==========================================
elif modulo == "4. Memoria Episódica y Comunicación (S8, S9)":
  tab1, tab2 = st.tabs([
      "📖 Codificación y Recuerdo Episódico (S8)",
      "💬 Comunicación Asertiva (S9)",
  ])

  with tab1:
    st.subheader("Recuerdo de Eventos Relevantes")
    mostrar_texto = st.checkbox("Mostrar historia para codificación", value=True)
    if mostrar_texto:
      st.info(
          "**Historia:** «El **martes a las 10:30 de la mañana**, Carlos fue a"
          " la **farmacia del centro** acompañado de su esposa. Compró una"
          " **libreta azul** para sus registros y luego tomaron café en la"
          " **plaza principal** antes de regresar a casa a la **1:00 PM**.»"
      )
    else:
      st.write("*(Texto oculto — aplica demora de 5 minutos antes de evaluar)*")

    recuerdo_libre = st.text_area(
        "1. Recuerdo libre (narra todo lo que recuerdes sin pistas):"
    )
    st.markdown("#### 2. Recuerdo con claves")
    c_q1, c_q2, c_q3 = st.columns(3)
    with c_q1:
      q1 = st.selectbox(
          "¿Qué día y hora ocurrió?",
          [
              "Selecciona...",
              "Lunes 9:00 AM",
              "Martes 10:30 AM",
              "Jueves 4:00 PM",
          ],
      )
    with c_q2:
      q2 = st.selectbox(
          "¿Qué compró en la farmacia?",
          [
              "Selecciona...",
              "Un reloj",
              "Una libreta azul",
              "Un pastillero rojo",
          ],
      )
    with c_q3:
      q3 = st.selectbox(
          "¿Dónde tomaron café?",
          [
              "Selecciona...",
              "En casa",
              "En la plaza principal",
              "En el hospital",
          ],
      )

    if st.button("Guardar Evaluación Episódica"):
      aciertos_q = sum([
          q1 == "Martes 10:30 AM",
          q2 == "Una libreta azul",
          q3 == "En la plaza principal",
      ])
      registrar_evento(
          "Módulo 4",
          "Memoria Episódica",
          f"Claves correctas: {aciertos_q}/3 | Libre: {recuerdo_libre}",
          bateria,
      )
      st.success("Evaluación episódica guardada.")

  with tab2:
    st.subheader("Constructor de Frases Asertivas")
    st.write("Estructura: **Lo que pasa + Cómo me siento + Lo que propongo**")

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
      parte1 = st.text_input(
          "Lo que pasa:",
          value="Cuando me preguntas varias veces si ya tomé mi pastilla",
      )
    with col_a2:
      parte2 = st.text_input("Cómo me siento:", value="me siento vigilado")
    with col_a3:
      parte3 = st.text_input(
          "Lo que propongo:",
          value="prefiero que revisemos juntos la tarjeta en la noche.",
      )

    frase_final = f"«{parte1}, {parte2}; {parte3}»"
    st.success(f"**Frase armada:** {frase_final}")

    estilo = st.radio(
        "Estilo observado en el ensayo:",
        [
            "Asertivo (calma y claridad)",
            "Pasivo (evita hablar)",
            "Agresivo (molesto)",
        ],
        horizontal=True,
    )

    if st.button("Guardar Práctica de Comunicación"):
      registrar_evento(
          "Módulo 4",
          "Comunicación Asertiva",
          f"Estilo: {estilo} | Frase: {frase_final}",
          bateria,
      )
      st.success("Frase asertiva guardada.")


# ==========================================
# MÓDULO 5: CIRCUITO INTEGRADOR FINAL
# ==========================================
elif modulo == "5. Circuito Integrador Final (S10, S12)":
  st.subheader("🏆 Simulación de Día Completo y Circuito Autónomo")
  st.write(
      "Evalúa la integración de todas las estrategias en 4 momentos clave."
      " Intervén con pista solo si hay bloqueo mayor a 1 minuto."
  )

  m1, m2 = st.columns(2)
  with m1:
    st.markdown("#### 1. Mañana: Planear el día (Agenda + Alarmas)")
    c_m1 = st.checkbox("Organizó cita, pendiente y visita sin encimar horarios")
    pistas_m1 = st.number_input("Pistas requeridas (Mañana):", 0, 5, 0)

    st.markdown("#### 3. Tarde: Manejo de Fatiga (Nivel 7/10)")
    c_m3 = st.checkbox("Identificó señales y pidió descanso de forma asertiva")
    pistas_m3 = st.number_input("Pistas requeridas (Tarde):", 0, 5, 0)

  with m2:
    st.markdown("#### 2. Mediodía: Tarea con Interrupción por Alarma")
    c_m2 = st.checkbox(
        "Completó cadena de adherencia y retomó tarea sin perder datos"
    )
    pistas_m2 = st.number_input("Pistas requeridas (Mediodía):", 0, 5, 0)

    st.markdown("#### 4. Noche: Imprevisto + Kit de Apoyo")
    c_m4 = st.checkbox(
        "Resolvió falta de dosis en pastillero y ubicó elementos de su kit"
    )
    pistas_m4 = st.number_input("Pistas requeridas (Noche):", 0, 5, 0)

  total_pistas = pistas_m1 + pistas_m2 + pistas_m3 + pistas_m4
  logros = sum([c_m1, c_m2, c_m3, c_m4])
  st.metric(
      "Autonomía General",
      f"{logros}/4 momentos logrados",
      f"Total pistas: {total_pistas}",
  )

  if st.button("Guardar Circuito Integrador Final", type="primary"):
    registrar_evento(
        "Módulo 5",
        "Circuito Final Integrado",
        f"Momentos logrados: {logros}/4 | Pistas totales usadas: {total_pistas}",
        bateria,
    )
    st.balloons()
    st.success("¡Circuito final registrado con éxito!")


# ==========================================
# BITÁCORA Y EXPORTACIÓN
# ==========================================
elif modulo == "📊 Bitácora y Descarga de Resultados":
  st.subheader("📊 Registro Clínico y Observaciones de la Sesión")

  if len(st.session_state.registros) == 0:
    st.info("Aún no hay actividades registradas en esta sesión.")
  else:
    df = pd.DataFrame(st.session_state.registros)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️ Descargar Bitácora en Excel / CSV",
        data=csv,
        file_name=f"bitacora_sesion_{datetime.date.today()}.csv",
        mime="text/csv",
        type="primary",
    )