# 📚 Book Summary Agent

Book Summary Agent is an application that extracts book titles and authors from text descriptions and provides summaries by scraping the web. The application uses GPT-4 and web scraping techniques to deliver accurate and comprehensive book summaries.

## Features

- Extracts book titles and authors from user-provided text.
- Searches the web for relevant book summaries.
- Displays summaries using a simple and intuitive interface.
- Powered by GPT-4 for high-quality natural language understanding.

## Prerequisites

Before you can run the application, you need to have the following installed:

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- [OpenAI Python library](https://pypi.org/project/openai/)
- [LangChain](https://langchain.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/en/master/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Google Search](https://pypi.org/project/googlesearch-python/)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Obtaining an OpenAI API Key

To use this application, you need an API key from OpenAI. You can obtain it by following these steps:

1. Go to the [OpenAI API website](https://beta.openai.com/signup/).
2. Sign up or log in to your account.
3. Navigate to the API keys section.
4. Create a new API key and copy it.
5. Paste the API key into the `.env` file in your project directory.

## Usage

### Running the Application

To run the application, use the following command:

```bash
streamlit run app.py
```

### Using the CLI

If you prefer to use the command-line interface (CLI), you can run the application with:

```bash
python app.py
```

## How It Works

1. **Input:** The user enters a prompt asking for a book summary.
2. **Extraction:** The application extracts the book title and author using a GPT-4 model.
3. **Search:** The application searches the web for relevant summaries.
4. **Summary:** The extracted information is summarized and displayed to the user.
