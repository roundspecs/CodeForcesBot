from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Status(Enum):
    FAILED = "FAILED"
    OK = "OK"


class Type(Enum):
    PROGRAMMING = "PROGRAMMING"
    QUESTION = "QUESTION"


class ParticipantType(Enum):
    CONTESTANT = "CONTESTANT"
    PRACTICE = "PRACTICE"
    VIRTUAL = "VIRTUAL"
    MANAGER = "MANAGER"
    OUT_OF_COMPETITION = "OUT_OF_COMPETITION"


class Verdict(Enum):
    FAILED = "FAILED"
    OK = "OK"
    PARTIAL = "PARTIAL"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    WRONG_ANSWER = "WRONG_ANSWER"
    PRESENTATION_ERROR = "PRESENTATION_ERROR"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    IDLENESS_LIMIT_EXCEEDED = "IDLENESS_LIMIT_EXCEEDED"
    SECURITY_VIOLATED = "SECURITY_VIOLATED"
    CRASHED = "CRASHED"
    INPUT_PREPARATION_CRASHED = "INPUT_PREPARATION_CRASHED"
    CHALLENGED = "CHALLENGED"
    SKIPPED = "SKIPPED"
    TESTING = "TESTING"
    REJECTED = "REJECTED"


class Testset(Enum):
    SAMPLES = "SAMPLES"
    PRETESTS = "PRETESTS"
    TESTS = "TESTS"
    CHALLENGES = "CHALLENGES"
    TESTS1 = "TESTS1"
    TESTS2 = "TESTS2"
    TESTS3 = "TESTS3"
    TESTS4 = "TESTS4"
    TESTS5 = "TESTS5"
    TESTS6 = "TESTS6"
    TESTS7 = "TESTS7"
    TESTS8 = "TESTS8"
    TESTS9 = "TESTS9"
    TESTS10 = "TESTS10"


class User(BaseModel):
    handle: str
    email: Optional[str] = None
    vkId: Optional[str] = None
    openId: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    organization: Optional[str] = None
    contribution: int
    rank: str
    rating: int
    maxRank: str
    maxRating: int
    lastOnlineTimeSeconds: int
    registrationTimeSeconds: int
    friendOfCount: int
    avatar: str
    titlePhoto: str


class RatingChange(BaseModel):
    contestId: int
    contestName: str
    handle: str
    rank: int
    ratingUpdateTimeSeconds: int
    oldRating: int
    newRating: int


class Member(BaseModel):
    handle: str
    name: Optional[str] = None


class Party(BaseModel):
    contestId: Optional[int] = None
    members: list[Member]
    participantType: ParticipantType
    teamId: Optional[int] = None
    teamName: Optional[str] = None
    ghost: bool
    room: Optional[int] = None
    startTimeSeconds: Optional[int] = None


class Problem(BaseModel):
    contestId: Optional[int] = None
    problemsetName: Optional[str] = None
    index: str
    name: str
    type: Optional[Type] = None
    points: Optional[float] = None
    rating: Optional[int] = None
    tags: Optional[list[str]] = []

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Problem):
            raise NotImplemented
        return (
            self.contestId == __value.contestId
            and self.index == __value.index
            and self.name == __value.name
        )

    def __str__(self) -> str:
        return f"{self.contestId}{self.index} {self.name}"

    def __hash__(self) -> int:
        return f"{self.contestId}{self.index}".__hash__()

class Submission(BaseModel):
    id: int
    contestId: Optional[int] = None
    creationTimeSeconds: int
    relativeTimeSeconds: int
    problem: Problem
    author: Party
    programmingLanguage: str
    verdict: Optional[Verdict] = None
    testset: Testset
    passedTestCount: int
    timeConsumedMillis: int
    memoryConsumedBytes: int
    points: Optional[float] = None