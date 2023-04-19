from collections import defaultdict
import re
import html2text
from langchain.text_splitter import MarkdownTextSplitter
from tqdm import tqdm
from chat_hatenablog import __version__, VectorStore
from chat_hatenablog.entry import Entry


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


def make_index(args):
    """Make index from hatenablog exported file

    Args:
        hatenablog_mt_file: hatenablog exported file path
        index_file: index file path
    """

    mt_file = args.mt_file
    index_file = args.index_file

    with open(mt_file, "r", encoding="utf-8") as file:
        content = file.read()

    entries = [
        Entry(item['title'], convert_body_for_index(
            item['body']), item['basename'])
        for item in extract_entries_from_movable_type(content)
    ]

    vs = VectorStore(index_file)

    for entry in tqdm(entries):
        vs.add_entry(entry)
        vs.save()
