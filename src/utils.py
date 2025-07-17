# load template
def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text