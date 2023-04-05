import yaml

def load_settings(file):
    with open(file) as f:
        templates = yaml.safe_load(f)
    return templates

def save_settings(file, data):
    with open(file, 'w') as f:
        yaml.dump(data, f)