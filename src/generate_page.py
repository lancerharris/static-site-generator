import re

from block_markdown import markdown_to_html_node

def extract_title(markdown):
    match = re.search(r"^#\s\s*(.+?)\s*$", markdown, re.MULTILINE)
    if match:
        h1_content = match.group(1)
        return h1_content.strip()
    else:
        return None
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    page_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    with open(template_path, "r") as f:
        template = f.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", page_content)

    with open(dest_path, "w") as f:
        f.write(template)

