"""Terminal reporting utilities and tabular output formatting."""

from typing import List, Optional


def render_table(
    headers: List[str],
    rows: List[List[str]],
    title: Optional[str] = None,
    padding: int = 2,
) -> str:
    """
    Renders a formatted ASCII table with headers, separators, and dynamic column widths.
    """
    if not headers and not rows:
        return ""

    num_cols = len(headers) if headers else max(len(r) for r in rows)

    # Normalize rows
    norm_rows = []
    for r in rows:
        row_copy = [str(cell) for cell in r]
        while len(row_copy) < num_cols:
            row_copy.append("")
        norm_rows.append(row_copy[:num_cols])

    # Compute column widths
    widths = [len(str(h)) for h in headers] if headers else [0] * num_cols
    for row in norm_rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    col_widths = [w + padding for w in widths]

    lines = []
    total_width = sum(col_widths) + (num_cols - 1)

    if title:
        lines.append("=" * total_width)
        lines.append(f"  {title}".ljust(total_width))
        lines.append("=" * total_width)

    # Format header
    if headers:
        header_line = " ".join(
            headers[i].ljust(col_widths[i]) for i in range(num_cols)
        )
        lines.append(header_line)
        sep_line = " ".join("-" * (col_widths[i] - padding + 1) for i in range(num_cols))
        lines.append(sep_line)

    # Format data rows
    for row in norm_rows:
        row_str = " ".join(row[i].ljust(col_widths[i]) for i in range(num_cols))
        lines.append(row_str)

    return "\n".join(lines)


def format_status_badge(status: str) -> str:
    """Returns standardized status badge."""
    upper = status.upper()
    if upper in ("PASS", "OK", "SUCCESS", "READY"):
        return "[PASS]"
    elif upper in ("FAIL", "ERROR", "BROKEN"):
        return "[FAIL]"
    elif upper in ("WARN", "WARNING", "PARTIAL"):
        return "[WARN]"
    elif upper in ("INFO", "SKIP"):
        return "[INFO]"
    return f"[{upper}]"

