import yaml

def load_settings(file):
    with open(file) as f:
        templates = yaml.safe_load(f)
    return templates


def save_settings(file, data):
    with open(file, 'w') as f:
        yaml.dump(data, f)

data = {(1, False): "text"}



kt = (0, 1, False)
a = [str(x) for x in kt]
key = ", ".join(a)

m = load_settings("1_contact.yaml")['garry']
print(m)



