import pymongo
import datetime
import bucketing

if __name__ == "__main__":
    # making mongo connection
    client = pymongo.MongoClient("mongodb://s2c_dev:s2c_dev@localhost:27018/?authMechanism=DEFAULT&authSource=admin")
    
    # accesing s2c_dev db
    s2c_dev = client["s2c_dev"]

    # accessing collections
    surveys_collection = s2c_dev["surveys"]
    derivedvariables_collection = s2c_dev["derivedvariables"]
    responses_collection = s2c_dev["responses"]

    # surveys created or updated in last 30 mins
    last_30_minutes = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30))
    survey_documents = surveys_collection.find({"updatedAt": {"$gt": last_30_minutes}})

    for survey in survey_documents:
        for derived_variable in derivedvariables_collection.find({"updatedAt": {"$gt": last_30_minutes}, "surveyId": survey["uuid"]}):
            if derived_variable["type"] == "bucket":
                survey_responses = responses_collection.find({"surveyId": survey["uuid"]})
                bucketing.handle_bucketing(derived_variable, survey_responses)
            elif derived_variable["type"] == "formula":
                print("formula")
            elif derived_variable["type"] == "logical":
                print("logical")
