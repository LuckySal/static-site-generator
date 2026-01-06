from generate_site import generate_pages, copy_static

STATIC_DIRECTORY = "static"
DESTINATION_DIRECTORY = "public"
CONTENT_DIRECTORY = "content"
TEMPLATE_PATH = "template.html"


def main():
    # Copy files from static directory to public directory
    copy_static(STATIC_DIRECTORY, DESTINATION_DIRECTORY)

    # Generate pages from markdown and template
    generate_pages(CONTENT_DIRECTORY, DESTINATION_DIRECTORY, TEMPLATE_PATH)


if __name__ == "__main__":
    main()
