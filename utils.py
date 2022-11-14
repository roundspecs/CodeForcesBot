from typing import Callable, List


def prompt(messsages: List[str], functions: List[Callable]):
    while True:
        print("Select an option:")
        for i, message in enumerate(messsages, start=1):
            print(f"{i}. {message}")
        answer = input()
        if answer.isdigit():
            answer = int(answer)
            if answer <= len(messsages):
                functions[answer - 1]()
                break
        print(f"'{answer}' is not a valid option. Please try again.")


if __name__ == "__main__":
    prompt(["hello", "hi"], [lambda: print("hello"), lambda: print("hi")])
