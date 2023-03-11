import htmlmin
import json
import re
from datetime import datetime, timezone
from jinja2 import Template, pass_eval_context
from markupsafe import Markup, escape
from jinja2.defaults import DEFAULT_FILTERS

with open("template.html", "r") as f:
    template_content = f.read()
with open("messages.json", "r") as f:
    data = json.load(f)


@pass_eval_context
def nl2br(eval_ctx, value):
    br = "<br>\n"

    if eval_ctx.autoescape:
        value = escape(value)
        br = Markup(br)

    result = "\n\n".join(
        f"<p>{br.join(p.splitlines())}</p>"
        for p in re.split(r"(?:\r\n|\r(?!\n)|\n){2,}", value)
    )
    return Markup(result) if eval_ctx.autoescape else result

DEFAULT_FILTERS["nl2br"] = nl2br

template = Template(template_content)
output = template.render(messages=data, time=datetime.now(tz=timezone.utc).isoformat())
output = htmlmin.minify(output)

with open("index.html", "w") as f:
    f.write(output)
