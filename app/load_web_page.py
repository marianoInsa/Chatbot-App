# import requests
import bs4
from langchain_community.document_loaders import WebBaseLoader
# from bs4 import BeautifulSoup
# from langchain_core.documents import Document
# from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
load_dotenv()

def load_web_page(url1, url2, url3, url4):
    """
    Load a web page and extract its content.
    """
    # docs = []
    # for url in urls:
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(headless=True)
    #         page = browser.new_page()
    #         page.goto(url)
    #         html = page.content()
    #         browser.close()

    #         soup = BeautifulSoup(html, 'lxml')
    #         # print(soup.title.string)
            
    #         elements = soup.find_all(class_="wixui-rich-text__text")
    #         element_text = ""
    #         for element in elements:
    #             if element.name == 'h1':
    #                 element_text += "\n" + element.get_text()
    #         docs.append(
    #             Document(
    #                 page_content=element_text,
    #                 metadata={
    #                     "url": url,
    #                     "title": soup.title.string
    #                 }
    #             )
    #         )

    bs4_strainer = bs4.SoupStrainer(class_=("wixui-rich-text__text"))
    loader = WebBaseLoader(
        web_paths=(url1, url2, url3, url4,),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    return docs

if __name__ == "__main__":
    # urls = (
    #     os.getenv('URL_1'),
    #     os.getenv('URL_2'),
    #     os.getenv('URL_3'),
    #     os.getenv('URL_4')
    # )
    docs = load_web_page(os.getenv('URL_1'), os.getenv('URL_2'), os.getenv('URL_3'), os.getenv('URL_4'))
    print(docs[0].page_content)
    # for doc in docs:
    #     print(f"\n>> URL: {doc.metadata['url']}")
    #     print(doc.page_content)
    #     print("==="*20)