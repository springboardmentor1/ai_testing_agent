# test_parser.py
from graph.graph_builder import parser_graph

input_text = "open Google and search for amazon"

result = parser_graph.invoke({
    "user_input": input_text
})

print(result)
