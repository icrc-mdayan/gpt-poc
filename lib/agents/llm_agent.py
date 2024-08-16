from abc import ABC
from openai import OpenAI

class LLMAgent(ABC):
    def __init__(self, agent_name: str, model_name: str, system_prompt: str, total_text_conversation: str) -> None:
        """
        Initializes the ConversableAgent with a agent name, model name, system prompt.
        """
        super().__init__()
        self.agent_name = agent_name
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.total_text_conversation = total_text_conversation

    def generate_response(self, message) -> str:
        """
        Generate a response to the request message, using the model name.
        """
        client = OpenAI(base_url="http://104.171.203.227:8000/v1", api_key="EMPTY")

        # default values
        temperature = 0.6
        top_p = 0.9
        max_tokens = 1024

        # print("----- Message -----")
        # prompt_text = ""
        # for m in message:
        #     role = m["role"].capitalize()
        #     content = m["content"]
        #     prompt_text += f"{role}:\n{content}\n"
        # print(prompt_text)
        # print("------------------")

        self.total_text_conversation += message[0]["content"]

        response = client.chat.completions.create(
            model=self.model_name,
            messages=message, 
            temperature=temperature, 
            top_p=top_p,
            max_tokens=max_tokens
        )
        self.total_text_conversation += response.choices[0].message.content

        return response.choices[0].message.content, self.total_text_conversation
    
    def prepare_prompt(self, user_prompt_input: str, patient_description: str) -> str:
        """
        Prepare the prompt for the model.
        """

        if patient_description:
            system_prompt_content = self.system_prompt + "Here are the information about the patient so far:\n" + patient_description
        
        if user_prompt_input is not None:
            prompt = [{"role": "system", "content": system_prompt_content}] + [{"role": "user", "content": user_prompt_input}]
        else:
            prompt = [{"role": "system", "content": system_prompt_content}]

        # print("----- Prompt -----")
        # prompt_text = ""
        # for message in prompt:
        #     role = message["role"].capitalize()
        #     content = message["content"]
        #     prompt_text += f"{role}:\n{content}\n\n"
        # print(prompt_text)
        # print("------------------")

        return prompt