import os


def get_prompt_file(script_dir, file_name):
    file_path = os.path.join(script_dir, "prompts", file_name)

    with open(file_path, "r") as file:
        return file.read()


def escape_curly_braces(query):
    return query.replace("{", "{{").replace("}", "}}")


def get_env_var(var_name):
    env_var = os.environ.get(var_name, None)
    if env_var is None:
        raise EnvironmentError(f'please set {var_name}')
    return env_var

