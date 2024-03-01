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
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico'},
            {'dia': 'Lunes', 'hora': '18:00-22:00', 'tipo': 'Práctico'},
        ],
        'opcion_B': [
            {'dia': 'Martes', 'hora': '18:30-20:30', 'tipo': 'Teórico'},
            {'dia': 'Miércoles', 'hora': '18:00-22:00', 'tipo': 'Práctico'},
        ],
    },
    'Taller de Poesía I': {
        'opcion_A': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico'},
            {'dia': 'Martes', 'hora': '18:00-22:00', 'tipo': 'Práctico'},
        ],
        'opcion_B': [
            {'dia': 'Lunes', 'hora': '18:30-20:30', 'tipo': 'Teórico'},
            {'dia': 'Jueves', 'hora': '18:00-22:00', 'tipo': 'Práctico'},
        ],
    },
    'Morfología y Sintaxis': {
        'opcion_A': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico'},
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Práctico'},
        ],
        'opcion_B': [
            {'dia': 'Viernes', 'hora': '18:00-22:00', 'tipo': 'Teórico'},
            {'dia': 'Miércoles', 'hora': '20:00-22:00', 'tipo': 'Práctico'},
        ],
    },
    'Teoría y Análisis de las Artes de la Escritura': {
        'opcion_A': [
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Teórico'},
            {'dia': 'Miércoles', 'hora': '20:00-22:00', 'tipo': 'Práctico'},
        ],
    },
    'Narrativa Argentina I': {
        'opcion_A': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico'},
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Práctico'},
        ],
    },
    'Narrativa Latinoamericana I': {
        'opcion_A': [
            {'dia': 'Jueves', 'hora': '18:00-20:00', 'tipo': 'Teórico'},
            {'dia': 'Jueves', 'hora': '20:00-22:00', 'tipo': 'Práctico'},
        ],
    },
    'Poesía Universal I': {
        'opcion_A': [
            {'dia': 'Miércoles', 'hora': '18:00-20:00', 'tipo': 'Teórico'},
            {'dia': 'Martes', 'hora': '17:00-19:00', 'tipo': 'Práctico'},
        ],
    },
}
# Función auxiliar para ordenar los días de la semana
def ordenar_dias(horario):
    orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    return orden.index(horario['dia'])

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
def generar_combinaciones(materias_seleccionadas, horarios):
    if not materias_seleccionadas:  # Si no hay materias seleccionadas, devolvemos una lista vacía
        return []

    opciones_seleccionadas = [list(horarios[materia].values()) for materia in materias_seleccionadas]
    combinaciones = list(product(*opciones_seleccionadas))

    # Convertimos las combinaciones en listas para poder iterar en la plantilla
    combinaciones_en_lista = []
    for combinacion in combinaciones:
        # Aplanamos la lista de listas de horarios
        combinacion_actual = [horario for opcion in combinacion for horario in opcion]
        # Añadimos el nombre de la materia a cada horario
        for horario in combinacion_actual:
            horario['materia'] = [materia for materia in materias_seleccionadas if
                                  horario in horarios[materia]['opcion_A'] or horario in horarios[materia].get(
                                      'opcion_B', [])][0]

        # Si no hay superposición, añadimos la combinación a la lista de combinaciones válidas
        if not hay_superposicion(combinacion_actual):
            combinacion_actual.sort(key=ordenar_dias)  # Ordenamos por días de la semana
            combinaciones_en_lista.append(combinacion_actual)

    return combinaciones_en_lista

@app.route('/', methods=['GET', 'POST'])
def index():
    materias_seleccionadas = []
    if request.method == 'POST':
        materias_seleccionadas = request.form.getlist('materias_seleccionadas')
        combinaciones = generar_combinaciones(materias_seleccionadas, horarios)
        # Pasamos las materias seleccionadas de vuelta a la plantilla para mantener los checkboxes marcados
        return render_template('index.html', materias=horarios.keys(), combinaciones=combinaciones, materias_seleccionadas=materias_seleccionadas)

    return render_template('index.html', materias=horarios.keys(), materias_seleccionadas=materias_seleccionadas)


@app.route('/get_combinaciones', methods=['POST'])
def get_combinaciones():
    materias_seleccionadas = request.json['materias_seleccionadas']
    combinaciones = generar_combinaciones(materias_seleccionadas, horarios)

    # Si no hay materias seleccionadas o no hay combinaciones válidas, establecemos un mensaje apropiado
    if not materias_seleccionadas:
        mensaje = 'Elegí al menos una materia.'
    elif not combinaciones:
        mensaje = 'No hay combinaciones posibles, a menos que consigas un Giratiempo.'
    else:
        mensaje = None

    # Renderizamos el template con el mensaje o con las combinaciones si existen
    combinaciones_html = render_template('combinaciones.html', combinaciones=combinaciones, mensaje=mensaje)
    return jsonify(combinaciones_html=combinaciones_html)

if __name__ == "__main__":
    # Iniciar la aplicación en el puerto especificado
    app.run(host="0.0.0.0", port=port)