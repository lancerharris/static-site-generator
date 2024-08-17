import os
import pathlib
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

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        full_item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(full_item_path):
            new_item = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, new_item)
            generate_page(full_item_path, template_path, dest_path)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            os.mkdir(new_dest_dir_path)
            generate_pages_recursively(full_item_path, template_path, new_dest_dir_path)
