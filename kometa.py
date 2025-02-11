import os
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from PIL import Image
import shutil
import subprocess
import markdown
import datetime
import argparse

BASE_DIR = Path(__file__).parent
ARTICLE_BASE_DIR = BASE_DIR / "article"
OUT_BASE_DIR = BASE_DIR / "out" / "article"
TEMPLATE_DIR = BASE_DIR / "template"

load_dotenv()

def create_article(title):
    date_obj = datetime.datetime.now()
    date = str(date_obj.date())
    article_dir = ARTICLE_BASE_DIR / title
    article_dir.mkdir(exist_ok=True, parents=True)
    article_file_path = article_dir / f"{title}.md"
    
    if article_file_path.exists():
        print("Error: Same name article has already exits.")
        return
    article_file_path.write_text(f"""---
title: {title}
date: {date}
---

# {title}
write your wrticle here...
        """, encoding="utf-8")
    print(f"Created article: {article_file_path}")

def convert_article(title):
    j2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = j2_env.get_template("base.html")
    
    article_dir = ARTICLE_BASE_DIR / title
    # article_out_dir = OUT_BASE_DIR / title
    # article_out_dir.mkdir(exist_ok=True, parents=True)

    print("Generating html...")
    for md_file in article_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        md = markdown.Markdown(extensions=["meta"])
        html_content = md.convert(content)
        try:
            visibility = md.Meta["visibility"][0]
        except KeyError:
            print("Error: visibility is not defined in article.")
            return
        html_output = template.render(content=html_content)
        if visibility == "public":
            article_out_dir = OUT_BASE_DIR / "public" / title
        elif visibility == "limited":
            article_out_dir = OUT_BASE_DIR / "limited" / title
        article_out_dir.mkdir(exist_ok=True, parents=True)
        output_html_path = article_out_dir / (md_file.stem + ".html")
        output_html_path.write_text(html_output, encoding="utf-8")
        print(f"Generated article: {output_html_path}")

    print("Deleting exif data in imgs...")
    for img_file in article_dir.glob("*.*"):
        if img_file.suffix.lower() in { ".jpg", ".png"}:
            dstpath = article_out_dir / img_file.name
            img = Image.open(img_file)
            img.save(img_file, exif=b"")
            print(f"Deleted exif data: {img_file}")
            shutil.copy(img_file, dstpath)
            print(f"Copied img file: {dstpath}")
        

def run_dev():
    subprocess.run(["docker", "compose", "up"], check=True)

# def publish():


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["new", "build", "dev", "publish"], help="実行するコマンド")
    parser.add_argument("title", nargs="?", help="article title")
    args = parser.parse_args()

    if args.command == "new" and args.title:
        create_article(args.title)
    elif args.command == "build" and args.title:
        convert_article(args.title)
    elif args.command == "dev":
        run_dev()
    elif args.command == "publish":
        print("Publish...")
        # publish()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()