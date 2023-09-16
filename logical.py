operator_dict = {
    "eq":  " == ",
    "neq": " != ",
    "lt": " < ",
    "lte": " <= ",
    "gt": " > ",
    "gte": " >= ",
    "con": " in ",
    "ans": "ans"
}

def handle_single_logic_close_ended(single_condition, single_response):
    answers = single_response["answers"]
    left_operand = single_condition["data"]["leftOperand"]
    right_operand_arr = single_condition["data"]["rightOperand"]
    operator = single_condition["data"]['operator']

    left_value = None
    right_arr = []

    if "answers" in single_response and left_operand["id"] in single_response["answers"]:
        answer_array = single_response["answers"][left_operand["id"]]
    else:
        print(False)
        return

    if 'colId' in right_operand_arr[0]:
        for answer in answer_array:
            if answer["rowId"] == left_operand["rowId"]:
                left_value = answer["colId"]
                break

        right_arr = [ right_operand["colId"] for right_operand in right_operand_arr ]
    else:
        for answer in answer_array:
                left_value = answer["rowId"]
                break

        right_arr = [ right_operand["rowId"] for right_operand in right_operand_arr ]
    
    if operator == "eq": return left_value in right_arr
    else: return left_value not in right_arr

def handle_single_logic_open_ended(single_condition, single_response):
    right_operand = single_condition["data"]["rightOperand"][0]["itemId"]
    operator = operator_dict[single_condition["data"]['operator']]
    left_operand = single_condition["data"]["leftOperand"]

    if "answers" in single_response and left_operand["id"] in single_response["answers"]:
        answer_array = single_response["answers"][left_operand["id"]]
    else:
        print(False)
        return

    for answer in answer_array:
        if "rowId" not in left_operand:
            if operator == "ans":
                print(True)
                return
            else:
                left_operand = answer["text"]
                break

        elif left_operand["rowId"] == answer["rowId"]:
            if "colId" in left_operand and left_operand["colId"] == answer["colId"]:
                if operator == "ans":
                    print(True)
                    return
                else:
                    left_operand = answer["text"]
                    break
            elif "colId" not in left_operand:
                if operator == "ans":
                    print(True)
                    return
                else:
                    left_operand = answer["text"]
                    break

    left_operand = str(int(left_operand)) if (left_operand.isnumeric() and operator != " in ") else f" '{left_operand}' "
    right_operand = str(int(right_operand)) if (right_operand.isnumeric() and operator != " in ") else f" '{right_operand}' "

    if operator == " in ":
        print((f" {right_operand} {operator} {left_operand} "))
    else:
        print((f" {left_operand} {operator} {right_operand} "))

def handle_edata(single_condition, single_response):
    edata_dv_name = single_condition["data"]["leftOperand"]["id"]
    
    edata_field_arr = single_response["embedDataArr"]
    edata_dict = single_response["embedData"]

    if edata_dv_name in edata_field_arr:
        res_edata_val = edata_dict[edata_dv_name]
        edata_dv_value = single_condition["data"]["rightOperand"][0]["itemId"]
        operator = operator_dict[single_condition["data"]["operator"]]

        # if str isnumeric than converted to int to delete precedding 0
        res_edata_val = str(int(res_edata_val)) if res_edata_val.isnumeric() else f" '{res_edata_val}' "
        edata_dv_value = str(int(edata_dv_value)) if edata_dv_value.isnumeric() else f" '{edata_dv_value}' "

        return eval( f" {res_edata_val} {operator} {edata_dv_value} ")

def handle_logic_block(inner_condition, single_response, questions_collection):
    block_result = ""
    for single_condition in inner_condition:
        is_openended = True if "itemId" in single_condition["data"]["rightOperand"][0] else False
        is_edata = True if single_condition["data"]["fieldType"] == "edata" else None

        if is_edata:
            block_result += f" {handle_edata(single_condition, single_response)} "
        elif is_openended:
            block_result += f" {handle_single_logic_open_ended(single_condition, single_response)} "
        else:
            block_result += f" {handle_single_logic_close_ended(single_condition, single_response)} "

        block_result += " " + single_condition["operator"] + " "

    else:
        block_result += " True "

    return eval(block_result)

def handle_logical(derived_variable, survey_responses, questions_collection):
    # Logical logic
    logical_logic = derived_variable["logicalLogic"]

    for single_response in survey_responses:
        # answers = survey["answers"]
        
        # else condition set to result 
        result = logical_logic[-1]["logicName"]

        for outer_condition in logical_logic[:-1]:
            inner_condition = outer_condition["condition"]
            if handle_logic_block(inner_condition, single_response, questions_collection):
                result = outer_condition["logicName"]
                break
        
        # print(result)