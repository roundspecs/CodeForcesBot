from constants import ALL_TAGS
from utils import prompt, get_credentials
from selenium import webdriver
from cf_site import create_mashup, generate_problems
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver():
    try:
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    except:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def handle_create_mashup():
    handle, pw = get_credentials()
    print("Enter Mashup Details:")
    name = input("Name of Contest: ")
    duration = input("Duration(in minutes): ")
    driver = get_driver()
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
    print("Enter Mashup Details:")
    contest_url = input("Contest Url: ")
    ratings = [int(x) for x in input("Rating (800-3500) (int) (space separated): ").split()]
    count = int(input("Number of problems to choose (int) : "))
    for i, tag in enumerate(ALL_TAGS, start=1):
        print(f"{i}. {tag}")
    tag_indices = [int(x) for x in input("Tags (int) (space separated): ").split()]
    driver = get_driver()
    generate_problems(
        chrome=driver,
        contest_url=contest_url,
        ratings=ratings,
        count=count,
        tag_indices=tag_indices,
        handle=handle,
        pw=pw,
    )
    input("Press enter to continue")


prompt(
    [
        "Create a Mashup Contest",
        "Generate Problems for a Mashup Contest",
    ],
    [
        handle_create_mashup,
        handle_generate_problems,
    ],
)