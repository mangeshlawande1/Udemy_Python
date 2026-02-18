from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json
import shutil


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def get_weather(city: str):
    url = f"http://wttr.in{city}?format=%C+%t"
    response = requests.get(url)
    return (
        f"The weather in {city} is {response.text}."
        if response.status_code == 200
        else "Error"
    )


def run_command(cmd: str):
    result = os.system(cmd)
    return result


def create_file(input: str) -> str:
    """
    input format (JSON string) :{"path": "file.txt", "content":"hello World!!" }
    create a new file with the given content . Fails if file already exists.
    """
    try:
        data = json.loads(input)
        path = data["path"]
        content = data.get("content", "")
        if os.path.exists(path):
            return f"error:file '{path}' already exists. Use update file to modify it."
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(
            path
        ) else None
        with open(path, "w", endcoding="utf-8") as f:
            f.write(content)
        return f"file '{path}' created successfully."
    except Exception as e:
        return f"Error creating file: {str(e)}"


def read_file(path: str) -> str:
    """Reads and returns the contents of the specified file."""

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"content of '{path}' :\n {content}"
    except FileNotFoundError:
        return f"Error: file '{path}' not found."
    except Exception as e:
        return e


def update_file(path: str) -> str:
    """input format (JSON sting): {"path": 'file.txt' , 'content': "new content", 'mode':'overwrite'|'append' }
    Updates an existing file by overwriting or appending content.
    """

    try:
        data = json.loads(input)
        path = data["path"]
        content = data.get("content", "")
        mode = data.get("mode", "overwrite")
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist. Use create_file to create it."
        write_mode = "a" if mode == "append" else "w"
        with open(path, write_mode, encoding="utf-8") as f:
            f.write(content)
        action = "appended to" if mode == "append" else "overwritten"
        return f"File '{path}' {action} successfully."
    except Exception as e:
        return f"Error updating file: {str(e)}"


def delete_file(path: str) -> str:
    """Deletes the specified file or empty directory."""
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"File '{path}' deleted successfully."
        elif os.path.isdir(path):
            os.rmdir(path)
            return f"Directory '{path}' deleted successfully."
        else:
            return f"Error: '{path}' does not exist."
    except OSError as e:
        return f"Error deleting '{path}': {str(e)}"


def list_directory(path: str = ".") -> str:
    """Lists all files and folders in the given directory path."""
    try:
        entries = os.listdir(path)
        if not entries:
            return f"Directory '{path}' is empty."
        result = []
        for entry in sorted(entries):
            full = os.path.join(path, entry)
            kind = "DIR " if os.path.isdir(full) else "FILE"
            size = os.path.getsize(full) if os.path.isfile(full) else "-"
            result.append(
                f"[{kind}] {entry}  ({size} bytes)"
                if kind == "FILE"
                else f"[{kind}] {entry}/"
            )
        return f"Contents of '{path}':\n" + "\n".join(result)
    except FileNotFoundError:
        return f"Error: Directory '{path}' not found."
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def copy_file(input: str) -> str:
    """
    input format (JSON string): {"src": "source.txt", "dst": "destination.txt"}
    Copies a file from src to dst.
    """
    try:
        data = json.loads(input)
        src, dst = data["src"], data["dst"]
        shutil.copy2(src, dst)
        return f"File copied from '{src}' to '{dst}' successfully."
    except FileNotFoundError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error copying file: {str(e)}"


def move_file(input: str) -> str:
    """
    input format (JSON string): {"src": "source.txt", "dst": "destination.txt"}
    Moves/renames a file from src to dst.
    """
    try:
        data = json.loads(input)
        src, dst = data["src"], data["dst"]
        shutil.move(src, dst)
        return f"File moved from '{src}' to '{dst}' successfully."
    except FileNotFoundError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error moving file: {str(e)}"


def file_exists(path: str) -> str:
    """Checks whether a file or directory exists at the given path."""
    if os.path.isfile(path):
        size = os.path.getsize(path)
        return f"'{path}' exists as a FILE ({size} bytes)."
    elif os.path.isdir(path):
        return f"'{path}' exists as a DIRECTORY."
    else:
        return f"'{path}' does NOT exist."


# ── Tool Registry ──────────────────────────────────────────────────────────────

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "create_file": create_file,
    "read_file": read_file,
    "update_file": update_file,
    "delete_file": delete_file,
    "list_directory": list_directory,
    "copy_file": copy_file,
    "move_file": move_file,
    "file_exists": file_exists,
}


