# from openai import OpenAI
# from defined_prompts import initial_assessment_prompt

# from setopenai import setupopenai
# setupopenai()

# # Initialize the OpenAI client
# client = OpenAI()
# print(client)

# # Define the system prompt content
# system_prompt = initial_assessment_prompt

# # Initialize conversation history with the system message
# conversation_history = [
#     {"role": "system", "content": system_prompt}
# ]

# # Function to send a request and update conversation history
# def send_request_and_update_history(client, conversation_history):
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=conversation_history
#     )
#     assistant_reply = completion.choices[0].message
#     conversation_history.append({"role": "assistant", "content": assistant_reply.content})
#     return assistant_reply.content

# # def assess_query(question_id, query):
# #     formatted_user_input = f"Question ID: {question_id}, Answer: {query}"
# #     conversation_history.append({"role": "user", "content": formatted_user_input})
# #     feedback = send_request_and_update_history(client, conversation_history)
# #     return feedback

# # example_question_id = 1
# # example_query = "SQL stands for Structured Query Language, and it's a programming language that allows users to communicate with and manipulate databases. "
# # feedback = assess_query(example_question_id, example_query)
# # print("Feedback:", feedback)

# def generate_feedback(question, answer):
#     # Format user input
#     formatted_user_input = f"Question: {question}\nAnswer: {answer}"
#     # Add user input to conversation history
#     conversation_history.append({"role": "user", "content": formatted_user_input})
#     # Send request to OpenAI and update conversation history
#     feedback = send_request_and_update_history(client, conversation_history)
#     return feedback

# example_question = "What is SQL?"
# example_answer = "SQL stands for Structured Query Language, and it's a programming language that allows users to communicate with and manipulate databases."
# feedback = generate_feedback(example_question, example_answer)
# print("Feedback:", feedback)

from openai import OpenAI
# from defined_prompts import initial_assessment_prompt

from setopenai import setupopenai
setupopenai()

# Initialize the OpenAI client
client = OpenAI()

# Define the system prompt content
# system_prompt = initial_assessment_prompt
def create_system_prompt(question, answer):
    # Create the system prompt using the question and answer
    system_prompt = f"Question: {question}\nAnswer: {answer}. Please go through the answer according to the question and provide a detailed feedback wether the answer is right or wrong."
    return system_prompt

# Initialize conversation history with the system messag
# Function to send a request and update conversation history
def send_request_and_update_history(client, prompt):
    conversation_history = [
    {"role": "system", "content": prompt}]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    assistant_reply = completion.choices[0].message.content  # Extract suggestions from assistant_reply if available
    print(assistant_reply)
    # if assistant_reply.suggestions:
    #     suggestions = assistant_reply.suggestions
    # conversation_history.append({"role": "assistant", "content": assistant_reply.content, "suggestions": suggestions})
    return assistant_reply


def assess_query(prompt):
    feedback = send_request_and_update_history(client, prompt)
    return feedback



# Example usage
example_question = "Give the names of employees who are working in the 'Sales' department."
example_query = "SELECT * FROM employees WHERE department_name = 'Sales';"
prompt= create_system_prompt(example_question, example_query)
feedback = assess_query(prompt)
print("Feedback:", feedback)
