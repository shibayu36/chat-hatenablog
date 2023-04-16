from collections import defaultdict
import os
import re
import dotenv
import html2text
import argparse
import openai
from langchain.text_splitter import MarkdownTextSplitter
from tqdm import tqdm
from chat_hatenablog import __version__, VectorStore

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def parse_movable_type_entry(entry_text):
    entry_data = defaultdict(lambda: None)
    # Extract TITLE, BASENAME, BODY, EXTENDED BODY from MT format
    title_pattern = re.compile(
        r"^TITLE:\s*(.+)$",
        re.MULTILINE
    )
    entry_data['title'] = title_pattern.search(entry_text).group(1)

    basename_pattern = re.compile(
        r"^BASENAME:\s*(.+)$",
        re.MULTILINE
    )
    entry_data['basename'] = basename_pattern.search(entry_text).group(1)

    body_pattern = re.compile(
        r"^BODY:\s*(.+?)\n-----",
        re.DOTALL | re.MULTILINE
    )
    entry_data['body'] = body_pattern.search(entry_text).group(1)

    extended_body_pattern = re.compile(
        r"^EXTENDED BODY:\s*(.+?)\n-----",
        re.DOTALL | re.MULTILINE
    )
    extended_body_match = extended_body_pattern.search(entry_text)
    if extended_body_match is not None:
        entry_data['body'] += extended_body_match.group(1)

    return entry_data


def extract_entries_from_movable_type(movable_type_text):
    entry_texts = re.split(r"(?m)^--------\n", movable_type_text)
    entry_texts.pop()  # Delete last empty entry

    entries = [parse_movable_type_entry(entry_text)
               for entry_text in entry_texts]

    return entries


def convert_body_for_index(body):
    """Convert body for index

    Args:
        body: body text
    """
    body = html2text.html2text(body)
    body = re.sub(
        r"\!\[(.*?)\]\(https?://.+?\)",
        r"\1", body, flags=re.DOTALL
    )  # image
    body = re.sub(
        r"\[(.*?)\]\(https?://.+?\)",
        r"\1", body, flags=re.DOTALL
    )  # link

    return body


def make_index_from_hatenablog(hatenablog_mt_file, index_file):
    """Make index from hatenablog exported file

    Args:
        hatenablog_mt_file: hatenablog exported file path
        index_file: index file path
    """
    with open(hatenablog_mt_file, "r", encoding="utf-8") as file:
        content = file.read()

    entries = extract_entries_from_movable_type(content)

    markdown_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0)
    vs = VectorStore(index_file)

    for entry in tqdm(entries):
        converted_body = convert_body_for_index(entry['body'])
        for chunk in markdown_splitter.split_text(converted_body):
            vs.add_record(chunk, entry['title'], entry['basename'])

        vs.save()


def main(args):
    make_index_from_hatenablog(args.mt_file, args.index_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create index from MT exported file.")
    parser.add_argument("-v", "--version", action="version",
                        version=f"{__version__}", help="Display the version")
    parser.add_argument("--mt-file", required=True,
                        help="MT exported file path")
    parser.add_argument("--index-file", default="indices/index.pickle",
                        help="Index file path")

    args = parser.parse_args()
    main(args)
