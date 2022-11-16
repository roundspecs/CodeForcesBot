from utils import prompt, get_credentials
from selenium import webdriver
from cf_site import create_mashup, generate_problems


def handle_create_mashup():
    handle, pw = get_credentials()
    print("Mashup Details:")
    name = input("Name: ")
    duration = input("Duration: ")
    driver = webdriver.Chrome()
    create_mashup(
        chrome=driver,
        handle=handle,
        pw=pw,
        name=name,
        duration=duration,
    )
    input("Press enter to continue")


def handle_generate_problems():
    handle, pw = get_credentials()
    print("Mashup Details:")
    contest_url = input("Contest Url: ")
    ratings = [int(x) for x in input("Rating (space separated): ").split()]
    count = int(input("Number of problems to choose: "))
    driver = webdriver.Chrome()
    generate_problems(
        chrome=driver,
        contest_url=contest_url,
        ratings=ratings,
        count=count,
        handle=handle,
        pw=pw,
    )
    input("Press enter to continue")


prompt(
    [
        "Create Mashup",
        "Generate Problems for Mashup",
    ],
    [
        handle_create_mashup,
        handle_generate_problems,
    ],
)

'''
TODO
1. Add discord webhook support
2. Copy link from clipboard
'''
