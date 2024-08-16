import yaml

def construct_prompt(conversation_mode):

    if conversation_mode == 'patient':

        with open("prompts/conversation/config_prompts_patient.yaml", "r") as file:
            yaml_content = yaml.safe_load(file)

        with open("prompts/conversation/patient_description.txt", "r") as file:
            patient_description = file.read().strip()

        with open("prompts/conversation/fewshot_conversation.txt", "r") as file:
            conversation_examples = file.read().strip()

        skeleton_text = f"""
    ## Constitution
    {yaml_content['constitution'].strip()}

    ## Goal
    {yaml_content['goal'].strip()}

    ## Safety
    {yaml_content['safety'].strip()}

    ## Formatting rules
    {yaml_content['formatting_rules'].strip()}

    ## Patient information so far
    ADDITIONAL_INFORMATION
"""
 
    else:
        with open("prompts/conversation/config_prompts_general.yaml", "r") as file:
            yaml_content = yaml.safe_load(file)

        skeleton_text = f"""
## Constitution
    {yaml_content['constitution'].strip()}

## Safety
    {yaml_content['safety'].strip()}

## Formatting rules
    {yaml_content['formatting_rules'].strip()}
    """ 
        
    with open("skeleton_filled.txt", "w") as file:
            file.write(skeleton_text.strip())
        
    # print("Skeleton filled and saved to 'skeleton_filled.txt' ::: ")
    
    return skeleton_text


# ## Conversation Examples
# {conversation_examples}

# ## Current patient description
# {patient_description}