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
        os.mkdir(destination)
        os.mkdir(destination + "/images")
        # copy all files and subdirectories
        contents = os.listdir(source)
        for file in contents:
            shutil.copy(file, destination)

    root = "/home/robert_chandler/workspace/staticsitegenerator/"
    source = root + "static"
    destination = root + "public"
    copy(source, destination)

main()

