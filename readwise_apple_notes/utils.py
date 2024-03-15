import itertools
import json
import os
import subprocess

import click
from dotenv import load_dotenv
from readwise import Readwise

load_dotenv()

client = Readwise(os.environ["READWISE_TOKEN"])


def get_books():
    return client.get_books(category="books")


def get_book_highlights(book_id: str):
    return client.get_book_highlights(book_id)


def get_highlight_count(book_id: str):
    return client.get_with_limit_20("/highlights/", params={"book_id": book_id}).json()[
        "count"
    ]


def get_book_details(book_id: str) -> dict:
    return client.get(f"/books/{book_id}").json()


def export_book_highlights(book_id: str, title: str, num: int | None = None):
    highlights = get_book_highlights(book_id)

    if not num:
        num = get_highlight_count(book_id)

    with click.progressbar(
        length=num,
        label="Exporting highlights",
        show_percent=True,
        show_pos=True,
    ) as bar:
        for highlight in itertools.islice(highlights, num):
            if highlight.note.startswith(".h"):
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
                        if name of eachNote is "{title}" then
                            set theNote to eachNote
                            exit repeat
                        end if
                    end repeat
                    
                    -- If found, append new content, otherwise create the note
                    if theNote is not missing value then
                        set the body of theNote to the body of theNote & ¬
                        "<br>" & "<b>{highlight.text}</b>"
                    else
                        make new note at theFolder with properties {{name:"{title}", body:"{highlight.text}"}}
                    end if
                end tell
                """

            else:
                tags = ", ".join(tag.name for tag in highlight.tags)

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
                        if name of eachNote is "{title}" then
                            set theNote to eachNote
                            exit repeat
                        end if
                    end repeat
                    
                    -- If found, append new content, otherwise create the note
                    if theNote is not missing value then
                        set the body of theNote to the body of theNote & ¬
                        "<br>" & "{highlight.text}" & ¬
                        "<br><br>" & "<b>Note</b>: {highlight.note}" & ¬
                        "<br>" & "<b>Tags</b>: {tags}" & ¬
                        "<br>" & "<b>Last Updated</b>: {highlight.updated.strftime("%d/%m/%Y")}" & ¬
                        "<br>"
                    else
                        make new note at theFolder with properties {{name:"{title}", body:"<br>{highlight.text}"}}
                    end if
                end tell
                """

            # Run the AppleScript
            subprocess.run(["osascript", "-e", apple_script], check=True)

            bar.update(1)


def dump_highlights(book_id: str, book_title: str):
    for highlight in get_book_highlights(book_id):
        click.echo(
            json.dumps(
                {
                    "title": book_title,
                    "highlight": highlight.text,
                    "note": highlight.note,
                    "tags": ", ".join(tag.name for tag in highlight.tags),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    export_book_highlights("38504317", "Zero to One", 10)
