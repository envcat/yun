from dataclasses import dataclass, field
from enum import StrEnum, auto

from rich.console import Console
from rich.text import Text


class MessageType(StrEnum):
    ERROR = auto()
    WARNING = auto()
    SUCCESS = auto()
    INFO = auto()


@dataclass
class MessageStyle:
    icon: str
    color: str


type Themes = dict[MessageType, MessageStyle]


def get_default_themes() -> Themes:
    return {
        MessageType.ERROR: MessageStyle("×", "red"),
        MessageType.WARNING: MessageStyle("⚠", "yellow"),
        MessageType.SUCCESS: MessageStyle("✓", "green"),
        MessageType.INFO: MessageStyle("ℹ", "blue"),
    }


@dataclass
class PrettyPrinter:
    themes: Themes = field(default_factory=get_default_themes)
    console: Console = field(default_factory=Console)

    def print(self, type: MessageType, message: str, details: str | list[str] | None = None):
        style = self.themes.get(type, MessageStyle("?", "white"))
        title = Text.assemble((style.icon, f"bold {style.color}"), (str(message), "bold white"))

        self.console.print(title)

        if not details:
            return

        if isinstance(details, str):
            details = [details]

        for detail in details:
            lines = str(detail).splitlines()
            for i, line in enumerate[str](lines):
                if i == 0:
                    prefix = " ╰─▶ "
                else:
                    prefix = " │   "

                detail_text = Text.assemble((prefix, style.color), (line, "default"))
                self.console.print(detail_text)

    def info(self, message: str, details: str | list[str] | None = None):
        self.print(MessageType.INFO, message, details)

    def success(self, message: str, details: str | list[str] | None = None):
        self.print(MessageType.SUCCESS, message, details)

    def warning(self, message: str, details: str | list[str] | None = None):
        self.print(MessageType.WARNING, message, details)

    def error(self, message: str, details: str | list[str] | None = None):
        self.print(MessageType.ERROR, message, details)
