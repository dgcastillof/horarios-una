from flask import Flask, render_template, request
from itertools import product
from flask import jsonify
import os

app = Flask(__name__)

# Obtener el puerto del entorno o usar 5000 como puerto predeterminado
port = int(os.environ.get("PORT", 5000))

# Definir horarios y materias
horarios = {
    'Taller de Narrativa I': {
        'opcion_A': [
            {'dia': 'Martes', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Lunes', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_B': [
            {'dia': 'Martes', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Martes', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_C': [
            {'dia': 'Martes', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Miércoles', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_D': [
            {'dia': 'Martes', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Miércoles', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_E': [
            {'dia': 'Martes', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Jueves', 'hora': '09:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_F': [
            {'dia': 'Martes', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Viernes', 'hora': '09:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_G': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Lunes', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_H': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Martes', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_I': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_J': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_K': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '09:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_L': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Viernes', 'hora': '09:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
    },
    'Taller de Poesía I': {
        'opcion_A': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Martes', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_B': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_C': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '09:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_D': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_E': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Viernes', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_F': [
            {'dia': 'Viernes', 'hora': '09:30-11:30', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Martes', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_G': [
            {'dia': 'Viernes', 'hora': '09:30-11:30', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Miércoles', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_H': [
            {'dia': 'Viernes', 'hora': '09:30-11:30', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Jueves', 'hora': '09:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_I': [
            {'dia': 'Viernes', 'hora': '09:30-11:30', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Jueves', 'hora': '18:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_J': [
            {'dia': 'Viernes', 'hora': '09:30-11:30', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Viernes', 'hora': '14:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
    },
    'Morfología y Sintaxis': {
        'opcion_A': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Martes', 'hora': '14:00-16:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_B': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Martes', 'hora': '16:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_C': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Práctico', 'turnos': ['tarde', 'noche']},
        ],
        'opcion_D': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Miércoles', 'hora': '20:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
        'opcion_E': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Lunes', 'hora': '10:00-12:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_F': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Lunes', 'hora': '12:00-14:00', 'tipo': 'Práctico', 'turnos': ['mañana', 'tarde']},
        ],
    },
    'Teoría y Análisis de las Artes de la Escritura': {
        'opcion_A': [
            {'dia': 'Miércoles', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Miércoles', 'hora': '09:00-11:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_B': [
            {'dia': 'Miércoles', 'hora': '11:00-13:00', 'tipo': 'Teórico', 'turnos': ['mañana']},
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Práctico', 'turnos': ['tarde', 'noche']},
        ],
        'opcion_C': [
            {'dia': 'Miércoles', 'hora': '20:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Miércoles', 'hora': '09:00-11:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_D': [
            {'dia': 'Miércoles', 'hora': '20:00-22:00', 'tipo': 'Teórico', 'turnos': ['noche']},
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Práctico', 'turnos': ['tarde', 'noche']},
        ],
    },
    'Narrativa Argentina I': {
        'opcion_A': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '16:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_B': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Práctico', 'turnos': ['tarde', 'noche']},
        ],
        'opcion_C': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Martes', 'hora': '14:00-16:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_D': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Martes', 'hora': '16:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
    },
    'Narrativa Latinoamericana I': {
        'opcion_A': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '11:00-13:00', 'tipo': 'Práctico', 'turnos': ['mañana']},
        ],
        'opcion_B': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '14:00-16:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_C': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '16:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_D': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Jueves', 'hora': '20:00-22:00', 'tipo': 'Práctico', 'turnos': ['noche']},
        ],
    },
    'Poesía Universal I': {
        'opcion_A': [
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Martes', 'hora': '15:00-17:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_B': [
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Martes', 'hora': '17:00-19:00', 'tipo': 'Práctico', 'turnos': ['tarde', 'noche']},
        ],
        'opcion_C': [
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '14:00-16:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
        'opcion_D': [
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Teórico', 'turnos': ['tarde', 'noche']},
            {'dia': 'Miércoles', 'hora': '16:00-18:00', 'tipo': 'Práctico', 'turnos': ['tarde']},
        ],
    }
}
# Función aux
# iliar para extraer la hora de inicio como un valor numérico
def obtener_hora_inicio(horario):
    hora_inicio_str = horario['hora'].split('-')[0]  # Ejemplo: "11:00"
    hora, minuto = map(int, hora_inicio_str.split(':'))
    return hora * 60 + minuto  # Convertir a minutos para facilitar la comparación

# Función modificada para ordenar primero por día y luego por hora de inicio
def ordenar_horarios(horario):
    orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    dia_orden = orden_dias.index(horario['dia'])
    hora_inicio = obtener_hora_inicio(horario)
    return (dia_orden, hora_inicio)

# Función para comprobar si hay superposición de horarios
def hay_superposicion(horarios):
    for i in range(len(horarios)):
        for j in range(i+1, len(horarios)):
            if horarios[i]['dia'] == horarios[j]['dia']:
                hora_inicio_i = int(horarios[i]['hora'].split('-')[0].replace(':', ''))
                hora_fin_i = int(horarios[i]['hora'].split('-')[1].replace(':', ''))
                hora_inicio_j = int(horarios[j]['hora'].split('-')[0].replace(':', ''))
                hora_fin_j = int(horarios[j]['hora'].split('-')[1].replace(':', ''))
                if (hora_inicio_i < hora_fin_j and hora_fin_i > hora_inicio_j) or \
                   (hora_inicio_j < hora_fin_i and hora_fin_j > hora_inicio_i):
                    return True
    return False


# Función para generar todas las combinaciones posibles
def generar_combinaciones(materias_seleccionadas, horarios, turnos_seleccionados):
    if not materias_seleccionadas:
        return []

    opciones_seleccionadas = []
    for materia in materias_seleccionadas:
        opciones_materia = []
        for opcion in horarios[materia].values():
            opciones_materia.append(opcion)
        opciones_seleccionadas.append(opciones_materia)

    combinaciones = list(product(*opciones_seleccionadas))

    combinaciones_en_lista = []
    for combinacion in combinaciones:
        combinacion_actual = []
        for i, horario in enumerate(combinacion):
            for horario_individual in horario:
                horario_actual = {
                    'dia': horario_individual['dia'],
                    'hora': horario_individual['hora'],
                    'tipo': horario_individual['tipo'],
                    'materia': materias_seleccionadas[i],
                    'turnos': horario_individual['turnos']  # Asegúrate de que esta línea esté presente
                }
                combinacion_actual.append(horario_actual)

        if cumple_horarios_disponibles(combinacion_actual, turnos_seleccionados):
            if not hay_superposicion(combinacion_actual):
                combinacion_actual.sort(key=ordenar_horarios)
                combinaciones_en_lista.append(combinacion_actual)

    return combinaciones_en_lista

def cumple_horarios_disponibles(combinacion, turnos_seleccionados):
    for horario in combinacion:
        # Asegúrate de que 'horario' tenga la clave 'turnos' antes de proceder
        turnos_horario = horario.get('turnos')
        if turnos_horario is None:
            continue  # o manejar de otra manera si no debería suceder
        if not any(turno in turnos_seleccionados for turno in turnos_horario):
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    materias_seleccionadas = []
    if request.method == 'POST':
        materias_seleccionadas = request.form.getlist('materias_seleccionadas')
        combinaciones = generar_combinaciones(materias_seleccionadas, horarios, horarios_disponibles)
        # Pasamos las materias seleccionadas de vuelta a la plantilla para mantener los checkboxes marcados
        return render_template('index.html', materias=horarios.keys(), combinaciones=combinaciones, materias_seleccionadas=materias_seleccionadas)

    return render_template('index.html', materias=horarios.keys(), materias_seleccionadas=materias_seleccionadas)


@app.route('/get_combinaciones', methods=['POST'])
def get_combinaciones():
    data = request.json
    materias_seleccionadas = data.get('materias_seleccionadas', [])
    turnos_seleccionados = data.get('turnos_seleccionados', [])

    # Aquí deberías incluir la lógica para filtrar las materias y horarios basándote en los turnos seleccionados.
    # Por ejemplo, filtrar primero los horarios según los turnos seleccionados antes de generar las combinaciones.

    if not materias_seleccionadas or not turnos_seleccionados:
        mensaje = 'Seleccioná al menos una materia y un turno disponible.'
        combinaciones = []
    else:
        combinaciones = generar_combinaciones(materias_seleccionadas, horarios, turnos_seleccionados)
        if not combinaciones:
            mensaje = 'No hay combinaciones posibles, a menos que consigas un Giratiempo.'
        else:
            mensaje = None

    # Suponiendo que tienes una forma de convertir las combinaciones en HTML o en una estructura que el frontend pueda renderizar.
    # Esto podría involucrar el uso de `render_template` con un template que itere sobre las combinaciones y las muestre.
    # Por simplicidad, aquí asumiremos que puedes generar un HTML o una respuesta directamente.

    return jsonify({'mensaje': mensaje, 'combinaciones': combinaciones})


def filtrar_horarios_por_turno(horarios, turnos_seleccionados):
    horarios_filtrados = {}
    for materia, opciones in horarios.items():
        opciones_filtradas = []
        for opcion in opciones:
            if any(turno in opcion['turnos'] for turno in turnos_seleccionados):
                opciones_filtradas.append(opcion)
        if opciones_filtradas:
            horarios_filtrados[materia] = opciones_filtradas
    return horarios_filtrados

    # Si no hay materias seleccionadas o no hay combinaciones válidas, establecer un mensaje apropiado
    if not materias_seleccionadas:
        mensaje = 'Elige al menos una materia.'
    elif not combinaciones:
        mensaje = 'No hay combinaciones posibles disponibles con los horarios seleccionados.'
    else:
        mensaje = None

    # Renderizar el template con el mensaje o con las combinaciones si existen
    combinaciones_html = render_template('combinaciones.html', combinaciones=combinaciones, mensaje=mensaje)
    return jsonify(combinaciones_html=combinaciones_html)

if __name__ == "__main__":
    # Iniciar la aplicación en el puerto especificado
    app.run(host="0.0.0.0", port=port)