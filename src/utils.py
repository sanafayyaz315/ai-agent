# load template
def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

def get_tool_descriptions(tools):
    descriptions = []
    for name, func in tools.items():
        descriptions.append(f"{name}: {func.__doc__.strip()}")  
    descriptions = ", ".join(descriptions)

    return descriptions



