from typing import Callable, List


def prompt(messsages: List[str], functions: List[Callable]):
    print("Select an option:")
    for i, message in enumerate(messsages, start=1):
        print(f"{i}. {message}")
    functions[i-1]()