import os
import openai
import argparse
import dotenv
import tiktoken
from make_index import VectorStore

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT = """
You are virtual character. Read sample output of the character in the following sample section. Then reply to the input within {return_size} unicode characters.
## Sample
{text}
## Input
{input}
""".strip()

MAX_PROMPT_SIZE = 4000
RETURN_SIZE = 500


def get_token_length(text):
    tokens = tiktoken.get_encoding("cl100k_base").encode(text)
    return len(tokens)


def ask(query, index_file, base_url):
    PROMPT_SIZE = get_token_length(PROMPT)
    rest = MAX_PROMPT_SIZE - RETURN_SIZE - PROMPT_SIZE
    input_size = get_token_length(query)
    if rest < input_size:
        raise RuntimeError("too large input!")
    rest -= input_size

    vs = VectorStore(index_file)
    samples = vs.get_sorted(query)

    to_use = []
    used_articles = []
    for _sim, body, title, basename in samples:
        size = get_token_length(body)
        if rest < size:
            break
        to_use.append(body)
        used_articles.append({"title": title, "basename": basename})

        rest -= size

    text = "\n".join(to_use)
    prompt = PROMPT.format(return_size=RETURN_SIZE, input=query, text=text)

    print("\nTHINKING...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=RETURN_SIZE,
        temperature=0.0,
    )

    # show question and answer
    content = response['choices'][0]['message']['content']
    print("\nANSWER:")
    print(content)
    print()
    print('refs:')
    for article in {x['basename']: x for x in used_articles}.values():
        print(f"- {article['title']}: {base_url}{article['basename']}")


def main(args):
    ask(args.query, args.index_file, args.base_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Answer question with my blog")
    parser.add_argument("--query", required=True)
    parser.add_argument("--index-file", default="indices/index.json",
                        help="Index file path")
    parser.add_argument("--base-url", default=os.environ.get("BASE_URL", ""),
                        help="Base URL of the blog. (e.g. https://example.com/.)  You can set this value with BASE_URL environment variable.")

    args = parser.parse_args()
    main(args)
