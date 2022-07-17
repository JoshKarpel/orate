from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import ContextManager, Type

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from spiel.constants import DECK, OPTIONS
from spiel.deck import Deck
from spiel.exceptions import NoDeckFound
from spiel.options import Options


def load_deck_and_options(path: Path) -> tuple[Deck, Options]:
    module_name = "__deck"
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None:
        raise FileNotFoundError(
            f"{path.resolve()} does not appear to be an importable Python module."
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)

    try:
        deck = getattr(module, DECK)
    except AttributeError:
        raise NoDeckFound(f"The module at {path} does not have an attribute named {DECK}.")

    if not isinstance(deck, Deck):
        raise NoDeckFound(
            f"The module at {path} has an attribute named {DECK}, but it is a {type(deck).__name__}, not a {Deck.__name__}."
        )

    options = getattr(module, OPTIONS, Options())

    if not isinstance(options, Options):
        options = Options()

    return deck, options


@dataclass
class DeckWatcher(ContextManager["DeckWatcher"]):
    event_handler: FileSystemEventHandler
    path: Path
    poll: bool = False

    def __post_init__(self) -> None:
        self.observer = (PollingObserver if self.poll else Observer)(timeout=0.1)

    def __enter__(self) -> DeckWatcher:
        self.observer.schedule(self.event_handler, str(self.path))
        self.observer.start()

        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.observer.stop()
        self.observer.join()

        return None
