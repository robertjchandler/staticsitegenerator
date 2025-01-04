import os
import shutil

from textnode import TextNode, TextType
from markdown_to_blocks import markdown_to_html_node

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    def copy(source, destination):
        # delete all the contents of the destination directory
        if os.path.exists(destination):
            shutil.rmtree(destination)
        print(f"creating directory {destination}")
        os.mkdir(destination)
        copy_helper(source, destination)
                
    def copy_helper(source, destination):
        # copy all files and subdirectories
        contents = os.listdir(source)
        for file in contents:
            if "." in file:
                print(f"copying {file} from {source} to {destination}")
                filepath = f"{source}/{file}"
                shutil.copy(filepath, destination)
            else:
                directory = f"{destination}/{file}"
                print(f"creating directory {directory}")
                os.mkdir(directory)
                rec_source = f"{source}/{file}"
                copy_helper(rec_source, directory)

    root = "/home/robert_chandler/workspace/staticsitegenerator/"
    source = root + "static"
    destination = root + "public"
    copy(source, destination)

def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Missing title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r')
    f = from_file.read()
    template_file = open(template_path, 'r')
    t = template_file.read()    
    markdown = markdown_to_html_node(f)
    title = extract_title(markdown)
    html = markdown.to_html()
    t.replace(r"{{ Title }}", title)
    t.replace(r"{{ Content }}", html.split("<\h1>", maxsplit=1)[1])
    dest_file = open(dest_path, 'w')
    dest_file.write(t)
    dest_file.close()
    template_file.close()
    from_file.close()

main()

