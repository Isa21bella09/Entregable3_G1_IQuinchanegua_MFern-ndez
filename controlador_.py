from modelo import *
from vista import *
from PyQt5.QtWidgets import QApplication 
import sys 

class Coordinador:    
    def __init__(self, vista, modelo):
        self.__mi_vista= vista
        self.__mi_modelo= modelo
    
    def validarUsuario(self, l,p):
        return self.__mi_modelo.validarUsuario(l,p)

def main():
    app= QApplication(sys.argv)
    mi_vista= IniciarSesion()
    mi_modelo= BaseDatos()    
    coordinador= Coordinador(mi_vista, mi_modelo)
    mi_vista.setControlador(coordinador)
    mi_vista.show()
    sys.exit(app.exec_())

if __name__== "__main__":
    main()