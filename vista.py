import pydicom
import os
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QFileDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class GraficarImagen(FigureCanvas):
    def __init__(self, parent, file, path):
        super().__init__(Figure())
        self.setParent(parent)
        self.__axes = self.figure.add_subplot(111)
        self.convertir_imagen(file, path)

    def convertir_imagen(self, img_dicom, path):
        ruta = os.path.join(path, img_dicom)
        imagen_dicom = pydicom.dcmread(ruta)
        self.__axes.imshow(imagen_dicom.pixel_array, cmap='gray')
        self.__axes.axis('off')
        self.draw()

class IniciarSesion(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("iniciar_sesion.ui",self)
        self.setup()

    def setup(self):
        self.buttonBox.accepted.connect(self.aceptar_)
        self.buttonBox.rejected.connect(self.close)
            
    def aceptar_(self):
        usuario= self.usuario_boton.text()
        contrasena= self.contrasena_boton.text()
        validar= self.__coordinador.validarUsuario(usuario,contrasena)
        
        if validar:
            self.ventana_path()
            self.usuario_boton.setText("")
            self.contrasena_boton.setText("")
            
        else:
            mensaje="El usuario y/o la contraseña son incorrectas.\nIntente de nuevo."
            self.advertencia.setText(mensaje)
    
    def setControlador(self,c):
        self.__coordinador= c
    
    def ventana_path(self):
        img = SeleccionarCarpeta(self)
        self.hide()
        img.show()

class SeleccionarCarpeta(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("seleccionar_carpeta.ui",self)
        self.__ventanaPadre = ppal
        self.setup()

    def setup(self):
        self.select_path.clicked.connect(self.ventana_imag)
        self.regresar.clicked.connect(self.salir)
        self.cerrar.clicked.connect(self.close)

    def ventana_imag(self):
        path=QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        archivos = [file for file in os.listdir(path) if file.endswith('.dcm')]
        if not archivos:
            mensaje="La ruta especificada no corresponde a archivos .dcm.\nIntente de nuevo."
            self.advertencia.setText(mensaje)
            
        else:
            img = ImagenDICOM(archivos,path, self.__ventanaPadre)
            self.hide()
            img.show()
    
    def salir(self):
        self.__ventanaPadre.show()
        self.close()

class ImagenDICOM(QDialog):
    def __init__(self, archivos, path, ppal=None):
        super().__init__(ppal)
        loadUi("imagen_dicom.ui", self)
        self.__ventanaPadre = ppal
        self.__files = archivos
        self.__path = path
        self.setup()
        self.valor_act.setText("1")


    def setup(self):
        self.cerrar.clicked.connect(self.close)
        self.vertical_slider.setMinimum(1)
        self.vertical_slider.setMaximum(len(self.__files))
        self.vertical_slider.setValue(1)
        self.vertical_slider.valueChanged.connect(self.actualImagen)
        self.vertical_slider.valueChanged.connect(self.valorSlider)
        self.total_valor.setText(str(len(self.__files)))
        self.salir_.clicked.connect(self.salir)
        layout = QVBoxLayout()
        self.dcm.setLayout(layout)
        self.imagen = GraficarImagen(self.dcm, self.__files[0], self.__path)
        layout.addWidget(self.imagen)
        self.patient_id.setText(self.infoPaciente("PatientID"))
        self.patient_sex.setText(self.infoPaciente("PatientSex"))
        self.patient_w.setText(str(self.infoPaciente("PatientWeight")) + 'Kg')
        self.date_study.setText(str(self.infoPaciente("StudyDate")))
        self.bpart.setText(self.infoPaciente("BodyPartExamined"))
        self.numero_imagen.setPlaceholderText("Número de Imagen")
        self.buscar_imagen.clicked.connect(self.buscarImagen)
        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.numero_imagen)
        layout_1.addWidget(self.buscar_imagen)
        self.dcm.setLayout(layout_1)

    def buscarImagen(self):
        try:
            numero_deseado = int(self.numero_imagen.text())
            if 1 <= numero_deseado <= len(self.__files):
                self.vertical_slider.setValue(numero_deseado)
                self.actualImagen()
            else:
                mensaje="Error. Número de imagen  \nfuera de rango. \nIntente de nuevo."
                self.advertencia.setText(mensaje)       
        except ValueError:
                mensaje="Error. \nIngrese un número válido"
                self.advertencia.setText(mensaje)
            
    def volverlogin(self):
        self.__ventanaPadre.__ventanaPadre.show()
        self.close()

    def valorSlider(self):
        self.valor_act.setText(str(self.vertical_slider.value()))
        
    def actualImagen(self):
        indice = self.vertical_slider.value()
        self.imagen.convertir_imagen(self.__files[indice - 1], self.__path)

    def salir(self):
        self.__ventanaPadre.show()
        self.close()

    def infoPaciente(self,caracteristica):
        indice = self.vertical_slider.value()
        dicom = pydicom.dcmread(os.path.join(self.__path, self.__files[indice-1]))
        return getattr(dicom, caracteristica, "No existe")
        

        
        
        
        
        
