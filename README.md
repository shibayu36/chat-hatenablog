# Chat HatenaBlog
`Chat HatenaBlog` is an AI-powered software to interact with your HatenaBlog. After indexing your HatenaBlog, you can ask a question, and then AI replies using your HatenaBlog.

This is an alpha version for now, so the interface and index structure may change.

This project is inspired by [Scrapbox ChatGPT Connector](https://github.com/nishio/scrapbox_chatgpt_connector) and [ChatWP](https://github.com/kentaro/chatwp).

## Description
You can create an index of your HatenaBlog with the following command:
```
python make_index.py --mt-file blog.shibayu36.org.export.txt
```

Once you have created the index, you can get the answer from ChatGPT, referring to your blog.  You can also get the entry URL related to the answer.

```
$ python ask.py --query "Is there anything I should do before I send a PullRequest on GitHub to request a review?"

THINKING...

ANSWER:
Yes, it's a good practice to write down the implementation plan and specifications
in the issue description or as a file in the repository before writing the code.
This way, you can get a review of the plan before implementing it, which can help
prevent significant rework if there are any critical mistakes. It's also helpful to
review your own code before submitting a PullRequest and ensure that it meets
certain standards, such as being easy to understand and having clear comments.
Additionally, it's a good idea to review your code after taking a break and with
fresh eyes to catch any issues you may have missed.

refs:
- Efforts to use PullRequest to discuss specifications and implementation policies: https://blog.shibayu36.org/entry/2016/08/05/103000
- Habits to reduce omissions and mistakes in code changes: https://blog.shibayu36.org/entry/2022/04/24/160753
- Automatic merging of library updates using Renovate: https://blog.shibayu36.org/entry/2020/11/10/183000
- Techniques for writing code and documentation based on the criteria that it doesn't matter when you suddenly stop working for the company: https://blog.shibayu36.org/entry/2016/08/05/102111
- Writing code and documentation based on the criteria that it doesn't matter when you suddenly stop working for the company: https://blog.shibayu36.org/entry/2016/08/04/220840
```

## Usage
### Install prerequisites
```
pip install -r requirements.txt
```

### Set environment variables
- `OPENAI_API_KEY`: Your API Key for Open AI
- `BASE_URL`: The base URL for your blog.  This is optional and you can also specify it by command line arguments

### Export your HatenaBlog
This tool uses a MovableType exported file.  Access https://blog.hatena.ne.jp/my/export/movable_type and then download the exported file.

### Make index
Make an index like this:

```
python make_index.py --mt-file blog.shibayu36.org.export.txt
```

It may take a long time that depends on how many articles your HatenaBlog has.

### Ask with your HatenaBlog
```
python ask.py --query "Is there anything I should do before I send a PullRequest on GitHub to request a review?"
```

Then you will get the answer and the related URLs.

## Author
Yuki Shibazaki <shibayu36@gmail.com>
