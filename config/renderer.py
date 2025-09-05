import html
import re

def md_to_html(text: str) -> str:
    # Conversión Markdown mínima para ligereza y robustez
    # Soporte: #, ##, ###, **bold**, *italic*, listas -, numeradas 1., líneas en blanco
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = t.split("\n")
    out = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close_lists()
            out.append("<br>")
            continue
        if line.startswith("### "):
            close_lists()
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            close_lists()
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
            continue
        if line.startswith("# "):
            close_lists()
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
            continue
        if re.match(r"^\s*-\s+", line):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            item = re.sub(r"^\s*-\s+", "", line)
            out.append(f"<li>{inline_format(item)}</li>")
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\s*\d+\.\s+", "", line)
            out.append(f"<li>{inline_format(item)}</li>")
            continue
        # párrafo plano
        close_lists()
        out.append(f"<p>{inline_format(line)}</p>")

    close_lists()

    style = """
    <style>
    body { background: #1c1c21; color: #e6e6eb; font-family: Segoe UI, Inter, system-ui, -apple-system, sans-serif; line-height: 1.5; }
    h1, h2, h3 { color: #ffffff; margin: 0.4em 0 0.2em; }
    p { margin: 0.3em 0; }
    ul, ol { margin: 0.2em 0 0.4em 1.2em; }
    li { margin: 0.15em 0; }
    strong { color: #ffffff; }
    em { color: #d7d7de; }
    code { background: #2a2a31; padding: 2px 4px; border-radius: 4px; }
    </style>
    """
    return f"<!doctype html><html><head><meta charset='utf-8'>{style}</head><body>" + "\n".join(out) + "</body></html>"

def inline_format(s: str) -> str:
    s = html.escape(s)
    # **bold**
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    # *italic*
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    # `code`
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s
