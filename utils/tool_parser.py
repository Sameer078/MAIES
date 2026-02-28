import json
import ast

def extract_tool_results(data_list):
    """
    Takes a list of dictionaries.
    Returns a list of dictionaries containing 'name' and parsed 'content'
    from entries where role == 'tool'.
    """
    result = []
    for item in data_list:
        if isinstance(item, dict) and item.get("role") == "tool":
            print(item.get("content"),type(item.get("content")))
            content_str = item.get("content")
            content_dict = ast.literal_eval(content_str)
            extracted = {
                "name": item.get("name"),
                "content": content_dict
            }
            result.append(extracted)
    return result

def extract_outer_json(text):
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1 or end <= start:
        return None
    return json.loads(text[start:end+1])