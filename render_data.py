import htmlmin
import json
import os
import re
from config import UIN, NICKNAME, WORKDIR
from datetime import datetime, timezone
from jinja2 import Template, pass_eval_context
from jinja2.defaults import DEFAULT_FILTERS
from markupsafe import Markup, escape


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


def datetime_fromtimestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def render_messages(year: int = datetime.now().year):
    with open("template.html", "r") as f:
        template_content = f.read()
    with open(f"{WORKDIR}/data/years/{year}.json", "r") as f:
        data = json.load(f)

    DEFAULT_FILTERS["nl2br"] = nl2br
    DEFAULT_FILTERS["datetime_fromtimestamp"] = datetime_fromtimestamp

    template = Template(template_content, autoescape=True)
    output = template.render(
        uin=UIN,
        nickname=NICKNAME,
        messages=data,
        time=datetime.now(tz=timezone.utc).isoformat(),
        year=year,
        year_now=datetime.now().year,
    )
    output = htmlmin.minify(output)

    with open(f"{WORKDIR}/{year}.html", "w") as f:
        f.write(output)


def render_index():
    with open("template_index.html", "r") as f:
        template_content = f.read()

    years = sorted(
        [int(f.split(".")[0]) for f in os.listdir(f"{WORKDIR}/data/years")],
        reverse=True,
    )
    template = Template(template_content, autoescape=True)
    output = template.render(
        uin=UIN,
        nickname=NICKNAME,
        years=years,
        time=datetime.now(tz=timezone.utc).isoformat(),
    )
    output = htmlmin.minify(output)

    with open(f"{WORKDIR}/index.html", "w") as f:
        f.write(output)


if __name__ == "__main__":
    render_messages()
    render_index()
