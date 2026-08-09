import requests
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="AI Study Abroad Consultancy", page_icon="🎓", layout="wide"
)

st.title("🎓 AI-Powered Study Abroad Consultancy Engine")
st.markdown(
    "Automate profile evaluation, university matching, and visa roadmap"
    " generation using a multi-agent AI workforce."
)

with st.form("consultation_form"):
  col1, col2 = st.columns(2)

  with col1:
    academic_background = st.text_input(
        "Academic Background",
        value="Bachelor's in Computer Science",
        placeholder="e.g., Bachelor's in Computer Science",
    )
    gpa_score = st.text_input(
        "GPA / Percentage Score",
        value="66% (2.64/4.0)",
        placeholder="e.g., 66% or 3.2/4.0",
    )
    test_scores = st.text_input(
        "Test Scores",
        value="IELTS: 7.5 overall",
        placeholder="e.g., IELTS: 7.5 overall",
    )

  with col2:
    budget = st.text_input(
        "Annual Budget",
        value="$25,000 USD per year max",
        placeholder="e.g., $25,000 USD per year max",
    )
    field_of_study = st.text_input(
        "Target Field of Study",
        value="Master's in Data Science or Artificial Intelligence",
        placeholder="e.g., Master's in Data Science",
    )

  submitted = st.form_submit_button("Generate Consultation Roadmap")

if submitted:
  if not all([academic_background, gpa_score, test_scores, budget, field_of_study]):
    st.warning("Please fill in all required fields.")
  else:
    with st.spinner(
        "🤖 AI Agents are evaluating your profile, researching universities,"
        " and drafting your roadmap..."
    ):
      try:
        payload = {
            "academic_background": academic_background,
            "gpa_score": gpa_score,
            "test_scores": test_scores,
            "budget": budget,
            "field_of_study": field_of_study,
        }

        # Send POST request to your FastAPI backend
        response = requests.post(
            "http://localhost:8000/api/v1/consult", json=payload, timeout=120
        )

        if response.status_code == 200:
          data = response.json()
          st.success("Consultation Roadmap Generated Successfully!")
          st.markdown("---")
          st.markdown(data.get("consultation_report"))
        else:
          st.error(
              f"Error from server ({response.status_code}): {response.text}"
          )

      except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the FastAPI backend. Ensure your server is"
            " running at http://localhost:8000"
        )
      except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
