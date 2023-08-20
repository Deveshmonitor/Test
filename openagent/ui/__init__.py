import asyncio
import os
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from dotenv import load_dotenv
from starlette.datastructures import Headers

if TYPE_CHECKING:
    from openagent.ui.client.base import BaseDBClient, BaseAuthClient, UserDict

import openagent.ui.input_widget as input_widget
from openagent.ui.action import Action
from openagent.ui.cache import cache
from openagent.ui.chat_settings import ChatSettings
from openagent.ui.config import config
from openagent.ui.element import (
    Audio,
    Avatar,
    File,
    Image,
    Pdf,
    Pyplot,
    Task,
    TaskList,
    TaskStatus,
    Text,
    Video,
)
from openagent.ui.haystack import HAYSTACK_INSTALLED
from openagent.ui.lc import LANGCHAIN_INSTALLED
from openagent.ui.llama_index import LLAMA_INDEX_INSTALLED
from openagent.ui.logger import logger
from openagent.ui.message import AskFileMessage, AskUserMessage, ErrorMessage, Message
from openagent.ui.sync import make_async, run_sync
from openagent.ui.telemetry import trace
from openagent.ui.types import LLMSettings
from openagent.ui.user_session import user_session
from openagent.ui.utils import wrap_user_function
from openagent.ui.version import __version__

if LANGCHAIN_INSTALLED:
    from openagent.ui.lc.callbacks import (
        AsyncLangchainCallbackHandler,
        LangchainCallbackHandler,
    )

if LLAMA_INDEX_INSTALLED:
    from openagent.ui.llama_index.callbacks import LlamaIndexCallbackHandler

if HAYSTACK_INSTALLED:
    from openagent.ui.haystack.callbacks import HaystackAgentCallbackHandler

env_found = load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

if env_found:
    logger.info("Loaded .env file")


@trace
def on_message(func: Callable) -> Callable:
    """
    Framework agnostic decorator to react to messages coming from the UI.
    The decorated function is called every time a new message is received.

    Args:
        func (Callable[[str, str], Any]): The function to be called when a new message is received. Takes the input message and the message id.

    Returns:
        Callable[[str], Any]: The decorated on_message function.
    """

    config.code.on_message = wrap_user_function(func)
    return func


@trace
def on_chat_start(func: Callable) -> Callable:
    """
    Hook to react to the user websocket connection event.

    Args:
        func (Callable[], Any]): The connection hook to execute.

    Returns:
        Callable[], Any]: The decorated hook.
    """

    config.code.on_chat_start = wrap_user_function(func, with_task=True)
    return func


@trace
def author_rename(func: Callable[[str], str]) -> Callable[[str], str]:
    """
    Useful to rename the author of message to display more friendly author names in the UI.
    Args:
        func (Callable[[str], str]): The function to be called to rename an author. Takes the original author name as parameter.

    Returns:
        Callable[[Any, str], Any]: The decorated function.
    """

    config.code.author_rename = wrap_user_function(func)
    return func


@trace
def on_stop(func: Callable) -> Callable:
    """
    Hook to react to the user stopping a conversation.

    Args:
        func (Callable[[], Any]): The stop hook to execute.

    Returns:
        Callable[[], Any]: The decorated stop hook.
    """

    config.code.on_stop = wrap_user_function(func)
    return func


def action_callback(name: str) -> Callable:
    """
    Callback to call when an action is clicked in the UI.

    Args:
        func (Callable[[Action], Any]): The action callback to execute. First parameter is the action.
    """

    def decorator(func: Callable[[Action], Any]):
        config.code.action_callbacks[name] = wrap_user_function(func, with_task=True)
        return func

    return decorator


def on_settings_update(
    func: Callable[[Dict[str, Any]], Any]
) -> Callable[[Dict[str, Any]], Any]:
    """
    Hook to react to the user changing any settings.

    Args:
        func (Callable[], Any]): The hook to execute after settings were changed.

    Returns:
        Callable[], Any]: The decorated hook.
    """

    config.code.on_settings_update = wrap_user_function(func, with_task=True)
    return func


@trace
def auth_client_factory(
    func: Callable[[Optional[Dict[str, str]], Optional[Headers]], "BaseAuthClient"]
) -> Callable[[Optional[Dict[str, str]], Optional[Headers]], "BaseAuthClient"]:
    """
    Callback to call when to initialize the custom client.

    Args:
        func (Callable[[Optional[UserDict]], BaseDBClient]): The action callback to execute. First parameter is the headers, second is the user infos if cloud auth is enabled.
    """

    config.code.auth_client_factory = wrap_user_function(func, with_task=False)
    return func


@trace
def db_client_factory(
    func: Callable[
        [Optional[Dict[str, str]], Optional[Headers], Optional["UserDict"]],
        "BaseDBClient",
    ]
) -> Callable[
    [Optional[Dict[str, str]], Optional[Headers], Optional["UserDict"]], "BaseDBClient"
]:
    """
    Callback to call when to initialize the custom client.

    Args:
        func (Callable[[Optional[UserDict]], BaseDBClient]): The action callback to execute. First parameter is the headers, second is the user infos if cloud auth is enabled.
    """

    config.code.db_client_factory = wrap_user_function(func, with_task=False)
    return func


def sleep(duration: int):
    """
    Sleep for a given duration.
    Args:
        duration (int): The duration in seconds.
    """
    return asyncio.sleep(duration)


__all__ = [
    "user_session",
    "LLMSettings",
    "Action",
    "Audio",
    "Pdf",
    "Image",
    "Text",
    "Avatar",
    "Pyplot",
    "File",
    "Task",
    "TaskList",
    "TaskStatus",
    "Video",
    "ChatSettings",
    "input_widget",
    "Message",
    "ErrorMessage",
    "AskUserMessage",
    "AskFileMessage",
    "on_chat_start",
    "on_stop",
    "action_callback",
    "author_rename",
    "on_settings_update",
    "sleep",
    "LangchainCallbackHandler",
    "AsyncLangchainCallbackHandler",
    "LlamaIndexCallbackHandler",
    "auth_client_factory",
    "db_client_factory",
    "HaystackAgentCallbackHandler",
    "run_sync",
    "make_async",
    "cache",
]
