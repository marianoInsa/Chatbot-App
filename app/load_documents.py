import pdfplumber
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)
from langchain_core.documents import Document
# from collections import defaultdict

def load_documents(pdf_path):
  """
  Load documents from a PDF file and extract text.
  """
  docs = []
  with pdfplumber.open(pdf_path) as pdf:
      pages = pdf.pages
      for i, page in enumerate(pages):
          text = f"Pagina {i + 1}:\n"
          text = page.extract_text()
          text = text.strip()

          # links = []
          # if page.annots:
          #    for annot in page.annots:
          #       uri = annot.get('uri')
          #       if uri:
          #           links.append(uri)
          
          # if links:
          #    text += "\n Links en la página: \n"
          #    text += "\n".join(links)

          # print(f"Page {i + 1}:\n{text}\n")

          docs.append(
             Document(
                page_content=text,
                metadata={
                    "page": i + 1
                    # "links": links
                }
             )
          )
      return docs


      #     words = page.extract_words()
      #     if not words:
      #        continue
          
      #     # Agrupar horizontalmente las palabras
      #     rows = defaultdict(list)
      #     for word in words:
      #         row_y = round(word['top'] / 80) * 80
      #         # if col_x not in cols:
      #         #     cols[col_x] = []
      #         rows[row_y].append(word)
          
      #     # Ordenar filas de arriba a abajo
      #     sorted_rows = [rows[y] for y in sorted(rows)]

      #     # Reconstruir el texto de cada columna
      #     cols_text = []
      #     for row in sorted_rows:
      #         sorted_row = sorted(row, key=lambda w: w['x0'])
      #         row_text = ' '.join([word['text'] for word in sorted_row])
      #         # if row_text:
      #         #     cols_text.append(row_text)
      #         cols_text.append(row_text.strip())
          
      #     if text and len(text.strip()) > 30:
      #        content = text.strip()
      #     else:
      #        content = "\n".join(cols_text)

      #     docs.append(Document(page_content=content, metadata={"page": i + 1}))

      # return docs
          
          # if page.extract_table():
          #   cols = {}
          #   words = page.extract_words()
          #   for word in words:
          #     col_x = round(word['x0'] / 40) * 40
          #     if col_x not in cols:
          #         cols[col_x] = []
          #     cols[col_x].append(word)
            
          #   for x in sorted(cols):
          #     col_words = cols[x]
          #     sorted_words = sorted(col_words, key=lambda w: w['top'])
          #     text = ' '.join([word['text'] for word in sorted_words])
          #     if text.strip():
          #         print(f"Column {x}: {text}")



          # print(f"Page {i + 1} Table:")
          # words = page.extract_words()

          # rows = {}
          # for word in words:
          #     top = round(word['top'] / 5) * 5
          #     if top not in rows:
          #         rows[top] = []
          #     rows[top].append(word)
          
          # sorted_rows = [rows[k] for k in sorted(rows)]
          # names = []

          # for row in sorted_rows:
          #     # ordenar las palabras de izquierda a derecha
          #     sorted_row = sorted(row, key=lambda w: w['x0'])

          #     name = ''
          #     last_x = None

          #     for word in sorted_row:
          #         x = word['x0']
          #         text = word['text']

          #         if last_x is None:
          #             name = text
          #         else:
          #             distance = x - last_x
          #             if distance < 60:
          #                 name += " " + text
          #             else:
          #                 names.append(name)
          #                 name = text
                  
          #         last_x = word['x1']
              
          #     if name:
          #         names.append(name)
          
          # print(names)

if __name__ == "__main__":

  pdf_path = "data/documento.pdf"
  doc = load_documents(pdf_path)
  for d in doc:
      print(f'\n>> Page {d.metadata["page"]}:')
      print(d.page_content)
      print("===" * 20)