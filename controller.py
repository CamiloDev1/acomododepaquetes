from itertools import count
from operator import ge
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import win32api,win32con

from algoritmo_genetico import algoritmoGenetico

class controlador(QMainWindow):
    
    TIPOS_PAQUETES = [[1, 3, 50, 36], [2, 9, 100, 32], [3, 1, 90, 85], [4, 3, 60, 38]]
    CANTIDAD_PAQUETES = [[7,1], [9,2], [8,3], [5,4]]
    CONTADOR_TIPOS = 5
    CONTADOR_CANTIDAD = 5
    
    def __init__(self) :
        super().__init__()
        uic.loadUi ("Vista/vista_paquetes.ui", self)
        self.btn_calcular.clicked.connect(self.comenzar)
        self.btnTipo.clicked.connect(self.agregar_tipos)
        self.btnCantidades.clicked.connect(self.agregar_cantidades)
        self.btnLimpiarTipo.clicked.connect(self.limpiar_tipos)
        self.btnLimpiarCantidad.clicked.connect(self.limpiar_cantidad)
    
    def comenzar(self):
        self.btn_calcular.setEnabled(False)
        algoritmo_genetico = algoritmoGenetico
        self.lista_generaciones.clear()
        lista_campos = [
            [self.pIni.text(), "Poblacion inicial"], 
            [self.pMax.text(), "Población maxima"],
            [self.inputPMG.text(), "PMG"], [self.inputPMI.text(), "PMI"], 
            [self.inputPD.text(), "PD"], [self.input_tamano_contenedor.text(), "Tamano de contenedor"]]
        lista_invalidos = algoritmo_genetico.fn_validar_campos(lista_campos)
        if len(lista_invalidos) == 0:
            print("Campos validados")
            win32api.MessageBox(0, "Todo el proceso puede tardar un rato", "Información", win32con.MB_ICONINFORMATION)
            lista_individuos_por_generacion = list()
            lista_individuos_grafica = list()
            num_generacion = int (self.generaciones.value())
            for generacion in range(num_generacion):
                gen = generacion + 1
                print(f"\n--------------------------- GENERACION #{gen} ---------------------------")
                num_paquetes = 0
                poblacion_inicial = int (self.pIni.text())
                pd = int (self.inputPD.text()) / 100
                pmi = int (self.inputPMI.text()) / 100
                pmg = int (self.inputPMG.text()) / 100
                tamano_contenedor = int (self.input_tamano_contenedor.text())
                poblacion_maxima = int (self.pMax.text())
                
                lista_nuevos = list()
                lista_individuos = list()
                if generacion == 0:
                    # lista_tipos_paquetes = algoritmo_genetico.fn_generar_tipos_paquetes()
                    print(f"TIPOS: {self.TIPOS_PAQUETES}")
                    lista_paquetes = algoritmo_genetico.fn_generar_paquetes(num_paquetes, self.TIPOS_PAQUETES, self.CANTIDAD_PAQUETES)
                    num_paquetes = len(lista_paquetes)
                    lista_individuos = algoritmo_genetico.fn_generar_individuos(num_paquetes, poblacion_inicial)
                    # Aqui se hace Seleccion
                    lista_nuevos = algoritmo_genetico.fn_seleccion(lista_individuos)
                    lista_nuevos = algoritmo_genetico.fn_comprobar_desendencia(lista_nuevos, pd)
                else:
                    #auxiliar = list()
                    cont = 1
                    for hijos in lista_individuos_por_generacion[generacion-1]:
                        print(f"Hijos: {hijos}")
                        print("I",str(cont), hijos[0])
                        lista_individuos.append(["I"+str(cont), hijos[0]])
                        cont += 1
                    #lista_individuos = auxiliar
                    lista_nuevos = algoritmo_genetico.fn_seleccion(lista_individuos)
                    #lista_nuevos = auxiliar

                # Aqui se hace cruza de los individuos con desendencia
                lista_cruzados = algoritmo_genetico.fn_cruza(lista_nuevos)
                lista_cruzados_sin_repetidos = algoritmo_genetico.fn_verificar_cadena(lista_cruzados)
                #Aqui se hace la mutación de los individuos
                lista_mutados = algoritmo_genetico.fn_mutacion(lista_cruzados_sin_repetidos, lista_individuos, pmi, pmg)
                #Aqui se obtiene las ganancias y se ordena de mejor a peor
                lista_ordenados = algoritmo_genetico.fn_ganancia_y_ordernar(lista_mutados, lista_paquetes, tamano_contenedor)
                #Aqui se obtienen el mejor, peor y promedio
                lista_individuos_grafica.append(algoritmo_genetico.fn_mejor_peor_promedio(lista_ordenados, generacion))
                # Aqui se hace la poda de los individuos
                individuos_finales = algoritmo_genetico.fn_poda(lista_ordenados, poblacion_maxima)
                ''' print(f"\nLista nuevos: \n{lista_nuevos}")
                print(f"\nLista Cruzados: \n{lista_cruzados}")
                print(f"\nLista Mutados: \n{lista_mutados}") '''
                lista_individuos_por_generacion.append(individuos_finales)
                
                algoritmo_genetico.grafica_seleccion_paquetes(individuos_finales, gen)
            
            algoritmo_genetico.fn_generar_video(num_generacion)
            
            print(f"\nGrafica: {lista_individuos_grafica}")
            algoritmo_genetico.fn_graficar(lista_individuos_grafica, num_generacion)
            
            for generacion in range(len(lista_individuos_por_generacion)):
                titulo = "\t\t\t\t                 Generacion #" + str(generacion+1)
                self.lista_generaciones.addItem(titulo)
                self.lista_generaciones.addItem(" ")
                cont = 1;
                for individuos in lista_individuos_por_generacion[generacion]:
                    # print(f"Individuo: {individuos[0]} | Espacio: {individuos[1]} | Costo: {individuos[2]}")
                    if cont == 1:
                        item = f"Mejor Individuo: {individuos[0]}   |   Espacio: {individuos[1]}   |   Ganancia: {individuos[2]}"
                        cont = 0
                    else:
                        item = f"    Individuo: {individuos[0]}   |   Espacio: {individuos[1]}   |   Ganancia: {individuos[2]}"
                    self.lista_generaciones.addItem(item)
                self.lista_generaciones.addItem(" ")
            
            # print(f"\nLista Padres: \n{lista_individuos}")  
        else:
            self.mensaje(lista_invalidos)
        self.btn_calcular.setEnabled(True) # Se habilita el boton para calcular
        
    def agregar_tipos(self):
        algoritmo_genetico = algoritmoGenetico
        lista_campos = [
            [self.tamanoPaquete.text(), "Tamaño"], 
            [self.precioPaquete.text(), "Precio público"], 
            [self.envioPaquete.text(), "Costo de envio"]
        ]
        lista_invalidos = algoritmo_genetico.fn_validar_campos(lista_campos)
        if len(lista_invalidos) == 0:
            #lista_tipo_paquetes.append([1, 3, 80, 43])
            tamano = int(self.tamanoPaquete.text())
            precio = int(self.precioPaquete.text())
            envio = int(self.envioPaquete.text())
            self.TIPOS_PAQUETES.append([self.CONTADOR_TIPOS, tamano, precio, envio])
            texto_tipo = f"Categoría: {self.CONTADOR_TIPOS} | Tamaño: {tamano} | Precio: {precio} | Envio: {envio} "
            self.listaTipos.addItem(texto_tipo)
            self.tamanoPaquete.setText("")
            self.precioPaquete.setText("")
            self.envioPaquete.setText("")
            self.comboBox.addItem(str(self.CONTADOR_TIPOS))
            if self.CONTADOR_TIPOS > 1:
                self.btnCantidades.setEnabled(True)
            
            self.btnLimpiarTipo.setEnabled(True)
            self.CONTADOR_TIPOS += 1
        else :
            self.mensaje(lista_invalidos)

    def agregar_cantidades(self):
        algoritmo_genetico = algoritmoGenetico
        lista_campos = [
            [self.cantidadAgregar.text(), "Cantidad"]
        ]
        lista_invalidos = algoritmo_genetico.fn_validar_campos(lista_campos)
        if len(lista_invalidos) == 0:
            categoria = int(self.comboBox.currentText())
            cantidad = int(self.cantidadAgregar.text())
            
            self.CANTIDAD_PAQUETES.append([cantidad, categoria])
            texto_agregar = f"Categoría: {categoria} | Cantidad: {cantidad} "
            self.listaAgregados.addItem(texto_agregar)
            self.cantidadAgregar.setText("")
            v = self.comboBox.currentText()
            print(f"Combo: {v}")
            if self.CONTADOR_CANTIDAD > 1:
                self.btn_calcular.setEnabled(True)
            
            self.btnLimpiarCantidad.setEnabled(True)
            
            self.CONTADOR_CANTIDAD += 1
        else :
            self.mensaje(lista_invalidos)

    def limpiar_tipos(self):
        self.TIPOS_PAQUETES.clear()
        self.listaTipos.clear()
        self.listaAgregados.clear()
        self.CANTIDAD_PAQUETES.clear()
        self.comboBox.clear()
        self.btnCantidades.setEnabled(False)
        self.btnLimpiarCantidad.setEnabled(False)
        self.btnLimpiarTipo.setEnabled(False)
        self.btn_calcular.setEnabled(False)
        self.CONTADOR_CANTIDAD = 1
        self.CONTADOR_TIPOS = 1
        
    def limpiar_cantidad(self):
        self.CANTIDAD_PAQUETES.clear()
        self.listaAgregados.clear()
        self.btnLimpiarCantidad.setEnabled(False)
        self.btn_calcular.setEnabled(False)
        self.CONTADOR_CANTIDAD = 1

    def mensaje(self, invalidos):
        print(f"\nAlgunos datos son invalidos:")
        mensaje = "Algunos datos son invalidos:\n\n"
        for dato in invalidos:
            print(f"Campo: {dato[1]} | Dato ingresado: {dato[0]}")
            mensaje = mensaje + f"Campo: {dato[1]} | Dato ingresado: {dato[0]}\n"
        print("\nIngresar solo numeros enteros")
        mensaje = mensaje + "\nIngresar solo numeros enteros"
        win32api.MessageBox(0, mensaje, "ERROR", win32con.MB_ICONERROR)