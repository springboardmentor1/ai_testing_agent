import json
from app.agents.instruction_parser_graph import instruction_parser_agent

result = instruction_parser_agent.invoke({
    "input": "open Google and search for Amazon"
})

print(json.dumps(result, indent=2))
