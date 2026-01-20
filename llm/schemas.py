from typing import List, Optional
from pydantic import BaseModel, Field

class CandidateDetails(BaseModel):
    name: Optional[str] = Field(description="Full name of the candidate")
    father_or_mother_name: Optional[str] = Field(description="Father's or Mother's name")
    roll_number: Optional[str] = Field(description="Roll number of the candidate")
    registration_number: Optional[str] = Field(description="Registration number of the candidate")
    date_of_birth: Optional[str] = Field(description="Date of birth of the candidate")
    exam_year: Optional[str] = Field(description="Year of examination")
    board_or_university: Optional[str] = Field(description="Board or University name")
    institution: Optional[str] = Field(description="School or College name")


class SubjectMarks(BaseModel):
    subject_name: str = Field(description="Name of the subject")
    max_marks_or_credits: Optional[float] = Field(description="Maximum marks or credits")
    obtained_marks_or_credits: Optional[float] = Field(description="Marks or credits obtained by the candidate")
    grade: Optional[str] = Field(description="Grade if mentioned")


class OverallResult(BaseModel):
    result_or_division: Optional[str] = Field(description="Pass/Fail/Division")
    overall_grade: Optional[str] = Field(description="Overall grade if present")


class IssueDetails(BaseModel):
    issue_date: Optional[str] = Field(description="Date of issue of marksheet")
    issue_place: Optional[str] = Field(description="Place of issue of marksheet")


class MarksheetExtraction(BaseModel):
    candidate_details: CandidateDetails
    subjects: List[SubjectMarks]
    overall_result: OverallResult
    issue_details: IssueDetails
