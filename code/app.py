from flask import Flask, request, jsonify
import requests
from azureaiservice import *
from esgindicator import *
from cdpindicator import *
from models import *
import timeit

app = Flask(__name__)

@app.route("/")
def home():
     return "Welcome to Sustainability Benchmark API-Data Dazzelers Team"

@app.route("/esg/benchmark/upload/<entityName>",methods=["POST"])
def uploadBenchmark(entityName: str):
     begin = timeit.default_timer()
     file1 = request.files['file']
     result = readTextFromFilepypd2(file1)
     splitResult = result.split()
     answerResult = ""
     if splitResult.__len__() > 15000:
          noOfCompletionapicall = round(splitResult.__len__()/10000)
          for i in range(noOfCompletionapicall):
               messagetosend = ' '.join(splitResult[i*10000:(splitResult.__len__() if (i+1)*10000 > splitResult.__len__() else  (i+1)*10000 )])
               answerResult += getEnvironmentalAnswers(messagetosend)
               answerResult += getSocialAnswers(messagetosend)
               answerResult += getGovernanceAnswers(messagetosend)
          

     else:
          answerResult+= getEnvironmentalAnswers(result)
          answerResult += getSocialAnswers(result)
          answerResult += getGovernanceAnswers(result)

     netZeroresult = getFinalResultForQuestion(answerResult,"what is the Net Zero Target for company?")
     netZeroresultMeta: MetaData = MetaData("what is the Net Zero Target for company?","Environmental","Net Zero Target",netZeroresult,"")

     interimEmissions = getFinalResultForQuestion(answerResult, "what is the company strategy to reduce emissions?")
     interimEmissionsMeta: MetaData = MetaData("what is the interim emissions reduction target for company?","Environmental","Emissions Reduction Target",interimEmissions,"")

     renEnergyTarget = getFinalResultForQuestion(answerResult, "what is the renewable electricity target for company?")
     renEnergyTargetMeta: MetaData = MetaData("what is the renewable electricity target for company?","Environmental","Renewable Electricity Target",renEnergyTarget,"")

     circStrategyTarget = getFinalResultForQuestion(answerResult, "what is the circulatory strategy & targets for company?")
     circStrategyTargetmeta: MetaData = MetaData("what is the circulatory strategy & targets for company?","Environmental","circulatory strategy & targets",circStrategyTarget,"")

     divequityincl = getFinalResultForQuestion(answerResult, "what is the company target on Diversity, Equity and inclusion?")
     divequityinclMeta: MetaData = MetaData("what is the company target on Diversity, Equity and inclusion?","Social","Diversity Equity & Inclusion Target",divequityincl,"")

     healthSafety = getFinalResultForQuestion(answerResult, "what is the company thinks on Employee Health & Safety Audits")
     healthSafetyMeta: MetaData = MetaData("what is the company thinks on Employee Health & Safety Audits?","Governance","Employee Health & Safety Audits",healthSafety,"")

     supplyaudits = getFinalResultForQuestion(answerResult, "does company thinks any thing on Supply Chain Audits?")
     supplyauditsMeta: MetaData = MetaData("does company thinks any thing on Supply Chain Audits?","Governance","Supply Chain Audits",supplyaudits,"")

     print('getting details form esg')
     cssClasses = ['col-6 risk-rating-score', 'col-6 risk-rating-assessment', 'row company-name']
     esgIndictor = esg_scrape_value(esg_get_url(entityName.lower()), cssClasses)
     esgIndicatorMeta: MetaData = MetaData("What is ESG Score?", "ESG Score", "MSCI Sustainalysis", esgIndictor,"")

     cssClasses = ['search_results__response_score_band']
     cdpIndicator = scrape_value(get_url(entityName.lower()),cssClasses)
     cdpIndicatorMeta: MetaData = MetaData("What is CDP Value?", "Reporting", "CDP", cdpIndicator[0] if cdpIndicator.__len__()>0 else "None","")
          


     end = timeit.default_timer()
     metricData: Metrics = Metrics(end-begin, "GPT35Turbo-16K", "")

     finalResult: ResponseInternalDetails = ResponseInternalDetails(entityName, [netZeroresultMeta, interimEmissionsMeta, renEnergyTargetMeta, circStrategyTargetmeta, divequityinclMeta,healthSafetyMeta, supplyauditsMeta, esgIndicatorMeta, cdpIndicatorMeta], metricData)

     return (finalResult.toJSON()),200



@app.route("/esg/benchmark/upload/<entityName>/<esgType>/<esgIndicator>",methods=["POST"])
def upload_entity(entityName: str, esgType: str, esgIndicator: str):
     begin = timeit.default_timer()
     file = request.files['file']
     question = request.form["question"]
     result = readTextFromFilepypd2(file)
     splitResult = result.split()
     answerResult = ""

     if splitResult.__len__() > 15000:
          noOfCompletionapicall = round(splitResult.__len__()/10000)
          for i in range(noOfCompletionapicall):
               messagetosend = ' '.join(splitResult[i*10000:(splitResult.__len__() if (i+1)*10000 > splitResult.__len__() else  (i+1)*10000 )])
               message_text = [{"role":"system","content":  messagetosend+ "\n" + question}]
               answerResult+= chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
          
     else:
          message_text = [{"role":"system","content":  result+ "\n" + question}]
          answerResult += chatCompletion(initiateAzureClient(), message_text, "GPT35Turbo-16K")
     
     end = timeit.default_timer()
     metricData: Metrics = Metrics(end-begin, "GPT35Turbo-16K", "")
     metaDataResult: MetaData = MetaData(question, esgType, esgIndicator, getFinalResultForQuestion(answerResult, question),"")
     responseDetails: ResponseInternalDetailsScalar = ResponseInternalDetailsScalar(entityName, metaDataResult, metricData)

     return responseDetails.toJSON(),200

@app.route("/esg/benchmark/keepalive",methods=["GET"])
def keepalive():
    return jsonify("Api is working fine"),200



if __name__ == "__main__":
     app.run()
