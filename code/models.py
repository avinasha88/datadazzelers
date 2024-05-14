import json


class MetaData:
     def __init__(self, question, esgType, esgIndicators,primaryDetails,secondaryDetails):
          self.question = question
          self.esgType = esgType
          self.esgIndicators = esgIndicators
          self.primaryDetails = primaryDetails
          self.secondaryDetails = secondaryDetails

class Metrics:
     def __init__(self, timeTaken, leveragedModel, f1Score):
          self.timeTaken = timeTaken
          self.leveragedModel = leveragedModel
          self.f1Score = f1Score

class ResponseInternalDetails:
     def __init__(self, entityName, benchmarkDetails, metrics):
          self.entityName = entityName
          #self.fileName = fileName
          self.benchmarkDetails = benchmarkDetails
          self.metrics = metrics
     def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class ResponseInternalDetailsScalar:
     def __init__(self, entityName:str, benchmarkdetails: MetaData, metrics: Metrics):
          self.entityName = entityName
          self.benchmarkdetails = benchmarkdetails
          self.metrics = metrics
     def toJSON(self):
          return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
          