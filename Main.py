import os
import speech_recognition as sr
import pyttsx3
import openai

# File paths
prompt_file_1 = "prompt_1.txt"
response_file_1 = "response_1.txt"
response_file_2 = "Executer_1.py"

# Memory content for current session
memory_content = ""

def read_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def write_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def CallOpenAPI(prompt, system_prompt):
    # Adding memory to the conversation
    messages = [
        {"role": "system", "content": system_prompt},  # Corrected role from "assistant" to "system"
        {"role": "assistant", "content": memory_content},
        {"role": "user", "content": prompt}
    ]
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",  # Fixed typo in model name (was "gpt-4o")
            temperature=1,
            max_tokens=1000,
            messages=messages
        )
        response = completion.choices[0].message['content']  # Correct indexing for response
        return response
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Error: Unable to process the request."


def remove_python_comments(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if lines[0].strip() == "```python" and lines[-1].strip() == "```":
            del lines[0]
            del lines[-1]

        with open(file_path, 'w') as file:
            file.writelines(lines)
        return True
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return False
    except IndexError:
        print(" ")

def update_memory(new_content):
    global memory_content
    memory_content += new_content + "\n"  # Changed "\\n" to "\n" for better readability

def delete_content(file_path):
    with open(file_path, 'w') as file:
        file.truncate(0)
    print(f"Content of {file_path} has been deleted.")

def SaveToforcode(fro, to):
    with open(fro, 'r') as source_file:
        lines = source_file.readlines()
    if lines and lines[0].strip() == "command=code":
        lines.pop(0)  # Remove the first line if it’s "command=code"
        with open(to, 'w') as dest_file:
            dest_file.writelines(lines)
        print("File copied successfully!")

def readfile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        if lines and lines[0].strip() == "command=response":
            for line in lines[1:]:
                print(line.strip())

def GenerateContent(prompt):
    delete_content(response_file_1)
    delete_content(response_file_2)
    system_prompt = read_file_content(prompt_file_1)
    response = CallOpenAPI(prompt, system_prompt)
    write_to_file(response_file_1, response)
    SaveToforcode(response_file_1, response_file_2)
    remove_python_comments(response_file_2)
    # Update memory with the response for this session
    update_memory(f"User prompt: {prompt}\nAssistant response: {response}")

# Execution flow
usage = input("Debug or User?: ")
while usage == "user":
    prompt = input("Enter prompt: ")
    if prompt == "exit":
        exit()
    else:
        GenerateContent(prompt)
    readfile(response_file_1)
    os.system('python ' + response_file_2)
