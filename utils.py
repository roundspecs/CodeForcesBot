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

def get_credentials(filename: str = "credentials.txt"):
    try:
        with open(file=filename) as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Credentials:")
        handle = input("Handle: ")
        pw = input("Password: ")
        with open(file=filename, mode='w') as file:
            file.writelines([handle, '\n', pw])
        return handle, pw

if __name__ == "__main__":
    print(get_credentials())
