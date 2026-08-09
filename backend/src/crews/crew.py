from crewai import Agent, Crew, Process, Task, LLM
from config.config import Settings
from src.prompts import AdvisorPrompts, EvaluatorPrompts, MatcherPrompts


class StudyAbroadCrew:

  def __init__(self):
    Settings.validate()
    
    # Initialize CrewAI's native LLM wrapper with the mistral provider prefix
    self.llm = LLM(
        model=f"mistral/{Settings.MODEL_NAME}",  # e.g., "mistral/mistral-medium"
        temperature=Settings.TEMPERATURE,
        api_key=Settings.API_KEY,
    )

  def assemble_crew(self) -> Crew:
    evaluator = Agent(
        role="Student Profile & Eligibility Evaluator",
        goal=(
            "Analyze student academic background, test scores, and budget to"
            " determine optimal study destinations and visa feasibility."
        ),
        backstory=EvaluatorPrompts.BACKSTORY_ANALYTICAL,
        llm=self.llm,
        verbose=True,
    )

    university_matcher = Agent(
        role="University & Course Matcher",
        goal=(
            "Identify specific universities, degree programs, scholarship"
            " opportunities, and intake deadlines matching the student"
            " profile."
        ),
        backstory=MatcherPrompts.BACKSTORY_EXPERT,
        llm=self.llm,
        verbose=True,
    )

    documentation_advisor = Agent(
        role="Visa & SOP Strategy Advisor",
        goal=(
            "Outline document checklists, visa financial requirements, and"
            " provide a structured framework for crafting a compelling"
            " Statement of Purpose (SOP)."
        ),
        backstory=AdvisorPrompts.BACKSTORY_EXPERT,
        llm=self.llm,
        verbose=True,
    )

    evaluate_task = Task(
        description=EvaluatorPrompts.TASK_DESCRIPTION,
        expected_output=(
            "An eligibility assessment report detailing candidate strengths,"
            " risk factors, and country feasibility."
        ),
        agent=evaluator,
    )

    match_task = Task(
        description=MatcherPrompts.TASK_DESCRIPTION,
        expected_output=(
            "A curated list of universities with program names, fee"
            " estimates, and key dates."
        ),
        agent=university_matcher,
    )

    doc_task = Task(
        description=AdvisorPrompts.TASK_DESCRIPTION,
        expected_output=(
            "A step-by-step documentation and SOP narrative framework for the"
            " student."
        ),
        agent=documentation_advisor,
    )

    return Crew(
        agents=[evaluator, university_matcher, documentation_advisor],
        tasks=[evaluate_task, match_task, doc_task],
        process=Process.sequential,
        verbose=True,
    )

  def run(
      self,
      academic_background: str,
      test_scores: str,
      budget: str,
      field_of_study: str,
  ) -> str:
    crew = self.assemble_crew()
    result = crew.kickoff(
        inputs={
            "academic_background": academic_background,
            "test_scores": test_scores,
            "budget": budget,
            "field_of_study": field_of_study,
        }
    )
    return str(result)
