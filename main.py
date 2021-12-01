import markdown
import frontmatter
import subprocess
import string
import sys
import re


md = markdown.Markdown(extensions=['extra'])
article = {"author": None, "title": None, "date": None, "thumbnail": None, "article_html": None}
template_html = "_template.html"


def print_help():
    print("sofme-markdown-to-html ver.1\n%s <変換するMarkdownファイル>　<変換後のHTMLファイル>\n" % sys.argv[0])


def add_img_responsive_class(markdown_file):
    modified_markdown = re.sub(r'^(!\[.*\]\(.*\))', r'\1{.img-responsive}', markdown_file, flags=re.MULTILINE)
    return modified_markdown


def open_markdown_file(dir):
    try:
        with open(dir) as markdown_file:
            return frontmatter.load(markdown_file)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def write_html(file_name, content):
    try:
        with open(file_name, mode="w") as f:
            f.write(content)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def get_content(file):
    try:
        fsrc = open(file)
    except OSError as e:
        print(e)
    else:
        content = fsrc.read()
        fsrc.close()
        return content


if len(sys.argv) == 1:
    print_help()
    print('Error: 変換するMarkdownファイルのパスを入力してください', file=sys.stderr)
    sys.exit(1)
elif len(sys.argv) == 2:
    print_help()
    print('Error: 変換後のファイル名を入力してください。', file=sys.stderr)
    sys.exit(1)

markdown_file = open_markdown_file(sys.argv[1])
html_file_name = sys.argv[2]

article["author"] = markdown_file["author"]
article["title"] = markdown_file["title"]
article["date"] = markdown_file["date"]
article["thumbnail"] = markdown_file["thumbnail"]

modified_markdown = add_img_responsive_class(markdown_file.content)
article["article_html"] = md.convert(modified_markdown)

generated_html = string.Template(get_content(template_html)).substitute(article)
write_html(html_file_name, generated_html)

subprocess.run(["tidy", "-wrap", "0", "--indent-spaces", "4", "--drop-empty-elements", "no", "-im", html_file_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# print(modified_markdown)
# print(article_html)
