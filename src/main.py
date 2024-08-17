from generate_public_contents import cp_source_contents_to_destination
from page_generation import generate_pages_recursively

def main():
    cp_source_contents_to_destination("static", "public")
    generate_pages_recursively("content", "template.html", "public")

if __name__ == "__main__":
    main()
