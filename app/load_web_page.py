# import requests
from dotenv import load_dotenv
import os
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")
from bs4 import SoupStrainer
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
import re

def load_web_page(url1, url2, url3, url4):
    """
    Load a web page and extract its content.
    """
    docs = []
    for url in (url1, url2, url3, url4):
        # print(f"\n\nLoading URL: {url}")
        strainer = SoupStrainer(class_=("wixui-rich-text__text"))
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs={"parse_only": strainer},
            header_template={"User-Agent": USER_AGENT},
        )
        raw_docs = loader.load()
        # print(f"\n Raw docs: \n\n {raw_docs} \n\n" + "="*20)
        for doc in raw_docs:
            cleaned_text = doc.page_content
            
            cleaned_text = cleaned_text.replace(".",". ").replace(",",", ").replace("  ", " ").replace("\xa0", " ").replace("\u200b", " ").strip()

            cleaned_text = re.sub(r"([a-z])([A-Z])", r"\1 \2", cleaned_text)

            docs.append(
                Document(
                    page_content=cleaned_text,
                    metadata=doc.metadata
                )
            )

    return docs

if __name__ == "__main__":
    # urls = (
    #     os.getenv('URL_1'),
    #     os.getenv('URL_2'),
    #     os.getenv('URL_3'),
    #     os.getenv('URL_4')
    # )
    docs = load_web_page(os.getenv('URL_1'), os.getenv('URL_2'), os.getenv('URL_3'), os.getenv('URL_4'))
    #print(docs[0].page_content)
    print(f"\n Docs: \n\n {docs} \n\n" + "="*20)
    for doc in docs:
        print(f"\n>> Metadata: {doc.metadata}")
        print("\n\nContenido:\n")
        print(doc.page_content)
        print("==="*20)