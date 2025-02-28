
# Configurando StreamLite:
import streamlit as st
import pdfplumber
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Criptografando a chave da API do Gemini e configurando
load_dotenv(override=True)

chave = os.getenv("chave_api")
genai.configure(api_key=chave)

# Funcao para extrair o texto do PDF
def extract_text_from_pdf(pdf_file):
  text = ""
  with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
      text += page.extract_text() or ""
  return text

# Funcao para a API resumir o texto
def summarize_text(text):
  try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([f"Por favor, resuma o seguinte texto: \n\n{text}"])
    return response.text
  except Exception as e:
    return f"Deu Ruim... {e}"

# Funcao para a API responder perguntas
def question_text(text, question):
  try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([f"Por favor, responda a seguinte pergunta baseada no seguinte texto:\n\nTexto: {text}\n\nPergunta: {question}"])
    return response.text
  except Exception as e:
    return f"Deu ruim... {e}"

# Streamlite APP
def main():
  st.title("Resuma seu PDF e tire suas dúvidas com Gemini-PRO")

  uploaded_file = st.file_uploader("Carregue seu PDF", type="pdf")

  if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    display_text = text[:500] + ('...' if len(text) > 500 else '')

    st.subheader("Texto Extraído")
    st.text_area("Texto do PDF", display_text, height=300)

    if st.button("Faça um Resumo"):
      summary = summarize_text(text)
      st.subheader("Resumo")
      st.write(summary)
    question = st.text_input("Faça sua pergunta sobre o PDF")
    if st.button("Responda"):
      if question:
        answer = question_text(text, question)
        st.subheader("Resposta")
        st.write(answer)
      else:
        st.warning("Escreva uma paergunta para ter uma resposta")

if __name__ == "__main__":
  main()