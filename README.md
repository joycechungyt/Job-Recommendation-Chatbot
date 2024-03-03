# Job Recommendation Chatbot

Welcome to the Job Recommendation Chatbot! This chatbot utilizes Natural Language Processing (NLP) to understand and respond to user inputs. It provides job recommendations based on data science job listings.

## Setup

To run this chatbot, you will need Python 3.7 or a later version installed on your computer. You also need to install the following packages: `chromadb`, `PyPDF2`, `sentence_transformers`, `gradio`, `accelerate`, and `transformers`. These can be installed using the command: `!pip install chromadb PyPDF2 sentence_transformers gradio accelerate transformers`.

## Overview

The `chromadb_job_chatbot_jpynb.py` script runs the Job Recommendation Chatbot. It starts by installing necessary packages and setting the locale encoding. Then, it reads job listings from CSV files and combines them into a single list.

The script initializes ChromaDB, a text search and retrieval library, and uses a sentence transformer model to embed job descriptions into a vector space. The embeddings are stored in a ChromaDB collection.

The chatbot interface is created using the Gradio library. Users can enter queries or request a job recommendation. The chatbot generates a context using the user's queries and provides a job recommendation using a language model.

## Example Interactions

Here are a few examples of how the chatbot may respond to user inputs:

**User:** "What roles are available right now?"

**Bot:** "..."
