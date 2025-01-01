import re
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
        # copy all files and subdirectories
        contents = os.listdir(source)
        for file in contents:
            if file.endswith((".css", ".png")):
                print(f"copying {file} from {source} to {destination}")
                filepath = f"{source}/{file}"
                shutil.copy(filepath, destination)
            else:
                directory = f"{destination}/{file}"
                print(f"creating directory {directory}")
                # os.mkdir(directory)
                rec_source = f"{source}/{file}"
                copy(rec_source, directory)
                

    root = "/home/robert_chandler/workspace/staticsitegenerator/"
    source = root + "static"
    destination = root + "public"
    copy(source, destination)

main()

