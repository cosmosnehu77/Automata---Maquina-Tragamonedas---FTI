from automata.fa.dfa import DFA
from graphviz import Digraph
import os
import random

class MaquinaTragamonedasDFA:
    def __init__(self):
        self.__tabla_tambores = {
        'Gris' : {'probabilidad': 0.40, 'multiplicador': 0},
        'Azul' : {'probabilidad': 0.25, 'multiplicador': 4},
        'Rosa' : {'probabilidad': 0.15, 'multiplicador': 10},
        'Morada' : {'probabilidad': 0.10, 'multiplicador': 20},
        'Roja' : {'probabilidad': 0.07, 'multiplicador': 100},
        'Dorada' : {'probabilidad': 0.03, 'multiplicador': 1000}
        }
        self.__automata = DFA(
            states = {'Espera', 'Listo', 'Rodillo1', 'Rodillo2', 'Rodillo3', 'Evaluando', 'Ganaste', 'Perdiste'},
            input_symbols = {'Moneda', 'Giro', 'Detener', 'Evaluar', 'Win', 'Lose'},
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
                    'Evaluar': 'Evaluando',
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
        self.__estado_actual = self.__automata.initial_state
        self.__tambores =[]
        self.__cadena_entradas = []
        os.makedirs('img', exist_ok=True)
    #getters
    @property
    def estado_actual(self):
        return self.__estado_actual
    @property
    def tambores(self):
        return self.__tambores
    @property
    def tabla_tambores(self):
        return self.__tabla_tambores
    @property
    def cadena(self):
        return self.__cadena_entradas
    @property
    def estados_automata(self):
        return self.__automata.states
    #metodos
    def diagramar_estado_actual(self):
        dot = Digraph()
        dot.attr(rankdir='LR')
        for estado in self.__automata.states:
            if estado == self.__estado_actual:
                dot.node(estado, shape='doublecircle', color='green')
            elif estado in self.__automata.final_states:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado, shape='circle')
        for origen, transiciones in self.__automata.transitions.items():
            for simbolo, destino in transiciones.items():
                dot.edge(origen, destino, label=simbolo)
        nro_estado = ['Espera', 'Listo', 'Rodillo1', 'Rodillo2', 'Rodillo3', 'Evaluando', 'Ganaste', 'Perdiste'].index(self.__estado_actual)
        nombre_archivo = f"img/estado_nro{nro_estado}"
        dot.render(nombre_archivo, format='png', cleanup=True)

    def transicionar(self, simbolo):
        if simbolo not in self.__automata.transitions[self.__estado_actual]:
            return False, self.__estado_actual
        self.__cadena_entradas.append(simbolo)
        nuevo_estado = self.__automata.transitions[self.__estado_actual][simbolo]
        self.__estado_actual = nuevo_estado
        #self.diagramar_estado_actual()
        return True, self.__estado_actual
    
    def girar_tambor(self):
        colores = list(self.__tabla_tambores.keys())
        probabilidades = [self.__tabla_tambores[color]['probabilidad'] for color in colores]
        color = random.choices(colores, weights=probabilidades, k=1)[0]
        self.__tambores.append(color)
        return color

    def evaluar_resultado(self, monto):
        a, b, c = self.__tambores
        if a == b == c and a != 'Gris':
            multiplicador = self.__tabla_tambores[a]['multiplicador']
            ganancia = monto * multiplicador
            return 'Win', ganancia
        elif (a == b or b == c or a == c):
            color_repetido = a if (a == b or a == c) else b
            if color_repetido != 'Gris':
                multi_base = self.__tabla_tambores[color_repetido]['multiplicador']
                ganancia = monto * (multi_base // 2)
                return 'Win', ganancia
        elif 'Dorada' in (a, b, c):
            ganancia = monto * 1.5
            return 'Win', ganancia
        return 'Lose', 0

    def reiniciar_maquina(self):
        self.__cadena_entradas = []
        self.__estado_actual = self.__automata.initial_state
        self.__tambores = []
    
    def cadena_aceptada(self):
        return self.__automata.read_input(self.__cadena_entradas)