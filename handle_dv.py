import datetime

import pymongo

import bucketing
import formula
import logical

if __name__ == "__main__":
    # making mongo connection
    client = pymongo.MongoClient(
        "mongodb://s2c_dev:s2c_dev@localhost:27018/?authMechanism=DEFAULT&authSource=admin"
    )

    # accesing s2c_dev db
    s2c_dev = client["s2c_dev"]

    # accessing collections
    surveys_collection = s2c_dev["surveys"]
    derivedvariables_collection = s2c_dev["derivedvariables"]
    responses_collection = s2c_dev["responses"]
    questions_collection = s2c_dev["questions"]

    last_30_minutes = datetime.datetime.utcnow() - datetime.timedelta(minutes=100)
    for derived_variable in derivedvariables_collection.find(
        {"updatedAt": {"$gt": last_30_minutes}}
    ):
        survey_responses = responses_collection.find(
            {"surveyId": derived_variable["surveyId"]}
        )
        if derived_variable["type"] == "bucket":
            bucketing.handle_bucketing(
                derived_variable, survey_responses, responses_collection
            )
        elif derived_variable["type"] == "formula":
            formula.handle_formula(
                derived_variable,
                survey_responses,
                responses_collection,
                questions_collection,
            )
        elif derived_variable["type"] == "logical":
            logical.handle_logical(
                derived_variable, survey_responses, responses_collection
            )
