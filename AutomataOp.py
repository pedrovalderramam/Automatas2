
class AutomataOp:

    #######################################################################################################
    #Complemento

    def complemento(self,automata):

        aut_complemento = list.copy(automata)
        nuevos_finales = set(aut_complemento[0]).difference(aut_complemento[3])
        aut_complemento[3] = nuevos_finales

        return aut_complemento

    #######################################################################################################
    #Union

    def union(self, automata1, automata2):

        automatas_union = list()

        estados_union = list.copy(automata1[0]) + list.copy(automata2[0])
        estados_union.insert(0, 'Q0')
        alfabeto = list(set(list.copy(automata2[1])).union(list.copy(automata1[1])))
        alfabeto.append('e')
        alfabeto_union = alfabeto
        transiciones_union = self.transicionesUnion(list.copy(automata1), list.copy(automata2))
        aceptadores_union = set.union(set.copy(automata1[3]),set.copy(automata2[3]))
        automatas_union.append(estados_union)
        automatas_union.append(alfabeto_union)
        automatas_union.append(transiciones_union)
        automatas_union.append(aceptadores_union)

        return automatas_union

    def transicionesUnion(self, automata1, automata2):

        transiciones1 = dict.copy(automata1[2])
        transiciones2 = dict.copy(automata2[2])
        nueva_transicion = {'Q0': ['e:' + str(automata1[0][0]) + ',' + str(automata2[0][0])]}
        transicion_union = dict(transiciones1, **transiciones2)
        transiciones_union = dict(nueva_transicion, **transicion_union)

        return transiciones_union

    #######################################################################################################
    #Interseccion

    def interseccion(self,automata1,automata2):

        automatas_interseccion = list()

        estados_interseccion = self.estadoCruzados(list.copy(automata1[0]), list.copy(automata2[0]))
        alfabeto_interseccion = list(set(list.copy(automata2[1])).intersection(automata1[1]))
        transiciones_interseccion = self.transicionesEstadosCruzados(dict.copy(automata1[2]), dict.copy(automata2[2]),estados_interseccion,alfabeto_interseccion)
        aceptadores_interseccion = self.aceptadoresEstadosCruzados(set.copy(automata1[3]), set.copy(automata2[3]))
        automatas_interseccion.append(estados_interseccion)
        automatas_interseccion.append(alfabeto_interseccion)
        automatas_interseccion.append(transiciones_interseccion)
        automatas_interseccion.append(aceptadores_interseccion)

        return automatas_interseccion

    def estadoCruzados(self,estados1,estados2):

        return [(e1+'-'+e2)for e1 in estados1 for e2 in estados2]

    def transicionesEstadosCruzados(self,transiciones1,transiciones2,estados_cruzados,alfabeto):

        transiciones_estados_cruzados = dict()

        for estado_compuesto in estados_cruzados:
            transiciones = self.transicionEstadoCompuesto(transiciones1, transiciones2, estado_compuesto,alfabeto)
            transiciones_estados_cruzados.update({estado_compuesto: transiciones})

        return transiciones_estados_cruzados

    def transicionEstadoCompuesto(self,transiciones1,transiciones2,estado_compuesto,alfabeto):

        transiciones = list()
        transiciones_estado1 = dict()
        transiciones_estado2 = dict()

        estados = estado_compuesto.split('-')
        for transicion in transiciones1[estados[0]]:
            transiciones_estado1.update({transicion.split(':')[0]:transicion.split(':')[1]})
        for transicion in transiciones2[estados[1]]:
            transiciones_estado2.update({transicion.split(':')[0]:transicion.split(':')[1]})
        for simbolo in alfabeto:
            transiciones.append(simbolo+':'+transiciones_estado1[simbolo]+ '-' +transiciones_estado2[simbolo] )

        return transiciones

    def aceptadoresEstadosCruzados(self,aceptacion1,aceptacion2):

        return set((a1+'-'+a2)for a1 in aceptacion1 for a2 in aceptacion2)

    #######################################################################################################
    #Concatenacion

    def concatenacion(self,automata1,automata2):

        automatas_concatenacion = list()

        estados_concatenacion = list.copy(automata1[0]) + list.copy(automata2[0])
        alfabeto = list(set(list.copy(automata1[1])).union(list.copy(automata2[1])))
        alfabeto.append('e')
        alfabeto_concatenacion = alfabeto
        transiciones_concatenacion = self.transicionesConcatenacion(automata1, automata2)
        aceptadores_concatenacion = automata2[3]
        automatas_concatenacion.append(estados_concatenacion)
        automatas_concatenacion.append(alfabeto_concatenacion)
        automatas_concatenacion.append(transiciones_concatenacion)
        automatas_concatenacion.append(aceptadores_concatenacion)

        return automatas_concatenacion

    def transicionesConcatenacion(self,automata1,automata2):

        aceptadores_Finales = list()

        transiciones1 = automata1[2]
        transiciones2 = automata2[2]
        aceptadores = list(automata1[3])
        for aceptador in aceptadores:
            if aceptador in automata1[3]:
                aceptadores_Finales.append(aceptador)
        for estadoFinal in aceptadores_Finales:
            lista = transiciones1[estadoFinal]
            lista.append('e:'+ automata2[0][0])
            transiciones1.update({estadoFinal: lista})
        transiciones_concatenacion = dict(transiciones1, **transiciones2)

        return transiciones_concatenacion

    #######################################################################################################
    #No determinista con e a determinista

    def afn_eAafd(self,automata,nombre_estado):
        automata_determinista = list()

        determinista = self.afnAafd(automata,nombre_estado)
        estados_determinista = determinista[0]
        alfabeto_determinista = determinista[1]
        transiciones_determinista = determinista[2]
        aceptadores_determinista = determinista[3]
        automata_determinista.append(estados_determinista)
        automata_determinista.append(alfabeto_determinista)
        automata_determinista.append(transiciones_determinista)
        automata_determinista.append(aceptadores_determinista)

        return automata_determinista

    def afnAafd(self, automata,nombre_estado):

        determinista = list()
        estados_temp = list()
        transiciones_temp = dict()
        pila = list()
        transiciones_simbolo = list()
        aceptadores_temp = list()
        lista_error = list()

        contador = 0
        err = 0
        estados_aceptadores = automata[3]
        alfabeto = automata[1]
        if alfabeto.count('e') > 0:
            alfabeto.remove('e')
        finalizado = 1
        estado_inicial = automata[0][0]
        pila.append(estado_inicial)

        while finalizado != 0:
            estado_actual = pila.pop()
            #print("El estado actual es:",estado_actual)
            nuevos_estados = self.e_cerradura(estado_actual, automata[2])
            #print("La e_cerradura del estado actual es: ",nuevos_estados)
            estados_temp.append(self.formadorNombresOrdenados(nuevos_estados,automata[0]))
            #print("Los estados actuales son: ",estados_temp)
            transiciones_simbolo.clear()
            for simbolo in alfabeto:
                #print("Con el simbolo ", simbolo, " me muevo a ",self.moverListas(nuevos_estados, simbolo, automata[2])
                if len(self.moverListas(nuevos_estados,simbolo,automata[2])) > 0:
                    nombre_futuro = self.e_cerradura(self.moverListas(nuevos_estados, simbolo, automata[2]),automata[2])
                    if self.formadorNombresOrdenados(self.e_cerradura( self.moverListas(nuevos_estados,simbolo,automata[2]),automata[2]),automata[0]) not in estados_temp:
                        #print("Agrego a la pila el estado ",nombre_futuro)
                        pila.append(nombre_futuro)
                    transiciones_simbolo.append(simbolo+':'+self.formadorNombresOrdenados(nombre_futuro,automata[0]))
                else:
                    transiciones_simbolo.append(simbolo + ':E')
                    err = 1
            transiciones_temp.update({self.formadorNombresOrdenados(nuevos_estados,automata[0]): list.copy(transiciones_simbolo)})
            #print("Los nuevos estados son: ",nuevos_estados)
            #print("Los estados aceptadores son: ",estados_aceptadores)
            if len(estados_aceptadores.intersection(nuevos_estados)) > 0:
                aceptadores_temp.append(self.formadorNombresOrdenados(nuevos_estados,automata[0]))
            if len(pila) == 0 or contador > 15:
                finalizado = 0
            #print("La pila queda ",pila)
            contador += 1
        if err == 1:
            for simbolo in alfabeto:
                error = simbolo+':E'
                lista_error.append(error)
            transiciones_temp.update({'E': list.copy(lista_error)})
            estados_temp.append('E')
        #print(estados_temp,"\n",transiciones_temp)
        nuevo_nombre = self.renombrador(estados_temp,transiciones_temp,alfabeto,aceptadores_temp,nombre_estado)
        estados = nuevo_nombre[0]
        transiciones = nuevo_nombre[1]
        aceptadores = nuevo_nombre[2]
        determinista.append(estados)
        determinista.append(alfabeto)
        determinista.append(transiciones)
        determinista.append(aceptadores)

        return determinista

    def e_cerradura(self,estado,transiciones):
        cerradura = set()
        pila = set()

        finalizado = 1
        i = 0
        if isinstance(estado, str):
            estado_lista = [estado]
        else:
            estado_lista = estado
        for e in estado_lista:
            pila.add(e)
        while finalizado != 0:
            estado_actual = pila.pop()
            cerradura.add(estado_actual)
            pila = pila.union(self.mover(estado_actual,'e',transiciones))
            if not pila or i > (len(transiciones)*1000):
                finalizado = 0
            i += 1
        return cerradura

    def moverListas(self,estados,simbolo,transiciones):

        estados_siguientes = set()

        for estado in estados:
            estados_siguientes = estados_siguientes.union(self.mover(estado,simbolo,transiciones))

        return estados_siguientes

    #######################################################################################################
    #Minimizacion

    def minimizacion(self,automata,nombre_estado):

        automata_minimizacion = list()

        conjunto_aceptadores = automata[3]
        conjunto_no_aceptadores = set(automata[0]).difference(automata[3])
        estados = self.Myhill_Nerode(conjunto_aceptadores,conjunto_no_aceptadores,automata)
        minimo = self.formadorAutomata(automata,estados,nombre_estado)
        estados_minimizacion = minimo[0]
        alfabeto_minimizacion = minimo[1]
        transiciones_minimizacion = minimo[2]
        aceptadores_minimizacion = minimo[3]
        automata_minimizacion.append(estados_minimizacion)
        automata_minimizacion.append(alfabeto_minimizacion)
        automata_minimizacion.append(transiciones_minimizacion)
        automata_minimizacion.append(aceptadores_minimizacion)

        return automata_minimizacion

    def Myhill_Nerode(self,aceptadores,no_aceptadores,automata):

        nuevos_estados = list()

        estados = automata[0]
        alfabeto = automata[1]
        transiciones = automata[2]
        #Creacion de la matriz de minimizacion
        an, al = len(automata[0]), len(automata[0])
        matriz_minimizadora = [[0 for x in range(an)] for y in range(al)]
        #Primer llenado de la matriz
        for i in range(0, len(estados)):
            for j in range(0, len(estados)):
                if (estados[i] in aceptadores and estados[j] in no_aceptadores) or (estados[j] in aceptadores and estados[i] in no_aceptadores):
                    matriz_minimizadora[i][j] = 1

        #Segundo llenado de la matriz
        for i in range(0,len(estados)):
            for j in range(0,len(estados)):
                if matriz_minimizadora[i][j] != 1 and self.revisionCruzada(transiciones,i,j,estados,alfabeto,matriz_minimizadora):
                    matriz_minimizadora[i][j] = 1
                    matriz_minimizadora[j][i] = 1

        #Obtencion de los estados semi finales
        for i in range(0,len(estados)):
            for j in range(0,len(estados)):
                if matriz_minimizadora[i][j] == 0 and i != j:
                    matriz_minimizadora[j][i] = 1
                    matriz_minimizadora[i][j] = 1
                    nuevos_estados.append({estados[i], estados[j]})
        estados_minimos_sin_ordenar = self.interseccionEstados(nuevos_estados,estados)
        return estados_minimos_sin_ordenar


    def revisionCruzada(self,transiciones,i,j,estados,alfabeto,matriz):

        estados_siguientes = list()
        revision = False
        z = 0
        for simbolo in alfabeto:
            estados_siguientes.append(list(self.mover(estados[i], simbolo, transiciones)))
            estados_siguientes.append(list(self.mover(estados[j], simbolo, transiciones)))
        for e in estados_siguientes:
            estados_siguientes[z] = e[0]
            z += 1
        z = 0
        for s in range(0,len(alfabeto)):
            if matriz[estados.index(estados_siguientes[z])][estados.index(estados_siguientes[z + 1])] == 1:
                revision = True
            z += 2
        return revision

    def interseccionEstados(self,nuevos_estados,estados_originales):

        estados_interseccion = set()
        estados_a_remover = list()

        for estado in estados_originales:
            estados_interseccion.clear()
            estados_a_remover.clear()
            estados_interseccion.add(estado)
            for es in nuevos_estados:
                if estado in es:
                    estados_interseccion = estados_interseccion.union(set.copy(es))
                    estados_a_remover.append(es)
            nuevos_estados.append(set.copy(estados_interseccion))
            for remover in estados_a_remover:
                if remover in nuevos_estados:
                    nuevos_estados.remove(remover)

        return nuevos_estados

    def formadorAutomata(self,automata,estados,nombre_estado):

        automata_minimo = list()
        aceptadores = list()
        aceptadores_sin_nombre = set()
        estados_sin_nombre = list()

        estados_originales = automata[0]
        alfabeto = automata[1]
        transiciones_originales = automata[2]
        aceptadores_originales = automata[3]
        for aceptador in list(aceptadores_originales):
            for estado in estados:
                if aceptador in estado and estado not in aceptadores:
                    aceptadores.append(estado)
        for estado in estados:
            estados_sin_nombre.append(self.formadorNombresOrdenados(estado,estados_originales))

        for aceptador in aceptadores:
            aceptadores_sin_nombre.add(self.formadorNombresOrdenados(aceptador,estados_originales))
        transiciones_sin_nombre = self.transicionesCompuestasMinimas(transiciones_originales,estados_originales,estados_sin_nombre,alfabeto)
        if self.automataNoValido(alfabeto,transiciones_sin_nombre,estados_sin_nombre):
            nombrado = self.renombrador(estados_originales, transiciones_originales, alfabeto,aceptadores_originales,
                                    nombre_estado)
        else:
            nombrado = self.renombrador(estados_sin_nombre,transiciones_sin_nombre,alfabeto,aceptadores_sin_nombre,nombre_estado)
        automata_minimo.append(nombrado[0])
        automata_minimo.append(alfabeto)
        automata_minimo.append(nombrado[1])
        automata_minimo.append(nombrado[2])

        return automata_minimo

    def automataNoValido(self,alfabeto, transiciones,estados):
        for estado in estados:
            for simbolo in alfabeto:
                if len(self.mover(estado,simbolo,transiciones)) == 0:
                    return True
        return False

    def transicionesCompuestasMinimas(self, transiciones, estados_originales,estados_nuevos, alfabeto):

        transiciones_estados_compuestos = dict()

        for estado_compuesto in estados_nuevos:
            transiciones_estado_compuesto = self.transicionCompuestaMinima(transiciones, estado_compuesto,estados_originales,estados_nuevos, alfabeto)
            transiciones_estados_compuestos.update({estado_compuesto: transiciones_estado_compuesto})

        return transiciones_estados_compuestos

    def transicionCompuestaMinima(self,transiciones,estado,estados_originales,estados_nuevos,alfabeto):

        transiciones_compuestas = list()
        estados_conjunto = set()

        estados = estado.split('.')
        for simbolo in alfabeto:
            estados_conjunto.clear()
            for es in estados:
                siguiente = self.mover(es, simbolo, transiciones)
                estados_conjunto.add(siguiente.pop())
            estado_siguiente = self.formadorNombresOrdenados(estados_conjunto,estados_originales)

            for e in estados_nuevos:
                if set(estado_siguiente.split('.')).issubset(set(e.split('.'))):
                    transiciones_compuestas.append(simbolo+':'+e)

        return transiciones_compuestas


    #######################################################################################################
    #Funciones compartidas


    def renombrador(self,estados,transiciones,alfabeto,aceptadores,nombre):

        estados_renombrados = list()
        transiciones_renombradas = dict()
        estados_viejos_nuevos = dict()
        renombrados = list()
        transiciones_lista = list()
        aceptadores_renombrados = set()

        j = 0
        for es in estados:
            estados_viejos_nuevos.update({es:nombre + str(j)})
            j += 1
        #estados_viejos_nuevos.update({'E': 'E'})
        i = 0
        for e in estados:
            estado = nombre + str(i)
            transiciones_lista.clear()
            for simbolo in alfabeto:
                for simb in transiciones[e]:
                    if simb.split(':')[0] == simbolo:
                        transiciones_lista.append(simbolo+':'+estados_viejos_nuevos[simb.split(':')[1]])
            transiciones_renombradas.update({estado: list.copy(transiciones_lista)})
            estados_renombrados.append(estado)
            i += 1
        for ac in aceptadores:
            aceptadores_renombrados.add(estados_viejos_nuevos[ac])
        renombrados.append(estados_renombrados)
        renombrados.append(transiciones_renombradas)
        renombrados.append(aceptadores_renombrados)

        return renombrados

    def mover(self,estado,simbolo,transiciones):
        estados = set()
        if estado != 'E':
            for transicion in transiciones[estado]:
                if simbolo == transicion.split(':')[0]:
                    if transicion.split(':')[1].split(',') != 'E':
                        estados = set(transicion.split(':')[1].split(','))
        return estados

    def formadorNombresOrdenados(self, conjunto,estados):

        conjunto_indices = list()
        conjunto_ordenado = list()
        if isinstance(conjunto, str):
            conjunto = {conjunto}
        for estado in conjunto:
            conjunto_indices.append(estados.index(estado))
        conjunto_ordenado_indices = sorted(conjunto_indices)
        for indice in conjunto_ordenado_indices:
            conjunto_ordenado.append(estados[indice])
        nombre = ''
        for elemento in conjunto_ordenado:
            nombre = nombre + elemento + '.'

        return nombre[:-1]
