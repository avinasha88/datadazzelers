from openai import AzureOpenAI
import pdfplumber
import PyPDF2 as pypdf2
import spacy

def initiateAzureClient():
    client = AzureOpenAI(
    api_key="5c87b35ff8ac4183bc6f9c99060c653e",  
    api_version="2023-12-01-preview",
    azure_endpoint="https://team377-openapi.openai.azure.com/"
)
    return client

def chatCompletion(client, prompt, modelName):
    chat_completion = client.chat.completions.create(
    model=modelName, # model = "deployment_name"
    messages = prompt,
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)

    print(chat_completion.model_dump_json(indent=2))
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

def readTextFromFile(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:         
            spacyText = cleanText(page.extract_text())
            questions = "What is the company name who owns this report? \n  what is the Net Zero Target?"
            message_text = [{"role":"system","content":  (spacyText)+ "\n" + questions}]
            answer = chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
            text += answer
    return text

def readTextFromFilepypd2(file):
     policy_text = ""
     reader = pypdf2.PdfReader(file)
     for page in reader.pages:
        policy_text+= page.extract_text()
     return policy_text

def cleanText(message: str):
    modifedMesage = ""
    modifedMesage = message.replace("\n","")
    nlp = spacy.load("en_core_web_sm")
    spacyMessage = " ".join([token.lemma_ for token in nlp(modifedMesage)]) 
    return spacyMessage

def getFinalResultForQuestion(messagetosend: str, question: str):
      message_text = [{"role":"system","content":  messagetosend+ "\n" + question}]
      answerResult = chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
      return answerResult

def getSocialAnswers(messagetosend: str):
     questions = " what is the company target on Diversity, Equity and inclusion?"
     message_text = [{"role":"system","content":  messagetosend+ "\n" + questions}]
     answerResult = chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
     return answerResult

def getGovernanceAnswers(messagetosend: str):
     questions = "what is the company thinks on Employee Health & Safety Audits and Supply Chain Audits?"
     message_text = [{"role":"system","content":  messagetosend+ "\n" + questions}]
     answerResult = chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
     return answerResult

def getEnvironmentalAnswers(messagetosend: str):
     questions = "What is the company name who owns this report? \n  what is the Net Zero Target, interim emissions reduction target, renewable electricity target, circulatory strategy & targets for environment?"
     message_text = [{"role":"system","content":  messagetosend+ "\n" + questions}]
     result = chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
     return result