import os
import pdfplumber
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key="5c87b35ff8ac4183bc6f9c99060c653e",  
    api_version="2023-12-01-preview",
    azure_endpoint="https://team377-openapi.openai.azure.com/"
)

pdf_path = r"C:\Users\Sunil\Downloads\2022-Regal-Rexnord-Sustainability-Report.pdf"
text = ""
with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
            modifed_text = text.lower().replace("\n","")

print(text)
#completion = client.completions.create(
 #   model="gpt-35-turbo-instruct", # This must match the custom deployment name you chose for your model.
  #  prompt="<prompt>"
#)

questions = "What is the company name who owns this report? \n  what is the Net Zero Target?"

message_text = [{"role":"system","content": ' '.join(text.split()[:800])+ "\n" + questions}]
print(message_text)
chat_completion = client.chat.completions.create(
    model="GPT35Turbo-16K", # model = "deployment_name"
    messages = message_text,
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)

#embedding = client.embeddings.create(
 #   model="text-embedding-ada-002", # model = "deployment_name".
  #  input="<input>"
#)

print(chat_completion.model_dump_json(indent=2))
print(chat_completion.choices[0].message.content)