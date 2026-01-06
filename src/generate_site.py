import os
import shutil

from markdown_to_html_node import markdown_to_html_node, extract_heading


def generate_pages(from_dir, dest_dir, template_path):
    # Read template file
    with open(template_path) as template_file:
        template = template_file.read()

    # Get contents of source directory
    source_contents = []
    traverse_directory(from_dir, source_contents)

    for item in source_contents:
        # Check if each item is a markdown file; ignores others
        split_text = os.path.splitext(item)
        if split_text[1] == ".md":
            destination = split_text[0].replace(from_dir, dest_dir, 1) + ".html"
            create_directory(destination)
            print(
                f"Generating page from {item} to {destination} using {template_path}"
            )

            # Read markdown from file
            with open(item) as md_file:
                md = md_file.read()

            # Fill in template with converted contents of markdown
            heading = extract_heading(md)
            node = markdown_to_html_node(md)
            html_with_heading = template.replace("{{ Title }}", heading)
            html = html_with_heading.replace("{{ Content }}", node.to_html())

            # Write new static site to destination
            with open(destination, "w") as dest_file:
                dest_file.write(html)


def copy_static(source_path, dest_path):
    # Get contents of source directory
    contents_list = []
    traverse_directory(source_path, contents_list)

    # Clear destination directory
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)

    # Copy contents of source directory into destination
    for item in contents_list:
        dest = item.replace(source_path, dest_path, 1)
        create_directory(dest)
        shutil.copy(item, dest)


def traverse_directory(current, contents_list):
    # Recursively traverse source directory and add all file contents to the list
    dir_contents = os.listdir(current)
    for item in dir_contents:
        path = os.path.join(current, item)
        if os.path.isfile(path):
            contents_list.append(path)
        else:
            traverse_directory(path, contents_list)


def create_directory(destination):
    # Recursively create directories for given file path
    dirname = os.path.dirname(destination)
    if os.path.exists(dirname):
        return
    create_directory(dirname)
    os.mkdir(dirname)
