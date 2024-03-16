import json

import click

from readwise_to_apple_notes import utils


@click.group()
@click.version_option()
def cli():
    """Export Readwise Highlights to Apple Notes."""


@cli.command()
@click.option(
    "--updated-after", type=click.DateTime(), help="Get all highlights after this date"
)
@click.option("--book-id", type=str, help="Export highlights for a specific book")
@click.option("--dump", is_flag=True, help="Output highlights to standard output")
def export(updated_after, book_id, dump):
    if dump:
        for book in utils.export_highlights(updated_after, book_id):
            for highlight in book["highlights"]:
                click.echo(
                    json.dumps(
                        {
                            "title": book["title"],
                            "highlight": highlight["text"],
                            "note": highlight["note"],
                            "tags": ", ".join(tag["name"] for tag in highlight["tags"]),
                        },
                        indent=2,
                    )
                )
    else:  # Export highlights to apple Notes
        utils.export_to_apple_notes(updated_after, book_id)


@cli.command()
@click.argument("book_id")
def book(book_id):
    book = utils.get_book_details(book_id)
    click.echo(json.dumps(book, indent=2))


@cli.command()
def books():
    for book in utils.get_books():
        click.echo(
            json.dumps(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "category": book.category,
                    "num_highlights": book.num_highlights,
                    "source": book.source,
                    "document_note": book.document_note,
                    "document_tag": ", ".join(tag.name for tag in book.tags),
                },
                indent=2,
            )
        )
