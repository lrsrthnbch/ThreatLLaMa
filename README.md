# ThreatLLaMa
 
## Overview
This project automates the process of creating an LLM embedding with content scraped from a website. The scraped content is tokenized and saved in a vector database and can then be queried on using a local LLM. Streamlit serves as the frontend.

## Prerequisites
The program uses the OpenAI API. This requires either an API Key or a local installation of a Llama Server like ollama or LMStudio

## Setup
Follow these steps to set up and run the project:

1. Clone the Repository:

```
git clone https://github.com/lrsrthnbch/ThreatLLaMa
```
2. Install Dependencies:

```
pip install -r requirements.txt
```

## Usage
1. Start the Streamlit Server:

```
streamlit run app.py

or use the run.bat
```
