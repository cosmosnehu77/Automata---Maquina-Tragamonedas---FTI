from automata.fa.dfa import DFA
from graphviz import Digraph
import random

tabla_tambores = {
    'Gris' : {'probabilidad': 0.40, 'multiplicador': 0},
    'Azul' : {'probabilidad': 0.25, 'multiplicador': 2},
    'Rosa' : {'probabilidad': 0.15, 'multiplicador': 10},
    'Morada' : {'probabilidad': 0.10, 'multiplicador': 20},
    'Roja' : {'probabilidad': 0.07, 'multiplicador': 100},
    'Dorada' : {'probabilidad': 0.03, 'multiplicador': 1000}
}

tragaMonedas = DFA(
    states = {'Espera', 'Listo', 'Rodillo1', 'Rodillo2', 'Rodillo3', 'Evaluando', 'Evaluando', 'Ganaste', 'Perdiste'},
    input_symbols = {'Moneda', 'Giro', 'Detener', 'Win', 'Lose'},
    transitions = {
        'Espera': {
            'Moneda': 'Listo',
        },
        'Listo': {
            'Giro': 'Rodillo1',
        },
        'Rodillo1': {
            'Detener': 'Rodillo2',
        },
        'Rodillo2': {
            'Detener': 'Rodillo3',
        },
        'Rodillo3': {
            'Detener': 'Evaluando',
        },
        'Evaluando': {
            'Win': 'Ganaste',
            'Lose': 'Perdiste',
        },
        'Ganaste': {},
        'Perdiste': {},
    },
    initial_state='Espera',
    final_states={'Ganaste', 'Perdiste'},
    allow_partial=True
)

def diagramar_estado_actual(automata, estado_actual, nombre_archivo):
    dot = Digraph()
    for estado in automata.states:
        if estado == estado_actual:
            dot.node(estado, shape='doublecircle', color='green')
        elif estado in automata.final_states:
            dot.node(estado, shape='doublecircle')
        else:
            dot.node(estado, shape='circle')
    for estado_origen, transiciones in automata.transitions.items():
        for simbolo, estado_destino in transiciones.items():
            dot.edge(estado_origen, estado_destino, label=simbolo)
    dot.render(nombre_archivo, format='png', cleanup=True)

def simulacion_paso(automata, input, estado_actual):
    nuevo_estado = automata.transitions[estado_actual][input]
    print(f"Entrada: {input} | Estado actual: {estado_actual} -> Nuevo estado: {nuevo_estado}")
    diagramar_estado_actual(automata, nuevo_estado, f"estado_{nuevo_estado}")
    return nuevo_estado

def simulacion_tambor():
    colores = list(tabla_tambores.keys())
    probabilidades = [tabla_tambores[color]['probabilidad'] for color in colores]
    return random.choices(colores, weights=probabilidades, k=1)[0]

def evaluar_resultado(tambores, monto):
    a, b, c = tambores
    if a == b == c:
        multiplicador = tabla_tambores[a]['multiplicador']
        ganancia = monto * multiplicador
        return 'Win', ganancia
    elif a == b or b == c or a == c:
        color_repetido = a if (a == b or a == c) else b
        multi_base = tabla_tambores[color_repetido]['multiplicador']
        ganancia = monto * (multi_base // 2)
        return 'Win', ganancia
    elif 'Dorado' in (a, b, c):
        ganancia = monto * 0.5
        return 'Win', ganancia
    else:
        return 'Lose', 0

# def simulacion_completa(automata, inputs):
#     estado = automata.initial_state
#     print(f"Estado inicial: {estado}")

#     for simbolo in inputs:
#         nuevo_estado = automata.transitions[estado][simbolo]
#         print(f"Entrada: {simbolo} | Estado actual: {estado} -> Nuevo estado: {nuevo_estado}")
#         estado = nuevo_estado
#     print (f"Estado final: {estado}")
#     if estado in automata.final_states:
#         print("El autómata ha terminado en un estado final.")

# simulacion_completa(tragaMonedas, ['Moneda', 'Giro', 'Detener', 'Detener', 'Detener', 'Win'])




# tragaMonedas.show_diagram(path="tragaMonedas.png")

# flag = tragaMonedas.accepts_input(['Moneda', 'Giro', 'Detener', 'Detener', 'Detener', 'Win'])
# if flag:
#     print("¡Felicidades! ¡Has ganado en la máquina tragamonedas!")
# else:
#     print("Lo siento, no has ganado esta vez. ¡Inténtalo de nuevo!")
