import streamlit as st
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from dotenv import load_dotenv
import openai
import os
import time
import random
import json
import sys

# Function to search and scrape book summaries
def search_and_scrape(book_title, num_results=10):
    query = f"{book_title} book summary"
    search_results = search(query, num_results=num_results)

    summaries = []
    for result in search_results:
        if "ad" in result:  # Skip ads
            continue

        try:
            response = requests.get(result, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                summary = extract_summary(soup)
                if summary:
                    summaries.append(summary)
                    if len(summaries) >= num_results:
                        break
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {result}: {e}")
        time.sleep(random.uniform(2, 5))  # Avoid rapid-fire requests

    return summaries if summaries else ["No suitable summaries found."]

# Function to extract summary from BeautifulSoup object
def extract_summary(soup):
    paragraphs = soup.find_all('p')
    if paragraphs:
        return " ".join(p.get_text() for p in paragraphs)
    return None

class BookSummaryAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = openai.OpenAI()

    def run(self, input_text):
        """Extracts the title and author from the input text."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": (
                        "Extract the book title and author from the following text. "
                        "Return the result in JSON format with keys 'title' and 'author'. "
                        "If there's no clear book title, set the title to 'No book title found' "
                        "and if there's no clear author, set the author to 'Unknown'. "
                        f"Text: {input_text}"
                    )}
                ]
            )
            extracted_info = response.choices[0].message["content"].strip()
            extracted_data = json.loads(extracted_info)
            extracted_title = extracted_data.get("title", "No book title found")
            author = extracted_data.get("author", "Unknown")
        except json.JSONDecodeError:
            return None, "Hmm... couldn't parse the input properly."
        except OpenAIError as e:
            return None, f"OpenAI Error: {str(e)}"

        if extracted_title.lower() == "no book title found":
            return None, "Hmm... couldn't find a valid book title."

        return {"title": extracted_title, "author": author}, None

    def summarize(self, extracted_title):
        """Searches and summarizes the book information."""
        summaries = search_and_scrape(extracted_title)
        if not summaries or summaries[0] == "No suitable summaries found.":
            return f"Sorry, I couldn't find a summary for '{extracted_title}'."

        try:
            book_info = summaries[0]
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": (
                        f"Summarize the following book information: {book_info}"
                    )}
                ]
            )
            summary = response.choices[0].message["content"].strip()
        except OpenAIError as e:
            return f"OpenAI Error: {str(e)}"
        return summary
    
    def run_local(self):
        """Runs the agent in a command-line interface."""
        while True:
            user_input = input("Enter your prompt (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            extracted_data, error = self.run(user_input)
            if error:
                print(error)
            elif extracted_data:
                print(f"Extracted Title: {extracted_data['title']}")
                print(f"Extracted Author: {extracted_data['author']}")
                print("Looking on the web for you...")
                summary = self.summarize(extracted_data["title"])
                print("\nBook Summary:")
                print(summary)
                print("\n" + "="*50 + "\n")

# Main Streamlit app
def main():
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    openai.api_key = api_key  # Set the API key for the OpenAI client
    
    model_name = 'gpt-4o'  # or whichever model you're using
    agent = BookSummaryAgent(model_name)

    # Check if running in Streamlit
    if 'streamlit.runtime.scriptrunner.script_run_context' in sys.modules:
        run_streamlit(agent)
    else:
        agent.run_local()

def run_streamlit(agent):
    # Sidebar with additional information or options
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app extracts book titles and authors from text descriptions and provides summaries from the web. 
        Powered by GPT-4 and web scraping.
        """
    )

    st.title("📚 LangChain Book Summary Agent")
    st.write("Enter a prompt asking for a book summary. The agent will extract the book title, search for information, and provide a summary.")

    user_input = st.text_input("Enter your prompt:")
    if st.button("Get Summary"):
        if user_input:
            with st.spinner("Extracting book title and author..."):
                extracted_data, error = agent.run(user_input)
            
            if error:
                st.error(error)
            elif extracted_data:
                st.write(f"**Extracted Title:** {extracted_data['title']}")
                st.write(f"**Extracted Author:** {extracted_data['author']}")
                st.success("Title and author extracted successfully!")
                
                with st.spinner("Looking on the web for a summary..."):
                    summary = agent.summarize(extracted_data["title"])
                    st.subheader("Book Summary")
                    st.write(summary)
        else:
            st.error("Please enter some text to analyze.")

if __name__ == "__main__":
    main()