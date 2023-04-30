from setuptools import setup, find_packages

setup(
    name="chat_hatenablog",
    version="0.2.1",
    author="Yuki Shibazaki",
    author_email="shibayu36@gmail.com",
    description="AI-powered software to interact with your HatenaBlog",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.0",
        "html2text==2020.1.16",
        "langchain==0.0.132",
        "tqdm==4.65.0",
        "openai==0.27.4",
        "tenacity==8.2.2",
        "tiktoken==0.3.3",
        "numpy==1.24.2",
    ],
    extras_require={
        "dev": [
            "pytest==7.3.1",
            "mypy==1.2.0",
            "pytest-mypy-plugins==1.10.1",
            "types-tqdm==4.65.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "chat-hatenablog = chat_hatenablog.main:main",
        ]
    },
)
