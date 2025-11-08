import streamlit as st
from logica import MaquinaTragamonedasDFA
from pathlib import Path
import random
import time
import os
from PIL import Image
import pandas as pd

st.set_page_config(page_title='Automata Tragamonedas', page_icon='🎰', layout='centered')
#css inyectado
st.markdown("""
    <style>
        /* Centrar todo el contenido */
        .main { text-align: center; }
        div.block-container {
            max-width: 900px;
            padding-top: 2rem;
            text-align: center;
        }

        /* Botones coloridos */
        div.stButton > button {
            width: 100%;
            height: 60px;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(255,255,255,0.4);
        }

        /* Colores de botones */
        div[data-testid="column"]:nth-child(1) button { background-color: #0074D9; }  /* Azul */
        div[data-testid="column"]:nth-child(2) button { background-color: #2ECC40; }  /* Verde */
        div[data-testid="column"]:nth-child(3) button { background-color: #FF851B; }  /* Naranja */
        div[data-testid="column"]:nth-child(4) button { background-color: #FF4136; }  /* Rojo */
        div[data-testid="column"]:nth-child(5) button { background-color: #B10DC9; }  /* Violeta */

        /* Rodillos */
        .rodillo {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            border: 4px solid #444;
            border-radius: 15px;
            padding: 25px;
            width: 180px;
            height: 130px;
            margin: 0 auto;
            color: white;
            text-shadow: 2px 2px 3px black;
        }

        /* Colores según símbolo */
        .Gris { background-color: #555; }
        .Azul { background-color: #0074D9; }
        .Rosa { background-color: #F012BE; }
        .Morada { background-color: #6f42c1; }
        .Roja { background-color: #FF4136; }
        .Dorada { background: linear-gradient(45deg, gold, #ffcc00); color: black; }

        /* Mensajes de saldo */
        .saldo {
            font-size: 1.4rem;
            color: #FFD700;
            text-shadow: 1px 1px 3px black;
        }
    </style>
""", unsafe_allow_html=True)
imagenes = sorted(
    [os.path.join('img', f) for f in os.listdir('img') if f.endswith(".png")],
    key=lambda x: int(x.split("estado_nro")[-1].split(".")[0])
)
if "indice" not in st.session_state:
    st.session_state.indice = 0
if 'maquina' not in st.session_state:
    st.session_state.maquina = MaquinaTragamonedasDFA()
if 'estado_actual' not in st.session_state:
    st.session_state.estado_actual = 'Espera'
if 'tambores' not in st.session_state:
    st.session_state.tambores = ['-', '-', '-']
if 'saldo' not in st.session_state:
    st.session_state.saldo = 1000
if 'monto' not in st.session_state:
    st.session_state.monto = 0
if 'imagen_actual' not in st.session_state:
    st.session_state.imagen_actual = 'img/estado_nro0.png'
if 'girando' not in st.session_state:
    st.session_state.girando = [False, False, False]

df_tabla = pd.DataFrame(st.session_state.maquina.tabla_tambores)

st.title('🎰 Simulador de Máquina Tragamonedas - AFD')
st.markdown('Este simulador demuestra el funcionamiento de un **Automata Finito Determinista (AFD)** aplicado a una máquina tragamonedas.')

st.markdown(f"<p class='saldo'><b>💰 Saldo Disponible:</b> {st.session_state.saldo} créditos</p>", unsafe_allow_html=True)
monto = st.number_input('Ingrese su apuesta:', min_value=0, max_value=int(st.session_state.saldo))

col1, col2, col3, col4, col5 = st.columns(5)

def actualizar_imagen(estado):
    nombres = ['Espera', 'Listo', 'Rodillo1', 'Rodillo2', 'Rodillo3', 'Evaluando', 'Ganaste', 'Perdiste']
    nro_estado = nombres.index(estado)
    img_path = Path(f"img/estado_nro{nro_estado}.png")
    st.session_state.imagen_actual = str(img_path) if img_path.exists() else None

if col1.button('🪙 Insertar Moneda'):
    exito, nuevo_estado = st.session_state.maquina.transicionar('Moneda')
    if exito:
        st.session_state.estado_actual = nuevo_estado
        actualizar_imagen(nuevo_estado)
        st.balloons()
        st.success('💸 Moneda insertada correctamente. ¡Listo para apostar!')
    else:
        st.error('🚫 No se puede insertar moneda en este estado.')

