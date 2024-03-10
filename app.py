from flask import Flask, render_template, request, redirect, url_for
from itertools import product
from flask import jsonify
import os

app = Flask(__name__)

# Obtener el puerto del entorno o usar 5000 como puerto predeterminado
port = int(os.environ.get("PORT", 5000))

# Definir horarios y materias
import csv

materias = [
    {"id": 1, "nombre": "Estado, Sociedad y Universidad", "habilitada": True, "requisitos": {"cursada": [], "aprobada": []}},
    {"id": 2, "nombre": "Taller de Escritura I", "habilitada": True, "requisitos": {"cursada": [], "aprobada": []}},
    {"id": 3, "nombre": "Introducción al Análisis del Discurso", "habilitada": True, "requisitos": {"cursada": [], "aprobada": []}},
    {"id": 4, "nombre": "Herramientas del Lenguaje Verbal", "habilitada": True, "requisitos": {"cursada": [], "aprobada": []}},
    {"id": 5, "nombre": "Taller de Escritura II", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [2]}},
    {"id": 6, "nombre": "Taller de Narrativa I", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 7, "nombre": "Taller de Poesía I", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 8, "nombre": "Teoría y Análisis de las Artes de la Escritura", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 9, "nombre": "Morfología y Sintaxis", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 10, "nombre": "Narrativa Argentina I", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 11, "nombre": "Narrativa Latinoamericana I", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 12, "nombre": "Poesía Universal I", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [1, 2, 3, 4, 5]}},
    {"id": 13, "nombre": "Taller de Crónica", "habilitada": False, "requisitos": {"cursada": [8, 9], "aprobada": [6, 7]}},
    {"id": 14, "nombre": "Taller de Narrativa II", "habilitada": False, "requisitos": {"cursada": [9], "aprobada": [6, 8]}},
    {"id": 15, "nombre": "Poesía Argentina y Latinoamericana I", "habilitada": False, "requisitos": {"cursada": [9], "aprobada": [8]}},
    {"id": 16, "nombre": "Semiótica General", "habilitada": False, "requisitos": {"cursada": [9], "aprobada": [6, 7, 8]}},
    {"id": 17, "nombre": "Taller de Poesía II", "habilitada": False, "requisitos": {"cursada": [9], "aprobada": [6, 8]}},
    {"id": 18, "nombre": "Narrativa Universal I", "habilitada": False, "requisitos": {"cursada": [9], "aprobada": [8, 10, 11]}},
    {"id": 19, "nombre": "Teoría y Análisis de las Artes Dramáticas", "habilitada": False, "requisitos": {"cursada": [16], "aprobada": [10, 11, 12]}},
    {"id": 20, "nombre": "Taller de Semiótica", "habilitada": False, "requisitos": {"cursada": [16], "aprobada": [6, 7]}},
    {"id": 21, "nombre": "Taller de Géneros", "habilitada": False, "requisitos": {"cursada": [14], "aprobada": [6, 7, 10, 11, 12]}},
    {"id": 22, "nombre": "Narrativa Latinoamericana II", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [11]}},
    {"id": 23, "nombre": "Narrativa Argentina II", "habilitada": False, "requisitos": {"cursada": [], "aprobada": [10]}}
]

def cargar_materias():
    # Asegurarse de que todas las materias tengan las claves 'cursada' y 'aprobada'
    for materia in materias:
        materia.setdefault('cursada', False)
        materia.setdefault('aprobada', False)
    return materias

horarios = {}

with open('horarios.csv', newline='', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        curso = row['curso']
        opcion = row['opcion']
        dia = row['dia']
        hora = row['hora']
        tipo = row['tipo']
        if row['turno'] is not None:
            turnos = row['turno'].split(' ')
        else:
            turnos = []

        if curso not in horarios:
            horarios[curso] = {}
        if opcion not in horarios[curso]:
            horarios[curso][opcion] = []

        horarios[curso][opcion].append({'dia': dia, 'hora': hora, 'tipo': tipo, 'turnos': turnos})

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
    print("Generando combinaciones para:", materias_seleccionadas, "con turnos", turnos_seleccionados)
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
                    'turnos': horario_individual['turnos']
                }
                combinacion_actual.append(horario_actual)

        if cumple_horarios_disponibles(combinacion_actual, turnos_seleccionados):
            if not hay_superposicion(combinacion_actual):
                # Ordenar la combinación actual antes de añadirla a la lista final
                combinacion_actual.sort(key=ordenar_horarios)
                print("Combinación sin superposición y cumple turnos:", combinacion_actual)
                combinaciones_en_lista.append(combinacion_actual)  # Añadir la combinación válida ya ordenada
            else:
                print("Combinación descartada por superposición.")
        else:
            print("Combinación no cumple con los turnos disponibles.")

    print("Combinaciones finales generadas:", combinaciones_en_lista)
    return combinaciones_en_lista

