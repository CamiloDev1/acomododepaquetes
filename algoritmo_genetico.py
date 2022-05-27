import re
import random
import matplotlib.pyplot as plt
from numpy import cos
import cv2

class algoritmoGenetico  :
            
    def fn_validar_campos(lista_campos):
        print("\n--------------------------- Validar Campos ---------------------------")
        num_format = re.compile(r'^[1-9][0-9]*$')
        lista_invalidos = list()
        for index in lista_campos:
            print(index)
            if len(index[0]) > 0:
                if re.match(num_format, index[0]):
                    print(f"Dato valido {index}")
                else: 
                    print(f"Dato invalido {index}")
                    lista_invalidos.append(index)
            else:
                print(f"Dato invalido {index}\n")
                lista_invalidos.append(["esta vacio", index[1]])
            
        return lista_invalidos
    
    # 10 mejores por generaciones
    
    def fn_generar_tipos_paquetes():
        print("\n--------------------------- Gnerar Tipos de Paquetes ---------------------------")
        lista_tipo_paquetes = list()
        ''' for x in range(5):
            espacio = random.randint(5, 20)
            costo = random.randint(25, 45)
            # x+1 = tipo de paquete representado en numero; espacio= Espacio que ocupa el paquete; costo: costo del paquete
            lista_tipo_paquetes.append([x+1, espacio, costo]) '''
        # x+1 = tipo de paquete representado en numero; espacio= Espacio que ocupa el paquete; costo: costo del paquete
        lista_tipo_paquetes.append([1, 3, 80, 43])
        lista_tipo_paquetes.append([2, 7, 70, 32])
        lista_tipo_paquetes.append([3, 7, 60, 31])
        lista_tipo_paquetes.append([4, 1, 60, 65])
        lista_tipo_paquetes.append([5, 9, 90, 32])
        return lista_tipo_paquetes
    
    def fn_generar_paquetes(num_paquetes, lista_tipos_paquetes, lista_cantidades_paquetes):
        print("\n--------------------------- Gnerar Paquetes ---------------------------")
        lista_paquetes = list()
        lista_aux = [[10,1], [10,2], [6,3], [7,4], [9,5]]
        #lista_aux = list()
        ''' for x in range(num_paquetes):
            tipo = random.randint(1,3)
            lista_aux.append(tipo)
        lista_aux.sort()
        for ID in range(len(lista_aux)):
            paquete = lista_tipos_paquetes[lista_aux[ID]-1]
            # ID+1 = id del paquete; paquete[0] = tipo de paquete; paquete[1]= Espacio que ocupa el paquete; paquete[2]; costo del paquete
            lista_paquetes.append([ID+1, [paquete[0], paquete[1], paquete[2]]]) '''
        
        
        ID = 1
        for cantidad in lista_cantidades_paquetes:
            for x in range(cantidad[0]):
                paquete = lista_tipos_paquetes[cantidad[1]-1]
                lista_paquetes.append([ID, [paquete[0], paquete[1], paquete[2], paquete[3]]])
                ID += 1
                
        
        print(f"Auxliar: {lista_aux}")    
        print(f"Tipos: {lista_tipos_paquetes}")
        print(f"Paquetes: {lista_paquetes}")
        
        return lista_paquetes
    
    def fn_generar_individuos(longitud_individuo, poblacion_inicial):
        print("\n--------------------------- Gnerar Individuos ---------------------------")
        lista_individuos = list()
        contador = 1
        for individuo in range(poblacion_inicial):
            aux = True
            lista_auxiliar = list()
            while aux :
                numero = random.randint(1, longitud_individuo)
                if (numero in lista_auxiliar) != True:
                    lista_auxiliar.append(numero)
        
                if len(lista_auxiliar) == longitud_individuo:
                    aux = False
            num_individuo ="I" + str(contador)
            lista_individuos.append([num_individuo, lista_auxiliar])
            contador += 1
            
        print(f"Individuos: {lista_individuos}")
        return lista_individuos
    
    def fn_seleccion(individuos):
        print("\n--------------------------- Selección ---------------------------")
        tamaño = len(individuos)
        count = 0
        conta2 = 0
        todosConTodos = list()
        listaAuxiliar = list()
        while count < tamaño:
            for indi in individuos:
                combinacion = individuos[count] + indi
                auxiliar = indi + individuos[count]
                if (conta2 > 0) and (individuos[count] != indi):
                    if (combinacion in listaAuxiliar) != True  : 
                        todosConTodos.append([individuos[count], indi])
                        listaAuxiliar.append(auxiliar)
                        
                elif (conta2 == 0) and (individuos[count] != indi):
                    todosConTodos.append([individuos[count], indi])
                    listaAuxiliar.append(auxiliar)
                    conta2 += 1
            count += 1
        
        print("\nTodos con todos: ")
        for i in todosConTodos:
            print(i)
        return todosConTodos
        # print(f"Individuo: {todosConTodos[0][0][1][7]}")
        
    def fn_comprobar_desendencia(todosConTodos, PD):
        print("\n--------------------------- Comprobar Desendencia ---------------------------")
        lista_desendencia = list()
        for individuo in todosConTodos:
            pd = random.randint(1,100) / 100
            if pd <= PD:
                print(f"Si: inidi: {individuo} | PD: {PD} - pd: {pd}")
                lista_desendencia.append(individuo)
            else:
                print(f"No: inidi: {individuo} | PD: {PD} - pd: {pd}")
        
        return lista_desendencia
    
    def fn_cruza(individuos_desendencia):
        print("\n--------------------------- Cruza ---------------------------")
        lista_cruza = list()
        
        print(f"Lista: {individuos_desendencia}")
        
        for individuo in individuos_desendencia:
            puntos_cortes = list()
            puntos_cortes.append(random.randint(1,len(individuo[0][1])-1))
            puntos_cortes.append(puntos_cortes[0])
            while puntos_cortes[1] == puntos_cortes[0]:
                puntos_cortes[1] = random.randint(1,len(individuo[0][1])-1)
            
            puntos_cortes.sort()
            print(f"Puntos: {puntos_cortes}")
            print(f"Individuo: {individuo}\n")
            # AB1
            izquierda1 = individuo[0][1][0:puntos_cortes[0]]
            derecha1 = individuo[0][1][puntos_cortes[1]:len(individuo[0][1])]
            centro1 = individuo[1][1][puntos_cortes[0]:puntos_cortes[1]]
            cruza1 = izquierda1+centro1+derecha1
            
            #AB2
            izquierda2 = individuo[1][1][0:puntos_cortes[0]]
            derecha2 = individuo[1][1][puntos_cortes[1]:len(individuo[1][1])]
            centro2 = individuo[0][1][puntos_cortes[0]:puntos_cortes[1]]
            cruza2 = izquierda2+centro2+derecha2
            
            print(f"\nCruza 1: {izquierda1}{centro1}{derecha1}")
            print(f"Cruza 2: {izquierda2}{centro2}{derecha2}")
            
            print("-----------------------------------\n")
            lista_cruza.append([cruza1, cruza2])
        return lista_cruza    
        
    def fn_verificar_cadena(lista_individuos):
        print("\n--------------------------- Verificar Cadena ---------------------------")
        print(f"Indis: {lista_individuos}")
        no_repetidos = list()
        
        for indi in lista_individuos:
            lista_sin_repetidos1 = list()
            lista_sin_repetidos2 = list()
            # se elimina el segundo repetido en la cadena del individuo
            for element in range(len(indi[0])):
                if indi[0][element] not in lista_sin_repetidos1:
                    lista_sin_repetidos1.append(indi[0][element])
            
            for element in range(len(indi[1])):
                if indi[1][element] not in lista_sin_repetidos2:
                    lista_sin_repetidos2.append(indi[1][element])
            
            for x in range(len(indi[0])):
                # Se agregan los numeros restantes
                if indi[1][x] not in lista_sin_repetidos1:
                    lista_sin_repetidos1.append(indi[1][x])
                    
                if indi[0][x] not in lista_sin_repetidos2:
                    lista_sin_repetidos2.append(indi[0][x])
            
            no_repetidos.append(lista_sin_repetidos1)
            no_repetidos.append(lista_sin_repetidos2)

            print(f"\nSin repetidos1: {lista_sin_repetidos1}")
            print(f"Sin repetidos2: {lista_sin_repetidos2}")
        
        return no_repetidos
        
    def fn_mutacion(lista_cruzados_sin_repetidos, poblacion_incial, PMI, PMG):
        print("\n--------------------------- Cruza ---------------------------")

        #Aqui se muturan los individuos
        for individuo in lista_cruzados_sin_repetidos:
            pmi_individuo = random.randint(1,100) / 100
            # Se comprueba si el individuo puede mutar
            if pmi_individuo <= PMI:
                print(f"\nEl individuo {individuo} puede mutar | PMI {PMI} | pmi {pmi_individuo}")
                # Aqui se mutan los genes
                for dato in individuo:
                    pmg = random.randint(1, 100) / 100
                    if pmg <= PMG :
                        numero_mutar = dato
                        posicion_mutado = individuo.index(dato)
                        posicion_nueva = posicion_mutado
                        while posicion_nueva == posicion_mutado:
                            posicion_nueva = random.randint(0, len(individuo)-1)
                        numero_mover = individuo[posicion_nueva]
                        
                        print(f"Mutado: {numero_mutar} - Posicion: {posicion_mutado}| Mover: {numero_mover} - Posicion: {posicion_nueva}")
                        
                        individuo[posicion_nueva] = numero_mutar
                        individuo[posicion_mutado] = numero_mover
                        
                        # print(f"\nIndividuo {individuo}")
            else:
                print(f"\nEl individuo {individuo} no puede mutar | PMI {PMI} | pmi {pmi_individuo}")   
        
        print(f"Antes: {lista_cruzados_sin_repetidos}")
        # Aqui se unen la pobalción inicial con los nuevos individuos
        iniciales = list()
        for index in poblacion_incial:
            iniciales.append(index[1])
        lista_cruzados_sin_repetidos = iniciales + lista_cruzados_sin_repetidos
        print(f"\nDepues: {lista_cruzados_sin_repetidos}")
        
        return lista_cruzados_sin_repetidos
    
    def fn_mejor_peor_promedio(lista_individuos, x_posicion):
        print("\n--------------------------- Mejor, peor y promedio ---------------------------")
        
        aux_grafica = list()
        
        mejor = lista_individuos[0][2]
        peor = lista_individuos[-1][2] 
        promedio = 0
        for x in lista_individuos:
            promedio = promedio + x[2]
            
        promedio = promedio / len(lista_individuos)
    
        aux_grafica.append([x_posicion, mejor])
        aux_grafica.append([x_posicion, peor])
        aux_grafica.append([x_posicion, promedio])
        
        print(f"X: {x_posicion}\n")
        
        return aux_grafica
        
    def fn_ganancia_y_ordernar(lista_mutados, lista_paquetes, tamano_contenedor):
        print("\n--------------------------- Obtener ganancia y Ordenar ---------------------------")
        lista_auxiliar = list()
        
        #Se recorre la lsita de individuos
        for individuo in lista_mutados:
            espacio = 0
            costo = 0
            aux_espa = 0
            # Se recorre la lista de tipo de paquetes de cada individuo
            for numero in range(len(individuo)):
                # Se reccore la lista de paquetes
                for tipo in lista_paquetes:
                    # Condición para saber si el tipo id del paquete del individuo es igual id del paquete en la lista de paquetes
                    if individuo[numero] == tipo[0]:
                        # Aqui se suman los espacios que ocupa el tipo de paquete que tiene el individuo
                        espacio = espacio + tipo[1][1]
                        # Condicional para saber si la suma de los espacios de cada paquete del individuo no excede al tamaño del contenedor
                        if espacio <= tamano_contenedor:
                            # aux_espa toma el valor mas grande que la suma de los paquetes del individuo que puede tener sin exceder el tamaño del contenedor
                            aux_espa = espacio
                            # costo toma el valor total de la suma de los costos de cada paquete que al sumar sus espacios no exceden el tamaño del contenedor
                            costo = costo + (tipo[1][2]-tipo[1][3])
                        else:
                            break
            lista_auxiliar.append([individuo, aux_espa, costo])
        print(f"\nAuxiliar: {lista_auxiliar}")
        
        # Se ordena de mejor a peor
        lista_auxiliar.sort(key=lambda costo : costo[2], reverse=True)
        print(f"\nOrdenada: {lista_auxiliar}")
        
        return lista_auxiliar
      
    def fn_graficar(individuos, bandera, generacion, tipo):
        print("\n--------------------------- Graficar ---------------------------")
        contador = 0
        fig = plt.figure(figsize=(12,7))
        fig.tight_layout()
        plt.subplot(1, 1, 1)
        
        x=[]
        y=[]
        
        atributos = [["Mejor", "green"], ["Peor", "orange"], ["Promedio", "blue"]]
            
        while contador < 3 :
            for xy in individuos :
                   # print(f"xy: {xy[0][0]} | {xy[1][0]} | {xy[2][0]}")
                print(f"{atributos[contador][0]}: x: {xy[contador][0]} | y: {xy[contador][1]} ")
                x.append(xy[contador][0])
                y.append(xy[contador][1])
            y.sort()
            plt.plot(x, y, label= atributos[contador][0], color = atributos[contador][1])
            x.clear()
            y.clear()
            contador += 1   
        
        titulo = 'Comportamiento ' #+ str(bandera)
        plt.title(titulo)
        if bandera > 0:
            plt.xlim(-0.5, generacion)
            plt.savefig(f"Image/Imagen#{bandera}.png")
        plt.legend(loc='lower right')
        if bandera == generacion and tipo == 2:
            plt.show()
        else :
            plt.close()
      
    def fn_poda(lista_ordenados, pMaxima):
        print("\n--------------------------- Poda ---------------------------")
        # En dado caso de que la cantidad de indivividuos sea mayor a la poblacion maxima se eliminan los peores y se quedan los mejores
        if len(lista_ordenados) > pMaxima :
            print("Es mayor")
            demas = len(lista_ordenados) - pMaxima
            for x in range(demas) :
                lista_ordenados.pop()
        
        print(f"\nCon poda: {lista_ordenados}")
        
        return lista_ordenados
    
    def fn_generar_video(generacion):
        lista_imagenes = list()
        for imagen in range(2, generacion+1) :
            imagen_nombre = "Image/Imagen#" + str(imagen) + ".png"
            openCv = cv2.imread(imagen_nombre)
            lista_imagenes.append(openCv)
            
        img = lista_imagenes[0]

        
        alto, ancho = img.shape[:2]
        ruta = "Video/Comportamiento.mp4"
        video = cv2.VideoWriter(ruta, cv2.VideoWriter_fourcc(*"mp4v"), 2, (ancho, alto))
        
        for index in lista_imagenes :
            video.write(index)
            
        video.release()