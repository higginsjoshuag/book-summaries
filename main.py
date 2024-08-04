from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

def search_book_info(book_title):
    query = f"{book_title} book summary"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    snippets = soup.find_all(['div', 'span'], class_=['aCOpRe', 'IsZvec'])
    summary = ' '.join([snippet.get_text() for snippet in snippets[:3]]) if snippets else ""
    return summary if summary else "No summary found."

class BookSummaryAgent:
    def __init__(self, llm):
        self.llm = llm
        self.title_extraction_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["input_text"],
                template="Extract the book title from the following text. If there's no clear book title, say 'No book title found'. Text: {input_text}\nExtracted title:"
            )
        )
        self.summary_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["book_info"],
                template="Summarize the following book information in a concise paragraph:\n\n{book_info}\n\nSummary:"
            )
        )

    def run(self, input_text):
        extracted_title = self.title_extraction_chain.invoke({"input_text": input_text})["text"].strip()
        if extracted_title.lower() == "no book title found":
            return "Hmm... couldn't find a valid book title."
        
        book_info = search_book_info(extracted_title)
        if book_info == "No summary found.":
            return f"Sorry, I couldn't find a summary for '{extracted_title}'."
        
        summary = self.summary_chain.invoke({"book_info": book_info})["text"]
        return f"Summary for '{extracted_title}':\n{summary}"

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    llm = OpenAI(temperature=0.7)
    agent = BookSummaryAgent(llm)
    
    while True:
        user_input = input("Enter your prompt (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        summary = agent.run(user_input)
        print("\nResult:")
        print(summary)
        print("\n" + "="*50 + "\n")