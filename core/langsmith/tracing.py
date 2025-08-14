def enable_tracing(project_name: str):
    '''
    Enable tracing in LangSmith for the project. This should be placed in the entry point of the application in order to trace all calls to the agent.

    Args:
        project_name (str): The name of the project to trace. This will instantiate a new LangSmith project if it doesn't exist - otherwise it will use the existing project.
    '''
    if project_name is None:
        raise ValueError("Tracing project_name is required to enable tracing.")
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = project_name
    return
