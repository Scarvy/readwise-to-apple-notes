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
@click.option("--book-id", type=str, help="Export highlights for a specific book")
def export(stop_after, num_books, book_id, dump):
    if book_id:  # Single book
        book = utils.get_book_details(book_id)
        if dump:
            utils.dump_highlights(book["id"], book["title"])
        else:
            utils.export_book_highlights(book["id"], book["title"], stop_after)
    else:  # All book highlights
        for book in itertools.islice(utils.get_books(), num_books):
            if dump:
                utils.dump_highlights(book.id, book.title)
            else:
                utils.export_book_highlights(book.id, book.title, stop_after)


@cli.command()
@click.argument("book_id")
def book(book_id):
    book = utils.get_book_details(book_id)
    click.echo(json.dumps(book, indent=2))
