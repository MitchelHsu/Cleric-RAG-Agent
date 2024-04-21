from pydantic import BaseModel
from typing import Optional, List


class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: Optional[List[str]]
    status: str


class SubmitQuestionAndDocumentsResponse(BaseModel):
    status: str


class SubmitQuestionAndDocumentRequest(BaseModel):
    question: str
    documents: List[str]
