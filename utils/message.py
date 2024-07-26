from colorama import Fore, just_fix_windows_console

just_fix_windows_console()


def page_message(page_number: int, total: int, success: bool) -> str:
    color = Fore.LIGHTGREEN_EX if success else Fore.LIGHTYELLOW_EX

    print(f"   {color}Página {page_number} de {total}{Fore.RESET}")


def message(text: str, type: int = 0, end: str = "\n") -> str:
    color = (
        Fore.LIGHTGREEN_EX
        if type == 1
        else (
            Fore.LIGHTYELLOW_EX
            if type == 2
            else Fore.LIGHTRED_EX if type == 3 else Fore.RESET
        )
    )

    print(f" {color}{text}{Fore.RESET}", end=end)


def success(text: str, end: str = "\n") -> str:
    message(text, 1, end)


def warn(text: str, end: str = "\n") -> str:
    message(text, 2, end)


def error(text: str, end: str = "\n") -> str:
    message(text, 3, end)
