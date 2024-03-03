# Job-Recommendation-Chatbot

Welcome to the Job Recommendation Chatbot! This chatbot uses Natural Language Processing (NLP) to understand and respond to user inputs. It also includes a web scraping feature to provide information about different data science jobs. 

## Setup

### Prerequisites:

You'll need Python 3.7 or later installed on your computer. 

### Running the Chatbot:

The chatbot can be run from the command line.

## Overview

The `chromadb_job_chatbot_jpynb.py` script is the main script that runs the chatbot. Here's a brief overview of how it works:

1. The script begins by importing the necessary modules and setting up the device for PyTorch computations.
2. It then loads the trained model and the intents from a JSON file.
3. The chatbot enters into a while loop, where it waits for user input. If the input is "quit", it breaks the loop and the chatbot stops.
4. If the input matches one of the keys in the data dictionary, it will scrape the data and print the standings.
5. If the input does not match, it tokenizes the input and transforms it into a bag-of-words tensor. This tensor is then fed into the model which produces an output. The output is a tag that corresponds to the type of user intent.
6. The chatbot then selects a random response from the corresponding tag and prints it.

## Web Scraping Feature

The chatbot includes a web scraping feature that uses Beautiful Soup to parse HTML and extract data. The HTML for the tables is stored in a Python dictionary, and the `extract_data` function takes a key from this dictionary, parses the HTML, and returns a Pandas DataFrame with the table data.

## Example Interactions

Here are a few examples of how the chatbot may respond to various user inputs. The responses are chosen randomly from a list of possible responses associated with each intent tag.

**User:** "What roles are available right now?"

**Bot:** " 
