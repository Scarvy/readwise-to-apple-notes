import itertools
import json

import click

from readwise_apple_notes import utils


@click.group()
@click.version_option()
def cli():
    """Export Readwise Highlights to Apple Notes."""


@cli.command()
@click.option("--stop-after", type=int, help="Stop after this many highlights")
@click.option("--num-books", type=int, help="Number of books to process")
@click.option("--dump", is_flag=True, help="Output highlights to standard output")
def export(stop_after, num_books, dump):
    for book in itertools.islice(utils.get_books(), num_books):
        i = 0
        if dump:
            for highlight in utils.get_book_highlights(book.id):
                click.echo(
                    json.dumps(
                        {
                            "title": book.title,
                            "highlight": highlight.text,
                            "note": highlight.note,
                            "tags": ", ".join(tag.name for tag in highlight.tags),
                        },
                        indent=2,
                    )
                )
                i += 1
                if stop_after and i >= stop_after:
                    break
        else:
            utils.export_book_highlights(book.id, book.title, stop_after)
