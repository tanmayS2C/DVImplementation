import pymongo

def handle_bucketing(derived_variable, survey_responses):
    # survey_id
    survey_id = derived_variable["surveyId"]
    
    # bucket_logic_name
    bucketing_logic_name = derived_variable["name"]

    # bucketing_logic 
    bucketing_logic = derived_variable["bucketingLogic"]
    edata_or_ques = bucketing_logic["fieldType"] 
    ques_id = bucketing_logic["fieldId"]["id"]
    domains = bucketing_logic["domains"]
    mapping = bucketing_logic["mapping"]

    help_dict = {}
    for bucket_name in domains:
        for bucket in mapping[bucket_name]:
            print(bucket)
            # if type == "Edata":
            #     help_dict[val] = bucket
            #     Help_type = "Edata"
            # elif "col_id" in val:
            #     help_dict[col_id] = bucket
            #     Help_type = "col_id"
            # else;
            #     help_dict[row_id] = bucket
            #     Help_type = "row_id"


    # if edata_or_ques == "ques":
    #     print(ques_id)
