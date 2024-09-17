from bs4 import BeautifulSoup, Comment, Tag
import typer
from typing_extensions import Annotated


def get_soup_from_file(file: str) -> BeautifulSoup:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return BeautifulSoup(content, "html.parser")  # TODO: remove warning for xml


def insert_markdown_content_into_section_tag(section_tag: Tag, path: str) -> None:

    markdown_file = path + section_tag.get("data-markdown")
    del section_tag["data-markdown"]
    section_tag.append(get_markdown_content(markdown_file, path))


def get_markdown_content(file: str, path: str) -> Tag:

    markdown_soup = get_soup_from_file(file)

    # if markdown loads a svg file get svg soup
    svg_soup = None
    if markdown_soup.find("div") is not None and markdown_soup.find("div").get("data-load"):

        # get svg_soup
        svg_file = path + markdown_soup.find("div").get("data-load")
        svg_soup = get_soup_from_file(svg_file)

        # get comment
        comment = markdown_soup.find(string=lambda text: isinstance(text, Comment))

        # create new div tag
        new_div_tag = markdown_soup.new_tag("div")
        new_div_tag["data-animate"] = None
        new_div_tag.append(svg_soup)
        new_div_tag.append(comment)

        return new_div_tag
    else:
        return markdown_soup


def main(html_file: Annotated[str, typer.Argument()]):
    """
    Create a single html file to use without local server.
    """
    file = html_file.split("/")[-1]
    path = html_file.rstrip(file)

    soup = get_soup_from_file(html_file)

    # for each section tag
    for section_tag in soup.find_all("section"):

        # if the section tag loads a markdown file
        if section_tag.get("data-markdown"):
            insert_markdown_content_into_section_tag(section_tag, path)

    # write the new html code to a file
    with open(path + "single_html.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())


if __name__ == "__main__":
    typer.run(main)
