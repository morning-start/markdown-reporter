from pathlib import Path
from typing import Any


class MarkdownReporter:
    def __init__(self, use_section_number: bool = False):
        self.lines: list[str] = []
        self._write = self._write_line
        self.use_section_number = use_section_number
        self._min_level = 2
        self._max_level = 6
        self._counters: dict[int, int] = {
            i: 0 for i in range(self._min_level, self._max_level + 1)
        }

    def _write_line(self, line: str = "") -> None:
        self.lines.append(line)
        try:
            print(line)
        except UnicodeEncodeError:
            print(line.encode("ascii", "replace").decode("ascii"))

    def _reset_counters_below(self, level: int) -> None:
        for i in range(level, self._max_level + 1):
            self._counters[i] = 0

    def _get_section_number(self, level: int) -> str:
        if level < self._min_level or level > self._max_level:
            return ""
        self._counters[level] += 1
        self._reset_counters_below(level + 1)
        prefix = ".".join(
            str(self._counters[i]) for i in range(self._min_level, level + 1)
        )
        return f"{prefix} "

    def _write_table_row(self, cells: list[Any]) -> None:
        self._write("| " + " | ".join(str(c) for c in cells) + " |")

    def _format_x_label(self, v: Any) -> str:
        s = str(v)
        if s.isdigit():
            return s
        return f'"{s}"'

    def h1(self, text: str) -> None:
        self._write(f"\n# {text}\n")

    def h2(self, text: str) -> None:
        prefix = self._get_section_number(2) if self.use_section_number else ""
        self._write(f"\n## {prefix}{text}\n")

    def h3(self, text: str) -> None:
        prefix = self._get_section_number(3) if self.use_section_number else ""
        self._write(f"\n### {prefix}{text}\n")

    def h4(self, text: str) -> None:
        prefix = self._get_section_number(4) if self.use_section_number else ""
        self._write(f"\n#### {prefix}{text}\n")

    def h5(self, text: str) -> None:
        prefix = self._get_section_number(5) if self.use_section_number else ""
        self._write(f"\n##### {prefix}{text}\n")

    def h6(self, text: str) -> None:
        prefix = self._get_section_number(6) if self.use_section_number else ""
        self._write(f"\n###### {prefix}{text}\n")

    def p(self, text: str) -> None:
        self._write(text)

    def hyperlink(self, text: str, url: str) -> None:
        self._write(f"[{text}]({url})")

    def image(self, alt_text: str, url: str) -> None:
        self._write(f"![{alt_text}]({url})")

    def bold(self, content: str) -> str:
        return f"**{content}**"

    def italic(self, content: str) -> str:
        return f"*{content}*"

    def blockquote(self, text: str) -> None:
        for line in text.split("\n"):
            self._write(f"> {line}")

    def horizontal_rule(self) -> None:
        self._write("\n---\n")

    def bullet(self, text: str) -> None:
        self._write(f"- {text}")

    def ul(self, items: list[Any], level: int = 1) -> None:
        for item in items:
            self._write(f"{'  ' * (level - 1)}- {str(item)}")

    def ol(self, items: list[Any]) -> None:
        for index, item in enumerate(items, start=1):
            self._write(f"{index}. {str(item)}")

    def task_list(self, items: list[tuple[str, bool]]) -> None:
        for text, checked in items:
            status = "x" if checked else " "
            self._write(f"- [{status}] {text}")

    def nested_list_from_dict(self, d: dict[str, Any]) -> None:
        def _add_items(d: dict[str, Any], level: int) -> None:
            for key, value in d.items():
                self._write(f"{'  ' * (level - 1)}- {str(key)}")
                if isinstance(value, dict):
                    _add_items(value, level + 1)
                elif isinstance(value, list):
                    for item in value:
                        self._write(f"{'  ' * level}- {str(item)}")
                else:
                    self._write(f"{'  ' * level}- {str(value)}")

        _add_items(d, 1)

    def table(self, headers: list[Any], rows: list[list[Any]]) -> None:
        self._write_table_row(headers)
        self._write_table_row(["---"] * len(headers))
        for row in rows:
            self._write_table_row(row)
        self._write("")

    def table_from_pandas(self, df: Any, index: bool = False) -> None:
        table = df.to_markdown(index=index) + "\n"
        for line in table.split("\n"):
            self._write(line)

    def code_block(self, text: str, lang: str = "", remove_indent: int = 0) -> None:
        if remove_indent:
            text = "\n".join(line[remove_indent:] for line in text.split("\n"))
        self._write(f"```{lang}\n{text.strip()}\n```")

    def mermaid(self, chart_type: str, data: dict[str, Any], title: str = "") -> None:
        self._write("\n```mermaid")
        if chart_type == "pie":
            self._write("pie showData")
            self._write(f'    title "{title}"' if title else '    title ""')
            for label, value in data.get("labels", []):
                self._write(f'    "{label}" : {value}')
        elif chart_type == "xy-horizontal":
            self._write("xychart-beta horizontal")
            self._write(f'    title "{data.get("title", "")}"')
            x_labels = data.get("x_labels", [])
            self._write(
                f"    x-axis [{', '.join(self._format_x_label(v) for v in x_labels)}]"
            )
            self._write(f'    y-axis "{data.get("y_axis", "")}"')
            self._write(
                f"    bar [{', '.join(str(v) for v in data.get('values', []))}]"
            )
        elif chart_type == "xy-vertical":
            self._write("xychart-beta")
            self._write(f'    title "{data.get("title", "")}"')
            x_labels = data.get("x_labels", [])
            self._write(
                f"    x-axis [{', '.join(self._format_x_label(v) for v in x_labels)}]"
            )
            self._write(f'    y-axis "{data.get("y_axis", "")}"')
            self._write(
                f"    bar [{', '.join(str(v) for v in data.get('values', []))}]"
            )
        self._write("```\n")

    def save(self, path: Path | str) -> "MarkdownReporter":
        if isinstance(path, str):
            path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.lines), encoding="utf-8")
        return self

    def __enter__(self) -> "MarkdownReporter":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def reset(self) -> None:
        self.lines.clear()
        self._counters = {i: 0 for i in range(self._min_level, self._max_level + 1)}
