from generate_page import generate_page
from generate_public_contents import cp_source_contents_to_destination

def main():
    cp_source_contents_to_destination("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
