"""Project pipelines."""
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

def register_pipelines():
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())   # eda + data_science razem
    return pipelines
