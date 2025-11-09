# AI Letter Generator

This is a Streamlit application that uses the Gemini API to generate letters and create PDF files.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AI_Letter_Generator
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Create a `.env` file:**
    -   Create a file named `.env` in the root of the project.
    -   Add your Gemini API key to the `.env` file like this:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

## Running the Application

-   **On Windows:**
    -   Run the `start_app.bat` file.
-   **On macOS/Linux:**
    -   Run the following command in your terminal:
        ```bash
        streamlit run app.py
        ```

The application will open in your web browser.
