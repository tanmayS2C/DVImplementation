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
    row_id = bucketing_logic["fieldId"]["rowId"] if "rowId" in bucketing_logic["fieldId"] else None
    domains = bucketing_logic["domains"]
    mapping = bucketing_logic["mapping"]

    help_dict = {}
    for bucket_name in domains:
        for bucket in mapping[bucket_name]:
            # if edata_or_ques == "Edata":
            #     help_dict[val] = bucket_name
            #     Help_type = "Edata"
            if "colId" in bucket:
                help_dict[bucket["colId"]] = bucket_name
                help_type = "colId"
            else:
                help_dict[bucket["rowId"]] = bucket_name
                help_type = "rowId"


    for response in survey_responses:
        for res in response["answers"][ques_id]:
            if row_id and res["rowId"] == row_id and res["colId"] in help_dict:
                dv_value = help_dict[res["colId"]]
                print(dv_value)
            elif row_id and res["rowId"] == row_id and res["colId"] not in help_dict:
                dv_value=None
                print(dv_value)
            elif not row_id and res["rowId"] in help_dict:
                dv_value = help_dict[res["rowId"]]
                print(dv_value)
            

