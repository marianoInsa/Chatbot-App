# import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
load_dotenv()

def load_web_page(urls):
    """
    Load a web page and extract its content.
    """
    docs = []
    for url in urls:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, 'lxml')
            # print(soup.title.string)
            
            elements = soup.find_all(class_="wixui-rich-text__text")
            element_text = ""
            for element in elements:
                if element.name == 'h1':
                    element_text += "\n" + element.get_text()
            docs.append(
                Document(
                    page_content=element_text,
                    metadata={
                        "url": url,
                        "title": soup.title.string
                    }
                )
            )
    return docs

if __name__ == "__main__":
    urls = [
        os.getenv('URL_1'),
        os.getenv('URL_2'),
        os.getenv('URL_3'),
        os.getenv('URL_4')
    ]
    docs = load_web_page(urls)
    for doc in docs:
        print(f"\n>> URL: {doc.metadata['url']}")
        print(doc.page_content)
        print("==="*20)