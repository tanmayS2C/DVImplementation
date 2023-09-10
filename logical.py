def handle_single_logic_close_ended(single_condition, answers):
    left_operand = single_condition["data"]["leftOperand"]
    right_operand_arr = single_condition["data"]["rightOperand"]
    operator = single_condition["data"]['operator']

    left_value = None
    right_arr = []


    if 'colId' in right_operand_arr[0]:
        for answer in answers[left_operand["id"]]:
            if answer["rowId"] == left_operand["rowId"]:
                left_value = answer["colId"]
                break

        right_arr = [ right_operand["colId"] for right_operand in right_operand_arr ]
    else:
        for answer in answers[left_operand["id"]]:
                left_value = answer["rowId"]
                break

        right_arr = [ right_operand["rowId"] for right_operand in right_operand_arr ]
    
    if operator == "eq": return left_value in right_arr
    else: return left_value not in right_arr


def handle_single_logic_open_ended(single_condition, answers):
    
    
    pass

def handle_logic_block(inner_condition, answers, questions_collection):
    block_result = ""
    for single_condition in inner_condition:
        openended = True if "itemId" in single_condition["data"]["rightOperand"][0] else False

        if openended:
            block_result += f" {handle_single_logic_open_ended(single_condition, answers)} "
        else:
            block_result += f" {handle_single_logic_close_ended(single_condition, answers)} "

        block_result += " " + single_condition["operator"] + " "

    else:
        block_result += " True "

    return eval(block_result)

def handle_logical(derived_variable, survey_responses, questions_collection):
    # Logical logic
    logical_logic = derived_variable["logicalLogic"]

    for survey in survey_responses:
        answers = survey["answers"]
        
        # else condition set to result 
        result = logical_logic[-1]["logicName"]

        for outer_condition in logical_logic[:-1]:
            inner_condition = outer_condition["condition"]
            if handle_logic_block(inner_condition, answers, questions_collection):
                result = outer_condition["logicName"]
                break
        
        print(result)