@app.route('/correlatividades')
def correlatividades():
    # Aquí deberías cargar o definir las materias y sus estados
    materias = cargar_materias()  # Esta función sería algo que necesitas implementar
    return render_template('correlatividades.html', materias=materias)

@app.route('/actualizar-correlatividades', methods=['POST'])
def actualizar_correlatividades():
    materias = cargar_materias()  # Asumiendo que tienes una función para cargar las materias
    for materia in materias:
        materia_id = str(materia["id"])
        materia["cursada"] = 'cursada_' + materia_id in request.form
        materia["aprobada"] = 'aprobada_' + materia_id in request.form
    # Aquí deberías actualizar el estado de las materias en tu base de datos o estructura de datos

    # Redirigir de nuevo a la página de correlatividades con la información actualizada
    return redirect(url_for('correlatividades'))


def actualizar_estado_materia(materia_id, cursada, aprobada):
    # Encuentra la materia y actualiza su estado
    for materia in materias:
        if materia["id"] == materia_id:
            materia["cursada"] = cursada
            materia["aprobada"] = aprobada
            break  # No necesitas seguir iterando una vez que encuentres la materia

    # Reevaluar las habilitaciones de materias aquí
    for materia in materias:
        # Asegúrate de que cada materia tenga las claves 'cursada' y 'aprobada' inicializadas
        materia.setdefault('cursada', False)
        materia.setdefault('aprobada', False)

        # Comprobar requisitos de aprobación
        requisitos = materia.get('requisitos', {})
        aprobadas_necesarias = requisitos.get('aprobada', [])
        materia['habilitada'] = all(
            any(m.get('aprobada', False) for m in materias if m['id'] == req_id)
            for req_id in aprobadas_necesarias
        ) if aprobadas_necesarias else True  # Si no hay requisitos, la materia está habilitada por defecto

    # Devuelve la lista actualizada de materias para la respuesta de la ruta
    return materias



@app.route('/actualizar-materia', methods=['POST'])
def actualizar_materia():
    data = request.get_json()  # Asegúrate de obtener los datos JSON correctamente
    materia_id = data['materiaId']
    cursada = data['cursada']
    aprobada = data['aprobada']

    # Llama a una función que actualizará el estado de la materia y recalcula las habilitaciones
    materias_actualizadas = actualizar_estado_materia(materia_id, cursada, aprobada)

    # Devuelve la lista completa de materias actualizadas
    return jsonify(materias_actualizadas)



def cumple_horarios_disponibles(combinacion, turnos_seleccionados):
    # Convertir los turnos seleccionados en un conjunto para una búsqueda más eficiente
    turnos_seleccionados_set = set(turnos_seleccionados)

    for horario in combinacion:
        # Convertir el día del horario a minúsculas y quitar acentos si es necesario
        dia_horario = horario['dia'].lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó',
                                                                                                           'o').replace(
            'ú', 'u')

        # Verificar si algún turno del horario está en los turnos seleccionados
        turno_valido = False
        for turno_horario in horario['turnos']:
            # Construir la cadena de día-turno para la verificación
            dia_turno_horario = f"{dia_horario}-{turno_horario}"
            if dia_turno_horario in turnos_seleccionados_set:
                turno_valido = True
                break

        # Si no se encontró un turno válido, la combinación actual no cumple con los requisitos
        if not turno_valido:
            print(f"Combinación descartada: {horario} no cumple con los turnos disponibles.")
            return False

    # Si todas las verificaciones pasan, la combinación es válida
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
    print("Materias seleccionadas:", data.get('materias_seleccionadas'))
    print("Turnos seleccionados:", data.get('turnos_seleccionados'))
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