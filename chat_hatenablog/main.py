import argparse
import os
import dotenv
import openai
from chat_hatenablog import ask, make_index, __version__

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def default_index_file_path() -> str:
    home_dir = os.path.expanduser('~')
    tool_dir = os.path.join(home_dir, '.chat-hatenablog')
    return os.path.join(tool_dir, 'index.pickle')


def main():
    parser = argparse.ArgumentParser(
        description='Chat HatenaBlog')
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{__version__}", help="Display the version")

    subparsers = parser.add_subparsers(
        title='subcommands', description='available subcommands')

    index_file_args = {
        "default": default_index_file_path(),
        "help": "Index file path. Default: ~/.chat-hatenablog/index.pickle"
    }

    # ask subcommand
    parser_ask = subparsers.add_parser(
        'ask', description='Ask a question and get answers from your Hatena Blog')
    parser_ask.add_argument("--query", required=True)
    parser_ask.add_argument(
        "--index-file", **index_file_args)
    parser_ask.add_argument(
        "--base-url", default=os.environ.get("BASE_URL", ""),
        help="Base URL of the blog. (e.g. https://example.com/.)  You can set this value with BASE_URL environment variable.")
    parser_ask.set_defaults(func=ask)

    # make-index subcommand
    parser_make_index = subparsers.add_parser(
        'make-index', help='Create an index from MT exported file')
    parser_make_index.add_argument(
        "--mt-file", required=True,
        help="MT exported file path")
    parser_make_index.add_argument(
        "--index-file", **index_file_args)
    parser_make_index.set_defaults(func=make_index)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
