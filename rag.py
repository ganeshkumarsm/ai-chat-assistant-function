import json
import config
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from tools import restart_virtual_machine, stop_virtual_machine


# OpenAI client
client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_KEY,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)

# Search client
search_client = SearchClient(
    endpoint=config.SEARCH_ENDPOINT,
    index_name=config.SEARCH_INDEX,
    credential=AzureKeyCredential(config.SEARCH_KEY)
)


def retrieve_docs(question):

    results = search_client.search(
        search_text=question,
        top=3
    )

    docs = [r["content"] for r in results]

    return "\n".join(docs)


# Tool definition
tools = [
{
"type": "function",
"function": {
"name": "restart_virtual_machine",
"description": "Restart an Azure virtual machine",
"parameters": {
"type": "object",
"properties": {
"resource_group": {
"type": "string"
},
"vm_name": {
"type": "string"
}
},
"required": ["resource_group","vm_name"]
}
}
}

{
"type": "function",
"function": {
"name": "stop_virtual_machine",
"description": "Stop and deallocate an Azure virtual machine",
"parameters": {
"type": "object",
"properties": {
"resource_group": {
"type": "string"
},
"vm_name": {
"type": "string"
}
},
"required": ["resource_group", "vm_name"]
}
}
}
]

def ask(question):

    docs = retrieve_docs(question)

    messages = [
        {
            "role": "system",
            "content": "You are an Azure infrastructure assistant."
        },
        {
            "role": "user",
            "content": f"""
Use the documentation below to answer the question.

Documentation:
{docs}

Question:
{question}
"""
        }
    ]

    response = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # If model decides to call tool
    if message.tool_calls:

        tool_call = message.tool_calls[0]

        if tool_call.function.name == "restart_virtual_machine":

            args = json.loads(tool_call.function.arguments)

            result = restart_virtual_machine(
                args["resource_group"],
                args["vm_name"]
            )

            messages.append(message)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            final = client.chat.completions.create(
                model=config.CHAT_MODEL,
                messages=messages
            )

            return final.choices[0].message.content
        elif tool_call.function.name == "stop_virtual_machine":

            args = json.loads(tool_call.function.arguments)

            result = stop_virtual_machine(
                args["resource_group"],
                args["vm_name"]
            )

            messages.append(message)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            final = client.chat.completions.create(
                model=config.CHAT_MODEL,
                messages=messages
            )

            return final.choices[0].message.content

    return message.content