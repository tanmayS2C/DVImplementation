import math

import handle_dv


def get_open_ended_value(operator_map, single_response):
    answer_array = single_response["answers"][operator_map["fieldId"]]

    for answer in answer_array:
        if not "rowId" in operator_map:
            val = answer["text"]
            return str(int(val)) if val.isnumeric() else "None"

        elif "rowId" in operator_map and answer["rowId"] == operator_map["rowId"]:
            if "colId" not in operator_map:
                val = answer["text"]
                return str(int(val)) if val.isnumeric() else "None"
            elif "colId" in operator_map and answer["colId"] == operator_map["colId"]:
                val = answer["text"]
                return str(int(val)) if val.isnumeric() else "None"


def get_close_ended_value(operator_map, single_response, questions_collection):
    return "0"


def get_ques_value(operator_map, single_response, questions_collection):
    if "quesCode" in operator_map:
        return get_close_ended_value(
            operator_map, single_response, questions_collection
        )
    else:
        return get_open_ended_value(operator_map, single_response)


def get_edata_value(operator_map, single_response):
    edata_field = operator_map["fieldId"]
    if edata_field in single_response["embedDataArr"]:
        return (
            str(int(single_response["embedData"][edata_field]))
            if single_response["embedData"][edata_field].isnumeric()
            else "None"
        )


def get_dv_value(operator_map, single_response):
    dv_field_id = operator_map["fieldId"]
    if dv_field_id in single_response["derivedVarArr"]:
        return (
            str(int(single_response["derivedVar"][dv_field_id]))
            if single_response["derivedVar"][dv_field_id].isnumeric()
            else "None"
        )


def get_value(operator_map, single_response, questions_collection):
    if operator_map["fieldType"] == "dv":
        return get_dv_value(operator_map, single_response)
    elif operator_map["fieldType"] == "edata":
        return get_edata_value(operator_map, single_response)
    elif operator_map["fieldType"] == "ques":
        return get_ques_value(operator_map, single_response, questions_collection)


def handle_formula(
    derived_variable, survey_responses, responses_collection, questions_collection
):
    expression = derived_variable["formulaLogic"]["expression"]
    domains = derived_variable["formulaLogic"]["domains"]
    mapping = derived_variable["formulaLogic"]["mapping"]

    expression = expression.replace("ceil", "math.ceil").replace("floor", "math.floor")

    for single_response in survey_responses:
        temp_expression = expression
        for operator in domains:
            operator_map = mapping[operator]
            temp_expression = temp_expression.replace(
                operator, get_value(operator_map, single_response, questions_collection)
            )

        if "None" in temp_expression:
            continue

        print((temp_expression))
