import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "chat_hatenablog", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name="chat_hatenablog",
    version=about["__version__"],
    author="Yuki Shibazaki",
    author_email="shibayu36@gmail.com",
    description="AI-powered software to interact with your HatenaBlog",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "html2text",
        "langchain",
        "tqdm",
        "openai",
        "tenacity",
        "tiktoken",
        "numpy",
    ],
    extras_require={
        "dev": [
            "pytest",
            "mypy",
            "pytest-mypy-plugins",
            "types-tqdm",
        ],
    },
    entry_points={
        "console_scripts": [
            "chat-hatenablog = chat_hatenablog.main:main",
        ]
    },
)
