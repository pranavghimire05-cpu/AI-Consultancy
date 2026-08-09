from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.crews.crew import StudyAbroadCrew

router = APIRouter(prefix="/api/v1", tags=["Study Abroad Consultancy"])


class StudyAbroadRequest(BaseModel):
  academic_background: str = Field(..., description="Bachelor's in Computer Science, CGPA: 3.2/4.0")
  test_scores: str = Field(..., description="IELTS: 7.5 overall")
  budget: str = Field(..., description="$25,000 USD per year max")
  field_of_study: str = Field(
      ..., description="Master's in Data Science or Artificial Intelligence"
  )


class StudyAbroadResponse(BaseModel):
  status: str
  consultation_report: str


@router.post("/consult", response_model=StudyAbroadResponse)
def run_study_abroad_consultation(request: StudyAbroadRequest):
  """Triggers the multi-agent study abroad consultancy crew and returns the

  generated roadmap.
  """
  try:
    crew_runner = StudyAbroadCrew()
    result = crew_runner.run(
        academic_background=request.academic_background,
        test_scores=request.test_scores,
        budget=request.budget,
        field_of_study=request.field_of_study,
    )
    return StudyAbroadResponse(
        status="success", consultation_report=str(result)
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
