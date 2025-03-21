# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

import os
import sys
base_path = tmp_global_obj["basepath"] # type: ignore
cur_path = base_path + 'modules' + os.sep + 'SSH' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)


from SSHConnector import SSHConnector # type: ignore

module = GetParams("module") # type: ignore

GetParams = GetParams # type: ignore
SetVar = SetVar # type: ignore
PrintException = PrintException # type: ignore

try:
    if module == "connect_pem":
        # TODO: Implementar la conexión con pem
        pass

    if module == "connect":
        # TODO: Implementar la conexión con credenciales
        pass

    if module == "run":
        # TODO: Implementar la ejecución de comandos
        pass

    if module == "create_folder":
        # TODO: Implementar la creación de carpetas
        pass
    
    if module == "change_directory":
        # TODO: Implementar el cambio de directorio
        pass
    
    if module == "write_in_file":
        # TODO: Implementar la escritura en archivos
        pass
    
    if module == "read_file":
        # TODO: Implementar la lectura de archivos
        pass
    
    if module == "disconnect":
        # TODO: Implementar la desconexión
        pass
except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
    PrintException()
    raise e
