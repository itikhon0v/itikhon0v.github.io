from pathlib import Path
import re
import yaml
import markdown
import html
from dataclasses import dataclass
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator


@dataclass
class BlogPost:
    title: str
    date: datetime
    tags: list
    slug: str
    content: str


def load_config(path: str = "config.yml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not config:
        raise ValueError("Configuration is missing or invalid.")
    return config


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "-", value)
    return value.strip("-")


def parse_md_file(path: Path, date_format: str) -> BlogPost:
    lines = path.read_text(encoding="utf-8").splitlines()

    if len(lines) < 4:
        raise ValueError(f"Not enough lines in {path} to parse metadata")

    title = html.escape(lines[0].strip())
    date_str = lines[1].strip()
    date_obj = datetime.strptime(date_str, date_format)
    tags = [tag.strip() for tag in lines[2].split(",")]
    content_md = "\n".join(lines[3:])
    content_html = markdown.markdown(content_md, extensions=["fenced_code", "tables"])

    return BlogPost(
        title=title,
        date=date_obj,
        tags=tags,
        slug=slugify(title),
        content=content_html,
    )


def render_template(template: str, context: dict) -> str:
    for key, value in context.items():
        template = template.replace(f"{{{{ {key.upper()} }}}}", str(value))
    return template


def build_blog(config: dict, blog: list):
    input_dir = Path(config["paths"]["input_dir"])
    output_dir = Path(config["paths"]["output_dir"])
    post_template_path = Path(config["paths"]["post_template"])
    date_format = config["site"]["date_format"]

    output_dir.mkdir(parents=True, exist_ok=True)
    template = post_template_path.read_text(encoding="utf-8")

    for path in input_dir.glob("*.md"):
        post = parse_md_file(path, date_format)

        context = {
            "title": post.title,
            "date": post.date.strftime(date_format),
            "tags": ", ".join(post.tags),
            "content": post.content,
            "year": str(datetime.now(timezone.utc).year),
            "description": post.title
        }

        post_html = render_template(template, context)
        output_path = output_dir / f"{post.slug}.html"
        output_path.write_text(post_html, encoding="utf-8")

        blog.append(post)


def build_index(config: dict, blog: list, start_time):
    template = Path(config["paths"]["index_template"]).read_text(encoding="utf-8")
    output_path = Path(config["paths"]["index_output"])

    posts_html = ""
    for post in sorted(blog, key=lambda x: x.date, reverse=True):
        posts_html += f'<p><a href="blog/{post.slug}.html">{post.title}</a><br />\n'
        posts_html += f'<small>{post.date.strftime(config["site"]["date_format"])} &bullet; {", ".join(post.tags)}</small></p>\n'

    now = datetime.now(timezone.utc)
    context = {
        "BLOG": posts_html,
        "YEAR": str(now.year),
        "BUILD_DATE": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "BUILD_TIME": f"{(datetime.now() - start_time).total_seconds())} s"
    }

    output_html = render_template(template, context)
    output_path.write_text(output_html, encoding="utf-8")


def build_feed(config: dict, blog: list):
    fg = FeedGenerator()
    fg.generator(None)
    fg.docs(None)
    fg.description(config["site"]["description"])
    fg.title(config["site"]["title"])
    fg.link(href=config["site"]["url"], rel="alternate")
    fg.lastBuildDate(datetime.now(timezone.utc))

    for post in sorted(blog, key=lambda x: x.date, reverse=True):
        fe = fg.add_entry()
        fe.title(post.title)
        fe.link(href=f"{config['site']['url']}/blog/{post.slug}.html")
        fe.description(", ".join(post.tags))
        fe.pubDate(post.date.replace(tzinfo=timezone.utc))

    fg.rss_file(config["paths"]["rss_output"])


def main():
    start_time = datetime.now()
    config = load_config()
    blog = []

    build_blog(config, blog)
    build_index(config, blog, start_time)
    build_feed(config, blog)


if __name__ == "__main__":
    main()
