from dotenv  import load_dotenv
from agents import Agent, Runner


load_dotenv()


spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the users message to spanish."
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the users message to French."
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
)


result =  Runner.run_sync(orchestrator_agent, input="Say, Hello, How are you? in Spanish.")
print(result.raw_responses)
print(result.final_output)
