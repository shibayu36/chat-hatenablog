import os
import openai
import tiktoken
from .vector_store import VectorStore

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


def ask(args):
    query = args.query
    index_file = args.index_file
    base_url = args.base_url

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

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=RETURN_SIZE,
        temperature=0.0,
        stream=True,
    )

    for chunk in response:
        print(
            chunk['choices'][0]['delta'].get(
                'content', ''),
            end='',
            flush=True
        )

    print('\n\nrefs:')
    for article in {x['basename']: x for x in used_articles}.values():
        print(f"- {article['title']}: {base_url}{article['basename']}")
