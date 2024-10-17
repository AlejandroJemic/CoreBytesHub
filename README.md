# CoreBytesHub

CoreBytesHub is a Python-based application designed to generate concise study notes and summaries from a collection of topics. Using AI, it processes topics in JSON format, creates short study cards or summaries, and stores them locally as Markdown files. These files build a knowledge vault, ideal for developers and tech enthusiasts seeking to create a personal library of information on various topics.

## Features

- **AI-Powered Summaries**: Automatically generate concise summaries for each topic using AI.
- **Markdown Storage**: Saves summaries as `.md` files, creating a structured and easily accessible knowledge repository.
- **JSON Input**: Provide a JSON file with topics, and the app will handle the rest.
- **Customizable Topics**: Add or remove topics and regenerate summaries.
- **Developer-Focused**: Specially tailored to topics related to development, programming, and technology.
- **suport**: enter url, file path or text and generate 


## Installation
git clone this repo

```bash
cd corebyteshub
pip install -r requirements.txt
```

## setup

open src/config.yaml and
 - enter your openai api_key
 - enter desired model
 - enter desired language

```yaml
api_key: <YOUR OPENAI API KEY HERE>
model: gpt-4o-mini
language: english
```
## usage

```bash
cd src
python main.py
```
afeter inserting url, file path or text you will get summary in output folder
located in ../corebyteshub/output
all notes ar stored in folders with name of topic an markdown file format
enjoy


## license

```bash
apache 2.0
```



