from typing import TypedDict, List, Dict, Any

from .connector import connect_with_model
from services.utils import normalize_date, safe_float

class WorkflowState(TypedDict, total=False):
    ocr_pages: List[Dict[str, Any]] 

    extracted_data: Dict[str, Any]
    validated_data: Dict[str, Any]

    final_result: Dict[str, Any]

def extraction_node(state: WorkflowState) -> WorkflowState:
    pages = state["ocr_pages"]

    combined_text = "\n".join(
        page["text"] for page in pages
    ).append("\n Also, provide the data in a structured format as per the MarksheetExtraction schema. and ensure to fill all fields, use null for missing values.")

    structured_model = connect_with_model()
    response = structured_model.invoke(combined_text)

    extracted_data = {
        "candidate_details": response.candidate_details,
        "subjects": response.subjects,
        "overall_result": response.overall_result,
        "issue_details": response.issue_details
    }

    state["extracted_data"] = extracted_data
    return state

def validation_node(state: WorkflowState) -> WorkflowState:
    extracted = state.get("extracted_data", {})

    validated: dict = {}

    candidate_obj = extracted.get("candidate_details", {})
    candidate = candidate_obj.model_dump() if hasattr(candidate_obj, 'model_dump') else candidate_obj

    validated["candidate_details"] = {
        "name": candidate.get("name"),
        "father_or_mother_name": candidate.get("father_or_mother_name"),
        "roll_number": candidate.get("roll_number"),
        "registration_number": candidate.get("registration_number"),
        "exam_year": candidate.get("exam_year"),
        "board_or_university": candidate.get("board_or_university"),
        "institution": candidate.get("institution"),
        "date_of_birth": normalize_date(candidate.get("date_of_birth"))
    }

    validated_subjects = []

    subjects_obj = extracted.get("subjects", [])
    for subject_item in subjects_obj:
        subject = subject_item.model_dump() if hasattr(subject_item, 'model_dump') else subject_item
        subject_name = subject.get("subject_name")
        if not subject_name:
            continue

        max_marks = safe_float(subject.get("max_marks_or_credits"))
        obtained_marks = safe_float(subject.get("obtained_marks_or_credits"))

        if max_marks is not None and obtained_marks is not None:
            if obtained_marks > max_marks:
                obtained_marks = None

        validated_subjects.append({
            "subject_name": subject_name.strip(),
            "max_marks_or_credits": max_marks,
            "obtained_marks_or_credits": obtained_marks,
            "grade": subject.get("grade")
        })

    validated["subjects"] = validated_subjects

    overall_obj = extracted.get("overall_result", {})
    overall = overall_obj.model_dump() if hasattr(overall_obj, 'model_dump') else overall_obj

    validated["overall_result"] = {
        "result_or_division": overall.get("result_or_division"),
        "overall_grade": overall.get("overall_grade")
    }

    issue_obj = extracted.get("issue_details", {})
    issue = issue_obj.model_dump() if hasattr(issue_obj, 'model_dump') else issue_obj

    validated["issue_details"] = {
        "issue_date": normalize_date(issue.get("issue_date")),
        "issue_place": issue.get("issue_place")
    }

    state["validated_data"] = validated
    return state

def confidence_node(state: WorkflowState) -> WorkflowState:
    validated_data = state["validated_data"]

    pages = state["ocr_pages"]
    avg_ocr_conf = sum(p["ocr_confidence"] for p in pages) / len(pages)

    def wrap(value, base_conf=avg_ocr_conf):
        return {
            "value": value,
            "confidence": round(base_conf, 2)
        }

    final_result = {
        "candidate_details": {},
        "subjects": [],
        "overall_result": {},
        "issue_details": {}
    }

    for section, fields in validated_data.items():
        if isinstance(fields, dict):
            final_result[section] = {
                k: wrap(v) for k, v in fields.items()
            }
        elif isinstance(fields, list):
            for item in fields:
                wrapped_item = {
                    k: wrap(v) for k, v in item.items()
                }
                final_result[section].append(wrapped_item)

    state["final_result"] = final_result
    return state
