
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from AutomataOp import AutomataOp

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static\Datos'
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    archivos_cargados = request.files.getlist("files[]")
    filenames = []
    print("Archivos cargados",archivos_cargados)
    for file in archivos_cargados:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

    ###############################################################################################
    # Creacion de las estructuras a utilizar
    automata1 = list()
    automata2 = list()

    estados1 = list()
    estados2 = list()

    alfabeto1 = list()
    alfabeto2 = list()

    transiciones1 = dict()
    transiciones2 = dict()

    aceptacion1 = set()
    aceptacion2 = set()

    # Lectura de los datos de los archivos de automatas
    aa1 = open('static/Datos/automata1.txt', mode='r', encoding='utf-8')
    aa2 = open('static/Datos/automata2.txt', mode='r', encoding='utf-8')
    res = open('static/Datos/resultado.txt', mode='w', encoding='utf-8')
    automata_lineas_1 = aa1.readlines()
    automata_lineas_2 = aa2.readlines()

    # Separacion del conjunto de estados
    automata1_estados = automata_lineas_1[0].split()
    for c in automata1_estados:
        estados1.append(c)
    automata1.append(estados1)

    automata2_estados = automata_lineas_2[0].split()
    for c in automata2_estados:
        estados2.append(c)
    automata2.append(estados2)

    # Separacion del alfabeto de simbolos
    automata1_alfabeto = automata_lineas_1[1].split()
    for c in automata1_alfabeto:
        alfabeto1.append(c)
    automata1.append(alfabeto1)

    automata2_alfabeto = automata_lineas_2[1].split()
    for c in automata2_alfabeto:
        alfabeto2.append(c)
    automata2.append(alfabeto2)

    # Separacion de las transiciones
    i = 0
    for t in range(2, len(automata_lineas_1) - 1):
        transiciones1.update({estados1[i]: automata_lineas_1[t].split()})
        i += 1
    for estado in estados1:
        if estado not in transiciones1.keys():
            transicion = []
            transiciones1.update({estado: transicion})
    automata1.append(transiciones1)

    i = 0
    for t in range(2, len(automata_lineas_2) - 1):
        transiciones2.update({estados2[i]: automata_lineas_2[t].split()})
        i += 1
    for estado in estados2:
        if estado not in transiciones2.keys():
            transicion = []
            transiciones2.update({estado: transicion})
    automata2.append(transiciones2)

    # Separacion de estados de aceptacion
    automata_aceptacion1 = automata_lineas_1[len(automata_lineas_1) - 1].split()
    for c in automata_aceptacion1:
        aceptacion1.add(c)
    automata1.append(aceptacion1)

    automata_aceptacion2 = automata_lineas_2[len(automata_lineas_2) - 1].split()
    for c in automata_aceptacion2:
        aceptacion2.add(c)
    automata2.append(aceptacion2)

    # Creacion del objeto automata
    automata = AutomataOp()

    print("Automatas leidos del archivo")
    print("Automata 1:", automata_lineas_1)
    print("Automata 2:", automata_lineas_2)

    print("Automatas originales")
    print("Automata 1:", automata1)
    print("Automata 2:", automata2)

    res.write("Automatas leidos del archivo\n")
    res.write("Automata 1:\n\n")
    for linea in automata_lineas_1:
        res.write(linea)

    res.write("\n\nAutomata 2:\n\n")
    for linea in automata_lineas_2:
        res.write(linea)

    res.write("\n\nAutomatas originales\n\n")
    print("\nAutomata 1:\n\n", file=res)
    for linea in automata1:
        print(linea, file=res)
    print("\nAutomata 2:\n\n", file=res)
    for linea in automata2:
        print(linea, file=res)
    #######################################################################################################
    automata1_afd = automata.afn_eAafd(list.copy(automata1), 'K')
    print("La version AFD del automata 1 es:", automata1_afd)
    automata2_afd = automata.afn_eAafd(list.copy(automata2), 'S')
    print("La version AFD del automata 2 es:", automata2_afd)
    automata1_minimizacion = automata.minimizacion(list.copy(automata1_afd), 'k')
    print("La minimizacion del automata 1 es:", automata1_minimizacion)
    automata2_minimizacion = automata.minimizacion(list.copy(automata2_afd), 's')
    print("La minimizacion del automata 2 es:", automata2_minimizacion)
    print("\n\nLa version AFD del automata 1 es:\n\n", file=res)
    for linea in automata1_afd:
        print(linea, file=res)
    print("\n\nLa version AFD del automata 2 es:\n\n", file=res)
    for linea in automata2_afd:
        print(linea, file=res)
    print("\n\nLa minimizacion del automata 1 es:\n\n", file=res)
    for linea in automata1_minimizacion:
        print(linea, file=res)
    print("\n\nLa minimizacion del automata 2 es:\n\n", file=res)
    for linea in automata2_minimizacion:
        print(linea, file=res)
    #######################################################################################################
    print()
    automata_complemento1 = automata.complemento(list.copy(automata1_minimizacion))
    print("El complemento del automata 1 es:", automata_complemento1)
    automata_complemento2 = automata.complemento(list.copy(automata2_minimizacion))
    print("El complemento del automata 2 es:", automata_complemento2)
    automata_complemento1_afd = automata.afn_eAafd(list.copy(automata_complemento1), 'K')
    print("La version AFD del automata complemento 1 es:", automata_complemento1_afd)
    automata_complemento2_afd = automata.afn_eAafd(list.copy(automata_complemento2), 'S')
    print("La version AFD del automata complemento 2 es:", automata_complemento2_afd)
    automata_complemento1_minimo = automata.minimizacion(list.copy(automata_complemento1_afd), 'k')
    print("La version minimizada del automata complemento 1 es:", automata_complemento1_minimo)
    automata_complemento2_minimo = automata.minimizacion(list.copy(automata_complemento2_afd), 's')
    print("La version minimizada del automata complemento 2 es:", automata_complemento2_minimo)
    print("\n\nEl complemento del automata 1 es:\n\n", file=res)
    for linea in automata_complemento1:
        print(linea, file=res)
    print("\n\nEl complemento del automata 2 es:\n\n", file=res)
    for linea in automata_complemento2:
        print(linea, file=res)
    print("\n\nLa version AFD del automata complemento 1 es:\n\n", file=res)
    for linea in automata_complemento1_afd:
        print(linea, file=res)
    print("\n\nLa version AFD del automata complemento 2 es:\n\n", file=res)
    for linea in automata_complemento2_afd:
        print(linea, file=res)
    print("\n\nLa version minimizada del automata complemento 1 es:\n\n", file=res)
    for linea in automata_complemento1_minimo:
        print(linea, file=res)
    print("\n\nLa version minimizada del automata complemento 2 es:\n\n", file=res)
    for linea in automata_complemento2_minimo:
        print(linea, file=res)
    #######################################################################################################
    print()
    automata_union = automata.union(list.copy(automata1_minimizacion), list.copy(automata2_minimizacion))
    print("La union de ambos automatas es:", automata_union)
    automata_union_afd = automata.afn_eAafd(list.copy(automata_union), 'K')
    print("La version AFD del automata union es:", automata_union_afd)
    automata_union_minimo = automata.minimizacion(list.copy(automata_union_afd), 'k')
    print("La version minimizada del automata union es:", automata_union_minimo)
    print("\n\nLa union de ambos automatas es:", file=res)
    for linea in automata_union:
        print(linea, file=res)
    print("\n\nLa version AFD del automata union es:", file=res)
    for linea in automata_union_afd:
        print(linea, file=res)
    print("\n\nLa version minimizada del automata union es:", file=res)
    for linea in automata_union_minimo:
        print(linea, file=res)
    #######################################################################################################
    print()
    automata_interseccion = automata.interseccion(list.copy(automata1_minimizacion), list.copy(automata2_minimizacion))
    print("La interseccion de ambos automatas es:", automata_interseccion)
    automata_interseccion_afd = automata.afn_eAafd(list.copy(automata_interseccion), 'K')
    print("La version AFD del automata interseccion es:", automata_interseccion_afd)
    automata_interseccion_minimo = automata.minimizacion(list.copy(automata_interseccion_afd), 'k')
    print("La version minimizada del automata interseccion es:", automata_interseccion_minimo)
    print("\n\nLa interseccion de ambos automatas es:\n\n", file=res)
    for linea in automata_interseccion:
        print(linea, file=res)
    print("\n\nLa version AFD del automata interseccion es:\n\n", file=res)
    for linea in automata_interseccion_afd:
        print(linea, file=res)
    print("\n\nLa version minimizada del automata interseccion es:\n\n", file=res)
    for linea in automata_interseccion_minimo:
        print(linea, file=res)
    #######################################################################################################
    print()
    automata_concatenacion = automata.concatenacion(list.copy(automata1_minimizacion),
                                                    list.copy(automata2_minimizacion))
    print("La concatenacion de ambos automatas es:", automata_concatenacion)
    automata_concatenacion_afd = automata.afn_eAafd(list.copy(automata_concatenacion), 'K')
    print("La version AFD del automata concatenacion es:", automata_concatenacion_afd)
    automata_concatenacion_minimo = automata.minimizacion(list.copy(automata_concatenacion_afd), 'k')
    print("La version minimizada del automata concatenacion es:", automata_concatenacion_minimo)
    print("\n\nLa concatenacion de ambos automatas es:\n\n", file=res)
    for linea in automata_concatenacion:
        print(linea, file=res)
    print("\n\nLa version AFD del automata concatenacion es:\n\n", file=res)
    for linea in automata_concatenacion_afd:
        print(linea, file=res)
    print("\n\nLa version minimizada del automata concatenacion es:\n\n", file=res)
    for linea in automata_concatenacion_minimo:
        print(linea, file=res)

    aa1.close()
    aa2.close()
    res.close()

    ###########################################################################################################33

    return render_template('upload.html', filenames=filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/descargar')
def downloaded_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'resultado.txt')

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("80"),
        debug=True
    )
