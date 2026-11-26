from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ResearchPlan(BaseModel):
    goal: NonEmptyText
    search_queries: list[NonEmptyText] = Field(min_length=1, max_length=3)

class SourceSelection(BaseModel):
    result_ids: list[int] = Field(max_length=4)


class Evidence(BaseModel):
    source_id: str
    title: str
    url: str
    text: str

class Finding(BaseModel):
    claim: NonEmptyText
    source_ids: list[NonEmptyText] = Field(min_length=1)


class AnswerDraft(BaseModel):
    short_answer: NonEmptyText
    key_findings: list[Finding]
    confidence: Literal["low", "medium", "high"]
    limitations: list[NonEmptyText]
    suggested_next_steps: list[NonEmptyText]


class SourceReference(BaseModel):
    source_id: str
    title: str
    url: str


class ResearchAnswer(AnswerDraft):
    question: NonEmptyText
    sources: list[SourceReference]