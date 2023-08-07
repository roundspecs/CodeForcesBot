import time
import random
from typing import Dict, List, Set
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from codeforces.methods import problemset_problems, user_status
from codeforces.models import Problem
from constants import ALL_TAGS

def generate_problems(
    chrome: Chrome,
    contest_url: str,
    ratings: List[int],
    count: int,
    tag_indices: List[int],
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

    selected_problems = getSelectedProblems(tag_indices, ratings, handles, count)

    # goto problem page
    chrome.get(gym_url + "/problems/new")
    for i, problem in enumerate(selected_problems, start=1):
        problem_input = getElem(
            wait,
            f'//*[@id="pageContent"]/div[2]/div[2]/div[6]/table/tbody/tr[{i}]/td[2]/form/label/input',
        )
        problem_input.send_keys(str(problem.contestId)+problem.index)
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


def getElem(wait: WebDriverWait, xpath: str) -> WebElement:
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def getElemClickable(wait: WebDriverWait, xpath: str):
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def getAttemptedProblems(handles: List[str]):
    attempted: Set[Problem] = set()
    for handle in handles:
        submissions = user_status(handle,1,500)
        for submission in submissions:
            attempted.add(submission.problem)

    print("Attempted Problems: \n" + "\n".join([str(prob) for prob in attempted]))
    return attempted

def getSelectedProblems(tag_indices, ratings, handles, count):
    attempted = getAttemptedProblems(handles)
    tags = [ALL_TAGS[i-1] for i in tag_indices]

    problems = problemset_problems(tags=tags)
    random.shuffle(problems)
    selected: Dict = {}
    count_per_rating, remaining = divmod(count, len(ratings))
    for rating in ratings:
        selected[rating] = {
            "count": count_per_rating,
            "problems": set(),
        }
    for i in range(remaining):
        selected[ratings[i]]["count"] += 1
    for problem in problems:
        if problem.rating == None or problem.rating not in ratings or problem in attempted:
            continue
        if (
            len(selected[problem.rating]["problems"])
            == selected[problem.rating]["count"]
        ):
            continue
        selected[problem.rating]["problems"].add(problem)
        count -= 1
        if count <= 0:
            break
    selected_problems: List[Problem] = []
    for p in selected.values():
        selected_problems.extend(p["problems"])
    print("Selected Problems: \n" + "\n".join([f"{prob.rating} - {prob} - {prob.tags}" for prob in selected_problems]))
    return selected_problems

if __name__ == "__main__":
    # getAttemptedProblems(["benq", "sorcerer_21"])
    getSelectedProblems([4], [800], ["sorcerer_21", "roundspecs", "mahiabdullah", "dev_shajid", "Microboy"], 10)