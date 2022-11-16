import time
import requests
from typing import List
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException


def generate_problems(
    chrome: Chrome,
    contest_url: str,
    ratings: List[str],
    count: int,
    handle: str,
    pw: str,
):
    # goto login page
    contest_url = contest_url[22:].replace("/", "%2F")
    chrome.get("https://codeforces.com/enter?back=" + contest_url)

    wait = WebDriverWait(chrome, 10)

    # login
    login(wait, handle=handle, pw=pw)

    # enter cotest
    enter_btn = getElem(
        wait,
        '//*[@id="pageContent"]/div[1]/div[1]/div[1]/div[6]/table/tbody/tr[2]/td[1]/a[1]',
    )
    enter_btn.click()

    # go to invitation page
    while chrome.current_url[23:].split("/")[0] != "gym":
        time.sleep(1)
    gym_url = chrome.current_url
    chrome.get(gym_url + "/invitations?")

    # Collect handles from invitation list
    tbody_element = getElem(
        wait, '//*[@id="pageContent"]/div[3]/div[3]/div[6]/table/tbody'
    )
    a_tags = tbody_element.find_elements(By.CSS_SELECTOR, "td.left > a")
    handles = [a_tag.text for a_tag in a_tags]

    # print invitation list
    print("Invitation List: " + ", ".join(handles))

    # Collect attempted problems
    attempted = set()
    for handle in handles:
        status_url = (
            f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=500"
        )
        res = requests.get(status_url)
        problems = res.json()["result"]
        for problem in problems:
            attempted.add(problemDict2ID(problem["problem"]))

    print("Attempted Problems: " + ", ".join(attempted))
    problems = requests.get("https://codeforces.com/api/problemset.problems").json()[
        "result"
    ]["problems"]
    selected = {}
    count_per_rating, remaining = divmod(count, len(ratings))
    for rating in ratings:
        selected[rating] = {
            "count": count_per_rating,
            "problems": set(),
        }
    for i in range(remaining):
        selected[ratings[i]]["count"] += 1
    for problem in problems:
        problem_id = problemDict2ID(problem)
        if problem_id in attempted:
            continue
        problem_rating = problem.get("rating", False)
        if not problem_rating:
            continue
        if problem_rating not in ratings:
            continue
        if (
            len(selected[problem_rating]["problems"])
            == selected[problem_rating]["count"]
        ):
            continue
        selected[problem_rating]["problems"].add(problem_id)
        count -= 1
        if count <= 0:
            break
    printable_problems = []
    for r, v in selected.items():
        for p in v["problems"]:
            printable_problems.append((p, r))
    print(
        "Selected Problems: ", ", ".join([f"{p}({r})" for p, r in printable_problems])
    )

    # goto problem page
    chrome.get(gym_url + "/problems/new")
    for i, t in enumerate(printable_problems, start=1):
        p = t[0]
        problem_input = getElem(
            wait,
            f'//*[@id="pageContent"]/div[2]/div[2]/div[6]/table/tbody/tr[{i}]/td[2]/form/label/input',
        )
        problem_input.send_keys(p)
        add_btn = getElem(
            wait,
            f'//*[@id="pageContent"]/div[2]/div[2]/div[6]/table/tbody/tr[{i}]/td[1]/a',
        )
        add_btn.click()
    final_add_btn = getElem(wait, '//*[@id="pageContent"]/div[2]/form[2]/input[2]')
    # final_add_btn.click()


def create_mashup(chrome: Chrome, handle: str, pw: str, name: str, duration: str):
    chrome.get("https://codeforces.com/enter?back=%2Fmashup%2Fnew")
    wait = WebDriverWait(chrome, 10)
    login(wait, handle=handle, pw=pw)

    # create mashup
    name_element = getElem(wait, '//*[@id="contestName"]')
    duration_element = getElem(wait, '//*[@id="contestDuration"]')
    create_btn = getElem(wait, '//*[@id="pageContent"]/div/form[2]/input[2]')
    name_element.send_keys(name)
    duration_element.send_keys(duration)
    create_btn.click()

    # goto invitation page
    while not chrome.current_url[-1].isdigit():
        time.sleep(1)
    chrome.get(chrome.current_url + "/invitations?")

    # generate invitation link
    generate_link_btn = getElem(wait, '//*[@id="pageContent"]/div[5]/div[1]/div/a')
    generate_link_btn.click()

    # print generated link
    link_element = getElem(
        wait, '//*[@id="pageContent"]/div[5]/div[2]/div[6]/table/tbody/tr/td[2]/input'
    )
    print("Mashup invitation Link: " + link_element.get_attribute("value"))

    # copy generated link
    copy_btn = getElem(
        wait, '//*[@id="pageContent"]/div[5]/div[2]/div[6]/table/tbody/tr/td[3]/a[1]'
    )
    copy_btn.click()
    print("Link is copied to the clipboard 📋")


def login(wait: WebDriverWait, handle: str, pw: str):
    handle_element = getElem(wait, '//*[@id="handleOrEmail"]')
    pw_element = getElem(wait, '//*[@id="password"]')
    login_btn = getElem(wait, '//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input')
    handle_element.send_keys(handle)
    pw_element.send_keys(pw)
    login_btn.click()
    print("Logging in...")


def problemDict2ID(problem: dict):
    return str(problem.get("contestId")) + str(problem.get("index"))


def getElem(wait: WebDriverWait, xpath: str):
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def getElemClickable(wait: WebDriverWait, xpath: str):
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))