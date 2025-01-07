import os
import shutil

from markdown_to_blocks import markdown_to_html_node

def main():
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

    from_path = root + "content"
    template_path = root + "template.html"
    generate_pages_recursive(from_path, template_path, destination)

def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Missing title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r')
    markdown = from_file.read()
    title = extract_title(markdown)
    template_file = open(template_path, 'r')
    template = template_file.read()
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_file = open(dest_path, 'w')
    dest_file.write(template)
    dest_file.close()
    template_file.close()
    from_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for file in contents:
        if "." in file:
            if file.endswith(".md"):                
                source = f"{dir_path_content}/{file}"
                file = file.replace(".md", ".html")
                print(f"source: {source}")
                print(f"template_path: {template_path}")
                print(f"dest_dir_path/file: {dest_dir_path}/{file}")
                generate_page(source, template_path, f"{dest_dir_path}/{file}")
        else:
            directory = f"{dest_dir_path}/{file}"
            print(f"creating directory {directory}")
            os.mkdir(directory)
            rec_source = f"{dir_path_content}/{file}"
            generate_pages_recursive(rec_source, template_path, directory)

main()