if col2.button('🎡 Girar'):
    if st.session_state.estado_actual != 'Listo':
        st.error('⚠️ No se puede girar aún. Inserta una moneda primero.')
    elif monto <= 0 or monto > st.session_state.saldo:
        st.warning('⚠️ Ingresa una apuesta válida.')
    else:
        exito, nuevo_estado = st.session_state.maquina.transicionar('Giro')
        if exito:
            st.session_state.estado_actual = nuevo_estado
            actualizar_imagen(nuevo_estado)
            st.session_state.tambores = ['-', '-', '-']
            st.session_state.girando = [True, True, True]
            st.toast('🎰 ¡Los tambores están girando!', icon="🎡")

if col3.button('⛔ Detener'):
    if not any(st.session_state.girando):
        st.info('❗ No hay tambores girando.')
    else:
        exito, nuevo_estado = st.session_state.maquina.transicionar('Detener')
        st.session_state.estado_actual = nuevo_estado
        actualizar_imagen(nuevo_estado)
        for i in range(3):
            if st.session_state.girando[i]:
                st.session_state.girando[i] = False
                color = st.session_state.maquina.girar_tambor()
                st.session_state.tambores[i] = color
                st.toast(f'🎨 Rodillo {i+1} detenido en: {color}', icon="✨")
                break

if col4.button('✅ Evaluar'):
    if st.session_state.estado_actual != 'Rodillo3':
        st.warning('⚠️ Detén los tres tambores antes de evaluar.')
    else:
        exito, nuevo_estado = st.session_state.maquina.transicionar('Evaluar')
        st.session_state.estado_actual = nuevo_estado
        actualizar_imagen(nuevo_estado)
        if exito:
            resultado, ganancia = st.session_state.maquina.evaluar_resultado(monto)
            exito, nuevo_estado = st.session_state.maquina.transicionar(resultado)
            if exito:
                st.session_state.estado_actual = nuevo_estado
                actualizar_imagen(nuevo_estado)
                if resultado == 'Win':
                    st.session_state.saldo += ganancia
                    st.success(f'🎉 ¡Ganaste {ganancia} créditos!')
                else:
                    st.session_state.saldo -= monto
                    st.error('💀 Has perdido tu apuesta.')

if col5.button('🔄 Reiniciar'):
    st.session_state.maquina.reiniciar_maquina()
    st.session_state.estado_actual = st.session_state.maquina.estado_actual
    st.session_state.tambores = ['-', '-', '-']
    st.session_state.girando = [False, False, False]
    actualizar_imagen(st.session_state.estado_actual)
    st.toast('🧼 Máquina reiniciada.', icon="🔁")

st.markdown("### 🎠 Rodillos Actuales")
col_a, col_b, col_c = st.columns(3)
placeholders = [col_a.empty(), col_b.empty(), col_c.empty()]
simbolos = ["Gris", "Azul", "Rosa", "Morada", "Roja", "Dorada"]

if any(st.session_state.girando):
    for _ in range(1000):  # velocidad/frames
        for i in range(3):
            if st.session_state.girando[i]:
                st.session_state.tambores[i] = random.choice(simbolos)
            placeholders[i].markdown(
                f"<div class='rodillo {st.session_state.tambores[i]}'>{st.session_state.tambores[i]}</div>",
                unsafe_allow_html=True
            )
        time.sleep(0.1)
else:
    for i in range(3):
        placeholders[i].markdown(
            f"<div class='rodillo {st.session_state.tambores[i]}'>{st.session_state.tambores[i]}</div>",
            unsafe_allow_html=True
        )

st.subheader(f"Estado Actual: `{st.session_state.estado_actual}`")
imagen_actual = Image.open(imagenes[st.session_state.indice])
st.image(imagen_actual, caption=f"Estado {st.session_state.indice}", use_container_width=True)
colu1, colu2, colu3 = st.columns(3)
with colu1:
    if st.button("Anterior", use_container_width=True):
        if st.session_state.indice > 0:
            st.session_state.indice -= 1
with colu3:
    if st.button("Siguiente", use_container_width=True):
        if st.session_state.indice < len(imagenes) - 1:
            st.session_state.indice += 1
st.caption(f"Mostrando diagrama {st.session_state.indice + 1} de {len(imagenes)}")

st.markdown("### 🎯 Tabla de Probabilidades y Multiplicadores")
st.dataframe(
    df_tabla,
    use_container_width=True,
    hide_index=True
)