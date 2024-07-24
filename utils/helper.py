import ctypes
import os
import platform
import sys


def set_title(title: str) -> None:
    from models.config import Config

    config = Config()
    ctypes.windll.kernel32.SetConsoleTitleW(f"{config.get_title()}: {title}")


def get_app_directory():
    if getattr(sys, "frozen", False):
        # Se o aplicativo estiver congelado (executado como um executável)
        app_dir = os.path.dirname(sys.executable)
    else:
        # Se o aplicativo estiver sendo executado como um script Python normal
        app_dir = os.path.dirname(os.path.dirname(__file__))
    return app_dir


def exit_application(message=None):
    output_message = "Pressione qualquer tecla para encerrar..."

    if message:
        print(message)

    if debugger_is_active():
        exit()

    print()

    if platform.system() == "Windows":
        os.system(f"pause>nul|set/p ={output_message}")
    else:
        os.system(f"/bin/bash -c 'read -s -n 1 -p \"{output_message}\"'")

    print()
    sys.exit()


def debugger_is_active() -> bool:
    """Retorna verdadeiro se o depurador estiver ativo no momento"""
    return hasattr(sys, "gettrace") and sys.gettrace() is not None
