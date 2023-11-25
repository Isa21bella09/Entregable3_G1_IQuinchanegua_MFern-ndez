class BaseDatos:
    def __init__(self):
        self.__usuario = "medicoAnalitico"
        self.__password = "bio12345"
        
    def set_usuario(self, l):
        self.__usuario = l
    
    def set_password(self, p):
        self.__password = p
    
    def validarUsuario(self, l, p):
        return (self.__usuario == l) and (self.__password == p)
