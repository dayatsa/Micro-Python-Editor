class CodeModel:

    def __init__(self, code):
        self.__code = code
        self.__filename = None


    # setter 
    def set_filename(self, filename):
        self.__filename = filename


    # getter    
    def get_filename(self):
        return self.__filename


    # setter 
    def set_code(self, code):
        self.__code = code
    

    # getter
    def get_code(self):
        return self.__code