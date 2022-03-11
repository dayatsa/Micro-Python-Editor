import os


class CodeModel:

    def __init__(self, header, code, path_lib):
        self.__header_code = header
        self.__code = code
        self.__filename = None
        self.__path_lib = path_lib


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

    
    # getter full code
    def get_full_code(self):
        data = self.__header_code + "\n\n\n" + self.get_code() + "\n\n\n"
        return data

    
    # getter path main code
    def get_path_main_code(self):
        return os.path.join(self.__path_lib, "main.py")