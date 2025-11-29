import streamlit as st
from fpdf import FPDF
import os
import openai

# --- Agent Functions (Optimized AI) ---

@st.cache_data
def run_llm_prompt(prompt):
    """
    Runs a prompt through the OpenAI API and returns the response.
    """
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        st.error("API Key not found! Please add your key to the Streamlit secrets.")
        return "Error: API Key not configured."

    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    except Exception as e:
        st.error(f"An error occurred with the API call: {e}")
        return f"Error: {e}"
def generate_letter_agent(purpose, recipient, details, tone):
      """
      Generates a complete letter by combining research and writing into one prompt.
      """
      st.info("Generate Agent: Researching and drafting letter...")
      prompt = f"""
  Act as a professional and empathetic letter writer. Your task is to draft a complete
  personal letter. First, internally consider the best keywords, phrases, and overall
  sentiment for the letter's context. Then, write a complete, well-structured letter with
  an opening, a body, and a closing.

  Letter Context:
  - Purpose of Letter: {purpose}
  - Recipient's Name: {recipient}
  - Key Details to Include: {details}
  - Desired Tone: {tone}

  Instructions:
  Write only the letter content itself, starting with 'Dear {recipient},'. Do not include
  any extra commentary, titles, or salutations before the letter begins.
  """
      return run_llm_prompt(prompt)

def review_and_pdf_agent(letter_text, sender_name, sender_address):
      """
      Reviews the letter for grammar/spelling using the Gemini API and creates a PDF.
      """
      st.info("Review Agent: Checking grammar and spelling...")
      prompt = f"""
  Act as a meticulous proofreader. Review the following letter for grammar, spelling, and
  punctuation errors. Ensure it flows naturally and that the tone is consistent. Return
  only the corrected, final version of the letter without any of your own commentary.

  Here is the text to review:
  {letter_text}
  """
      corrected_text = run_llm_prompt(prompt)

      st.info("PDF Agent: Formatting the letter...")

      # Sanitize text for PDF generation by replacing unsupported characters
      pdf_safe_text = corrected_text.encode('latin-1', 'replace').decode('latin-1')
      safe_sender_name = sender_name.encode('latin-1', 'replace').decode('latin-1')
      safe_sender_address = sender_address.encode('latin-1', 'replace').decode('latin-1')

      pdf = FPDF()
      pdf.add_page()
      pdf.set_font("Arial", size=12)

      # Add sender's address
      if safe_sender_name:
          pdf.cell(0, 5, safe_sender_name, ln=True, align='L')
      if safe_sender_address:
          pdf.multi_cell(0, 5, safe_sender_address, align='L')

      pdf.ln(10) # Add space

      # Add letter body using the sanitized text
      pdf.multi_cell(0, 5, pdf_safe_text)

      # Return PDF as bytes
      return corrected_text, pdf.output(dest='S').encode('latin1')


  # --- Streamlit Frontend ---

st.title("AI Letter Generator")

st.sidebar.header("Your Information")
sender_name_input = st.sidebar.text_input("Your Name", placeholder="John Doe")
sender_address_input = st.sidebar.text_area("Your Address", placeholder="123 Main Street\\nAnytown, USA 12345")

st.sidebar.header("How to Use")
st.sidebar.info(
      "1. Fill out your info in the sidebar."
      "2. Define the letter's purpose, recipient, tone, and details in the main panel."
      "3. Click 'Generate Letter'."
      "4. Review the output and download the PDF."
  )

st.header("1. Define Your Letter")

  # Inputs for need/request and tone
need_request = st.text_input("What is the purpose of the letter?", placeholder="e.g.,Thank you, Condolence, Formal Complaint")
recipient_name = st.text_input("Who is the recipient?", placeholder="e.g., Aunt Mary,Hiring Manager")
tone = st.selectbox("Select the tone:", ["Casual", "Formal", "Heartfelt", "Humorous","Professional"])
key_details = st.text_area("What key details should be included?", placeholder="e.g.,For the beautiful handmade sweater, it fits perfectly and I love the color.")

  # Initialize session state variables
if 'generated_letter' not in st.session_state:
      st.session_state.generated_letter = ""
if 'pdf_bytes' not in st.session_state:
      st.session_state.pdf_bytes = b""
if 'generation_complete' not in st.session_state:
      st.session_state.generation_complete = False

  # Generate Letter Button
if st.button("Generate Letter", type="primary"):
      st.session_state.generation_complete = False # Reset on new generation
      if not all([need_request, recipient_name, tone, key_details]):
          st.warning("Please fill out all fields in the main panel before generating aletter.")
      else:
          with st.spinner("Agents are at work..."):
              # 1. Generate Agent (Combined Research and Writing)
              draft_letter = generate_letter_agent(need_request, recipient_name,
  key_details, tone)

              # 2. Review and PDF Agent
              final_letter, pdf_bytes = review_and_pdf_agent(draft_letter,
  sender_name_input, sender_address_input)

              # Store results in session state
              st.session_state.generated_letter = final_letter
              st.session_state.pdf_bytes = pdf_bytes
              st.session_state.generation_complete = True # Set flag to show output

              st.success("Letter generated successfully!")

  # Display generated letter and download button
if st.session_state.generation_complete:
      st.header("2. Review and Download")
      st.text_area("Generated Letter:", value=st.session_state.generated_letter,
  height=300)

      st.download_button(
          label="Download as PDF",
          data=st.session_state.pdf_bytes,
          file_name=f"{need_request.replace(' ', '_').lower()}_letter.pdf",
          mime="application/pdf"
      )
    