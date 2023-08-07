from typing import Optional
import requests
from .models import Problem, RatingChange, Status, Submission, User
from .exceptions import CFStatusFailed

BASE_URL = "https://codeforces.com/api"


def problemset_problems(
    tags: list[str] = [], problemset_name: Optional[str] = None
) -> list[Problem]:
    """Returns all problems from problemset. Problems can be filtered by tags."""
    params = {"tags": ";".join(tags), "problemsetName": problemset_name}
    data = requests.get(
        url=BASE_URL + "/problemset.problems",
        params=params,
    ).json()
    if data["status"] == Status.FAILED.value:
        raise CFStatusFailed(data["comment"])
    return [Problem(**problem) for problem in data["result"]["problems"]]


def problemset_recent_status(count: int) -> list[Submission]:
    """Returns recent submissions."""
    params = {"count": count}
    data = requests.get(
        url=BASE_URL + "/problemset.recentStatus",
        params=params,
    ).json()
    if data["status"] == Status.FAILED.value:
        raise CFStatusFailed(data["comment"])
    return [Submission(**submission) for submission in data["result"]]


def user_info(handles: list[str]) -> list[User]:
    """Returns information about one or several users."""
    params = {"handles": ";".join(handles)}
    data = requests.get(
        url=BASE_URL + "/user.info",
        params=params,
    ).json()
    if data["status"] == Status.FAILED.value:
        raise CFStatusFailed(data["comment"])
    return [User(**user) for user in data["result"]]


def user_rating(handle: str) -> list[RatingChange]:
    """Returns rating history of the specified user."""
    params = {"handle": handle}
    data = requests.get(
        url=BASE_URL + "/user.rating",
        params=params,
    ).json()
    if data["status"] == Status.FAILED.value:
        raise CFStatusFailed(data["comment"])
    return [RatingChange(**rating_change) for rating_change in data["result"]]


def user_status(handle: str, from_: int, count: int):
    """Returns submissions of specified user."""
    params = {"handle": handle, "from": from_, "count": count}
    data = requests.get(
        url=BASE_URL + "/user.status",
        params=params,
    ).json()
    if data["status"] == Status.FAILED.value:
        raise CFStatusFailed(data["comment"])
    return [Submission(**submission) for submission in data["result"]]
