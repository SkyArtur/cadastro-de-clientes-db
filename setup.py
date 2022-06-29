import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
base = None
if sys.platform == "win64":
    base = "Win64GUI"

setup(
    name="Cadastro de Clientes",
    version="0.1",
    description="Versão de Cadastro de Cliente com Banco de Dados!",
    options={"build_exe": build_exe_options},
    executables=[Executable("principal.py", base=base)],
)

