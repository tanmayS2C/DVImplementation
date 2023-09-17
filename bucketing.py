from collections import defaultdict


def handle_bucketing(derived_variable, survey_responses, response_collection):
    bucketing_logic_name = derived_variable["name"]

    # bucketing_logic
    bucketing_logic = derived_variable["bucketingLogic"]
    edata_or_ques = bucketing_logic["fieldType"]
    ques_id = bucketing_logic["fieldId"]["id"]
    row_id = (
        bucketing_logic["fieldId"]["rowId"]
        if "rowId" in bucketing_logic["fieldId"]
        else None
    )
    domains = bucketing_logic["domains"]
    mapping = bucketing_logic["mapping"]

    e_data_field = bucketing_logic["fieldId"]["id"]

    help_dict = defaultdict(str)
    for bucket_name in domains:
        for bucket in mapping[bucket_name]:
            if edata_or_ques == "edata":
                help_dict[bucket["id"]] = bucket_name
            elif "colId" in bucket:
                help_dict[bucket["colId"]] = bucket_name
            else:
                help_dict[bucket["rowId"]] = bucket_name

    for response in survey_responses:

        if edata_or_ques == "edata" and response["embedDataArr"]:
            for e_data in response["embedDataArr"]:
                if e_data == e_data_field:
                    dv_value = help_dict[response["embedData"][e_data_field]]
                    break
            else:
                dv_value = None

        elif ques_id in response["answers"]:
            for res in response["answers"][ques_id]:
                if row_id and res["rowId"] == row_id and res["colId"] in help_dict:
                    dv_value = help_dict[res["colId"]]
                    break
                elif not row_id and res["rowId"] in help_dict:
                    dv_value = help_dict[res["rowId"]]
                    break
            else:
                dv_value = None
        else:
            dv_value = None

        derivedVarArr = response["derivedVarArr"]
        derivedVarArr.append(derived_variable["name"])

        derivedVar = response["derivedVar"] if "derivedVar" in response else {}
        derivedVar[str(derived_variable["name"])] = dv_value

        filter = {"uuid": response["uuid"]}
        response_collection.update_one(
            filter, {"$set": {"derivedVarArr": derivedVarArr, "derivedVar": derivedVar}}
        )
