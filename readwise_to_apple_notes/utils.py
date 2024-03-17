import os
import subprocess
from typing import Generator

import click
from dotenv import load_dotenv
from readwise import Readwise

load_dotenv()

try:
    client = Readwise(os.environ["READWISE_TOKEN"])
except KeyError:
    raise EnvironmentError(
        "READWISE_TOKEN environment variable is not set.",
        "Please set it before continuing or place it in a .env file.",
    )


def get_books():
    """Generates a sequence of books from Readwise.

    Yields:
        dict: A dictionary representing a single book with its details.
    """
    for book in client.get_books(category="books"):
        yield book


def get_book_details(book_id: str) -> dict:
    """Retrieves the details of a specific book by its ID.

    Parameters:
        book_id (str): The unique identifier for the book.

    Returns:
        dict: A dictionary containing the details of the book.
    """
    return client.get(f"/books/{book_id}").json()


def export_highlights(
    updated_after: str = None, book_ids: str = None
) -> Generator[dict, None, None]:
    """Exports the highlights of books based on modification date and/or specific book IDs.

    This function iterates over pages of highlights fetched from the client service,
    filtering by update time and book IDs if provided, and yields each highlight.

    Parameters:
        updated_after (str, optional): The ISO 8601 date string to filter highlights
            that were updated after a certain date. Defaults to None.
        book_ids (str, optional): A comma-separated string of book IDs to filter
            highlights by specific books. Defaults to None.

    Yields:
        dict: A dictionary representing a single book's highlight.
    """
    for data in client.get_pagination_limit_20(
        "/export/", params={"updatedAfter": updated_after, "ids": book_ids}
    ):
        for book in data["results"]:
            yield book


def export_to_apple_notes(updated_after: str, book_id: str) -> None:
    """Exports book highlights to Apple Notes.

    For each highlight of a given book, this function formats the highlight and note
    content, creating or updating a note in the "Readwise" folder within Apple Notes.
    Progress is shown through a progress bar.

    Parameters:
        updated_after (str): The ISO 8601 date string to filter highlights
            that were updated after this date.
        book_id (str): The unique identifier for the book whose highlights
            are to be exported.

    Note:
        This function directly manipulates Apple Notes using AppleScript and
        requires that the user has permissions to execute `osascript`.
    """
    for book in export_highlights(updated_after, book_id):
        with click.progressbar(
            length=len(book["highlights"]),
            label="Exporting highlights",
            show_percent=True,
            show_pos=True,
        ) as bar:
            for highlight in book["highlights"]:
                clean_text = _escape_for_applescript(highlight["text"])
                clean_note = _escape_for_applescript(highlight["note"])

                if highlight["note"].startswith(".h"):
                    apple_script = f"""
                        tell application "Notes"
                        -- Ensure the "Readwise" folder exists
                        set folderName to "Readwise"
                        set theFolder to missing value
                        repeat with eachFolder in folders
                            if name of eachFolder is folderName then
                                set theFolder to eachFolder
                            end if
                        end repeat
                        if theFolder is missing value then
                            set theFolder to (make new folder with properties {{name:folderName}})
                        end if
                        
                        -- Attempt to find the note by title in the "Readwise" folder
                        set theNote to missing value
                        repeat with eachNote in (notes of theFolder)
                            if name of eachNote is "{book["title"]}" then
                                set theNote to eachNote
                                exit repeat
                            end if
                        end repeat
                        
                        -- If found, append new content, otherwise create the note
                        if theNote is not missing value then
                            set the body of theNote to the body of theNote & ¬
                            "<br>" & "<b>{clean_text}</b>"
                        else
                            make new note at theFolder with properties {{name:"{book["title"]}", body:"{clean_text}"}}
                        end if
                    end tell
                    """

                else:
                    highlight_tags = ", ".join(tag["name"] for tag in highlight["tags"])
                    book_tags = ", ".join(tag["name"] for tag in book["book_tags"])

                    apple_script = f"""
                    tell application "Notes"
                        -- Ensure the "Readwise" folder exists
                        set folderName to "Readwise"
                        set theFolder to missing value
                        repeat with eachFolder in folders
                            if name of eachFolder is folderName then
                                set theFolder to eachFolder
                            end if
                        end repeat
                        if theFolder is missing value then
                            set theFolder to (make new folder with properties {{name:folderName}})
                        end if
                        
                        -- Attempt to find the note by title in the "Readwise" folder
                        set theNote to missing value
                        repeat with eachNote in (notes of theFolder)
                            if name of eachNote is "{book["title"]}" then
                                set theNote to eachNote
                                exit repeat
                            end if
                        end repeat
                        
                        -- If found, append new content, otherwise create the note
                        if theNote is not missing value then
                            set the body of theNote to the body of theNote & ¬
                            "<br>" & "{clean_text}" & " (Location {highlight["location"]})" & ¬
                            "<br><br>" & "<b>Note</b>: {clean_note}" & ¬
                            "<br>" & "<b>Tags</b>: {highlight_tags}" & ¬
                            "<br>"
                        else
                            make new note at theFolder with properties {{name:"{book["title"]}", body:"<br>Title: {book["title"]}<br>Category: {book["category"]}<br>Document Tags: {book_tags}"}}
                        end if
                    end tell
                    """

                # Run the AppleScript
                subprocess.run(
                    ["osascript", "-e", apple_script],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )

                bar.update(1)


def _escape_for_applescript(text: str) -> str:
    """
    Escapes double quotes and backslashes in the given text for safe insertion into an AppleScript command.

    Parameters:
        text (str): The text to be escaped.

    Returns:
        str: The escaped text.
    """
    # Escape backslash first to avoid escaping already escaped characters later
    text = text.replace("\\", "\\\\")
    # Escape double quotes
    text = text.replace('"', '\\"')
    return text