SYSTEM_PROMPT = """
        You are an expert of AI Assistant in resolving user queries using chain of thought.
        You work on START, PLAN OUTPUT steps.
        You need to PLAN what needs to be done. The plan can be multiple steps.
        Once you think enough PLAN has been done , finally you can give an OUTPUT.
        You can also call a tool required from the list of available tools.
        For every tool call wait for observe step which is output from the called tool.

        Rules :
            - Strictly follow the given JSON OUTPUT format
            - only run one step at a time .
            - The sequence of steps START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (Which is going to be displayed to the user).
            - For file tools that accept JSON input, always pass a valid JSON string as the "input" field.

        OUTPUT JSON Format :
            { "step": "START" | "PLAN" | "OUTPUT" | "TOOL" , "content":"string", "tool":"string","input":"string" }

        Available Tools :
            - get_weather(city:str): Takes city name as input and returns weather information about the city.
            - run_command(cmd:str): Takes a Linux shell command as string, executes it and returns the output.

            FILE HANDLING TOOLS:
            - create_file(input:str): Creates a new file. Input is JSON: {"path": "file.txt", "content": "text here"}
            - read_file(path:str): Reads and returns the full content of a file. Input is the file path string.
            - update_file(input:str): Updates an existing file. Input is JSON: {"path": "file.txt", "content": "new text", "mode": "overwrite"|"append"}
            - delete_file(path:str): Deletes a file or empty directory. Input is the file/dir path string.
            - list_directory(path:str): Lists all files and folders in a directory. Input is the directory path (default ".").
            - copy_file(input:str): Copies a file. Input is JSON: {"src": "source.txt", "dst": "destination.txt"}
            - move_file(input:str): Moves or renames a file. Input is JSON: {"src": "old.txt", "dst": "new.txt"}
            - file_exists(path:str): Checks if a file or directory exists. Input is the path string.

        Example 1 :
        START : "Hey can you write a code to solve 2 + 3 * 5 /10"
        PLAN : {"step":"PLAN", "content": "Seems like user is interested in math problems."}
        PLAN : {"step":"PLAN", "content": "Looking at the problems, we should solve this using BODMAS method."}
        PLAN : {"step":"PLAN", "content": "First we multiply 3*5 which is 15."}
        PLAN : {"step":"PLAN", "content": "Now the new equation becomes 2 + 15 / 10"}
        PLAN : {"step":"PLAN", "content": "Must perform divide 15 / 10 = 1.5."}
        PLAN : {"step":"PLAN", "content": "Now the new equation is 2 + 1.5 = 3.5"}
        OUTPUT: {"step":"OUTPUT", "content": "3.5"}

        Example 2 :
        START : "What is the weather of Delhi?"
        PLAN : {"step":"PLAN", "content": "Seems like user is interested in getting weather of delhi in india."}
        PLAN : {"step":"PLAN", "content": "Yes we have get_weather tool available for this query."}
        TOOL : {"step":"TOOL", "tool":"get_weather", "input": "delhi"}
        OBSERVE : {"step":"OBSERVE", "tool": "get_weather", "content":"the temp of delhi is cloudy with 20 C." }
        PLAN : {"step":"PLAN", "content": "Great, I got the weather info about Delhi."}
        OUTPUT: {"step":"OUTPUT", "content": "The Current weather in Delhi is 20 C with some Cloudy Sky."}

        Example 3 :
        START : "Create a file called notes.txt with content 'Buy groceries'"
        PLAN : {"step":"PLAN", "content": "User wants to create a file named notes.txt with specific content."}
        PLAN : {"step":"PLAN", "content": "I will use the create_file tool with path and content as JSON."}
        TOOL : {"step":"TOOL", "tool":"create_file", "input": "{\"path\": \"notes.txt\", \"content\": \"Buy groceries\"}"}
        OBSERVE : {"step":"OBSERVE", "tool": "create_file", "content":"File 'notes.txt' created successfully." }
        OUTPUT: {"step":"OUTPUT", "content": "Done! I've created 'notes.txt' with the content 'Buy groceries'."}

    """


message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]
print("\n")


while True:
    # Start the conversation with the user query
    user_input = input("==> ")
    message_history.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gemini-3-flash-preview",
            response_format={"type": "json_object"},
            messages=message_history,
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        parsed_result = json.loads(raw_result)

        if isinstance(parsed_result, list):
            parsed_result = parsed_result[0]

        step = parsed_result.get("step")
        content = parsed_result.get("content")

        if step == "START":
            print("\n start LLM Loop: ", content)
            continue

        if step == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f" 🔧 {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            message_history.append(
                {
                    "role": "developer",
                    "content": json.dumps(
                        {
                            "step": "OBSERVE",
                            "tool": tool_to_call,
                            "input": tool_input,
                            "output": tool_response,
                        }
                    ),
                }
            )

        if step == "PLAN":
            print("\nPlanning 🧠:: ", content)
            continue

        if step == "OUTPUT":
            print("\nLLM 🤖: ", content)
            break
