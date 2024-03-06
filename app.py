from flask import Flask, render_template, request
from itertools import product
from flask import jsonify
import os

app = Flask(__name__)

# Obtener el puerto del entorno o usar 5000 como puerto predeterminado
port = int(os.environ.get("PORT", 5000))

# Definir horarios y materias
import csv



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