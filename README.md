# Chat HatenaBlog
`Chat HatenaBlog` is an AI-powered software to interact with your HatenaBlog. After indexing your HatenaBlog, you can ask a question, and then AI replies using your HatenaBlog.

This is an alpha version for now, so the interface and index structure may change.

This project is inspired by [Scrapbox ChatGPT Connector](https://github.com/nishio/scrapbox_chatgpt_connector) and [ChatWP](https://github.com/kentaro/chatwp).

## Description
You can create an index of your HatenaBlog with the following command:
```
chat-hatenablog make-index --mt-file blog.shibayu36.org.export.txt
```

Once you have created the index, you can get the answer from ChatGPT, referring to your blog.  You can also get the entry URL related to the answer.

```
$ chat-hatenablog ask --query "Is there anything I should do before I send a PullRequest on GitHub to request a review?"
Yes, it is important to perform a self-code review before sending a PullRequest.
Specifically, only add the necessary parts with git add, confirm the differences
with git diff --cached, and perform a self-code review. When creating a PullRequest,
review the contents of the files yourself, make necessary corrections, leave line comments
on GitHub for unclear parts, and leave comments on the code if necessary. Additionally,
if the code affects the user's flow, it is necessary to trace the user's behavior
yourself and check for any discomfort. By doing these tasks, you can reduce the amount
of rework and provide higher quality code.

refs:
- Efforts to use PullRequest to discuss specifications and implementation policies: https://blog.shibayu36.org/entry/2016/08/05/103000
- Habits to reduce omissions and mistakes in code changes: https://blog.shibayu36.org/entry/2022/04/24/160753
- Automatic merging of library updates using Renovate: https://blog.shibayu36.org/entry/2020/11/10/183000
- Techniques for writing code and documentation based on the criteria that it doesn't matter when you suddenly stop working for the company: https://blog.shibayu36.org/entry/2016/08/05/102111
- Writing code and documentation based on the criteria that it doesn't matter when you suddenly stop working for the company: https://blog.shibayu36.org/entry/2016/08/04/220840
```

## Usage
### Install
```
pip install git+https://github.com/shibayu36/chat-hatenablog.git
```

### Set environment variables
- `OPENAI_API_KEY`: Your API Key for Open AI
- `BASE_URL`: The base URL for your blog.  This is optional and you can also specify it by command line arguments

You can also use a `.env` file.

```
OPENAI_API_KEY=...
BASE_URL=https://blog.shibayu36.org/entry/
```

### Export your HatenaBlog
This tool uses a MovableType exported file.  Access https://blog.hatena.ne.jp/my/export/movable_type and then download the exported file.

### Make index
Make an index like this:

```
chat-hatenablog make-index --mt-file blog.shibayu36.org.export.txt
```

It may take a long time that depends on how many articles your HatenaBlog has.

### Ask with your HatenaBlog
```
chat-hatenablog ask --query "Is there anything I should do before I send a PullRequest on GitHub to request a review?"
```

Then you will get the answer and the related URLs.

## How to Develop
```
pip install -e '.[dev]'
pytest
chat-hatenablog --version
```

## Author
Yuki Shibazaki <shibayu36@gmail.com>
