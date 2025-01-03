import os
import shutil

from textnode import TextNode, TextType

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

main()

