from itertools import count
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import win32api,win32con

from algoritmo_genetico import algoritmoGenetico

class controlador(QMainWindow):
    
    TIPOS_PQAQUETES = list()
    CANTIDAD_PAQUETES = list()
    CONTADOR_TIPOS = 1
    CONTADOR_CANTIDAD = 1
    
    def __init__(self) :
        super().__init__()
        uic.loadUi ("Vista/vista_paquetes.ui", self)
        self.btn_calcular.clicked.connect(self.comenzar)
        self.btnTipo.clicked.connect(self.agregar_tipos)
        self.btnCantidades.clicked.connect(self.agregar_cantidades)
    
    def comenzar(self):
        self.btn_calcular.setEnabled(False)
        algoritmo_genetico = algoritmoGenetico
        self.lista_generaciones.clear()
        lista_campos = [
            [self.pIni.text(), "Poblacion inicial"], 
            [self.pMax.text(), "Población maxima"], 
            [self.input_num_paquetes.text(), "Num. de paquetes"], 
            [self.inputPMG.text(), "PMG"], [self.inputPMI.text(), "PMI"], 
            [self.inputPD.text(), "PD"], [self.input_tamano_contenedor.text(), "Tamano de contenedor"]]
        lista_invalidos = algoritmo_genetico.fn_validar_campos(lista_campos)
        if len(lista_invalidos) == 0:
            print("Campos validados")
            lista_individuos_por_generacion = list()
            lista_individuos_grafica = list()
            num_generacion = int (self.generaciones.value())
            for generacion in range(num_generacion):
                gen = generacion + 1
                print(f"\n--------------------------- GENERACION #{gen} ---------------------------")
                num_paquetes = int (self.input_num_paquetes.text())
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
                    print(f"TIPOS: {self.TIPOS_PQAQUETES}")
                    lista_paquetes = algoritmo_genetico.fn_generar_paquetes(num_paquetes, self.TIPOS_PQAQUETES, self.CANTIDAD_PAQUETES)
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
                
                algoritmo_genetico.fn_graficar(lista_individuos_grafica, gen, num_generacion, 1)
            
            t = len(lista_individuos_por_generacion)
            print(f"Cantidad final: {t}")
            
            algoritmo_genetico.fn_generar_video(num_generacion)
            
            print(f"\nGrafica: {lista_individuos_grafica}")
            algoritmo_genetico.fn_graficar(lista_individuos_grafica, num_generacion, num_generacion, 2)
            
            for generacion in range(len(lista_individuos_por_generacion)):
                titulo = "\t\t\t\t                 Generacion #" + str(generacion+1)
                self.lista_generaciones.addItem(titulo)
                self.lista_generaciones.addItem(" ")
                print(f"\nlis: {lista_individuos_por_generacion[generacion]}")
                for individuos in lista_individuos_por_generacion[generacion]:
                    print(f"Individuo: {individuos[0]} | Espacio: {individuos[1]} | Costo: {individuos[2]}")
                    item = f"    Individuo: {individuos[0]}   |   Espacio: {individuos[1]}   |   Ganancia: {individuos[2]}"
                    self.lista_generaciones.addItem(item)
                self.lista_generaciones.addItem(" ")
            
            print(f"\nLista Padres: \n{lista_individuos}")  
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
            self.TIPOS_PQAQUETES.append([self.CONTADOR_TIPOS, tamano, precio, envio])
            texto_tipo = f"Categoría: {self.CONTADOR_TIPOS} | Tamaño: {tamano} | Precio: {precio} | Envio: {envio} "
            self.listaTipos.addItem(texto_tipo)
            self.tamanoPaquete.setText("")
            self.precioPaquete.setText("")
            self.envioPaquete.setText("")
            self.comboBox.addItem(str(self.CONTADOR_TIPOS))
            if self.CONTADOR_TIPOS > 1:
                self.btnCantidades.setEnabled(True)
            
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
            
            self.CONTADOR_CANTIDAD += 1
        else :
            self.mensaje(lista_invalidos)

    def mensaje(self, invalidos):
        print(f"\nAlgunos datos son invalidos:")
        mensaje = "Algunos datos son invalidos:\n\n"
        for dato in invalidos:
            print(f"Campo: {dato[1]} | Dato ingresado: {dato[0]}")
            mensaje = mensaje + f"Campo: {dato[1]} | Dato ingresado: {dato[0]}\n"
        print("\nIngresar solo numeros enteros")
        mensaje = mensaje + "\nIngresar solo numeros enteros"
        win32api.MessageBox(0, mensaje, "ERROR", win32con.MB_ICONERROR)