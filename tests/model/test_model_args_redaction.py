from inspect_ai._util.registry import registry_value
from inspect_ai.model import get_model
from inspect_ai.model._model_config import model_args_for_log


def test_model_args_for_log_redacts_credentials() -> None:
    assert model_args_for_log(
        {
            "api_key": "sk-secret",
            "access_token": "ya29.secret",
            "aws_secret_access_key": "secret",
            "project": "my-project",
        }
    ) == {"project": "my-project"}


def test_model_args_for_log_leaves_caller_dict_intact() -> None:
    model_args = {"api_key": "sk-secret", "project": "my-project"}
    model_args_for_log(model_args)
    assert model_args == {"api_key": "sk-secret", "project": "my-project"}


def test_registry_value_redacts_model_args() -> None:
    """A Model passed as a task/solver/scorer parameter is recorded in the log."""
    model = get_model("mockllm/model")
    model.model_args = {"access_token": "ya29.secret", "project": "my-project"}
    value = registry_value(model)
    assert value["model_args"] == {"project": "my-project"}
