import yaml

def get_config(file_name = "config.yaml"):
    with open(file_name, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def clear_file(file_name):
    try:
        file = open(file_name, 'w')
        file.write('')
    finally:
        file.close()