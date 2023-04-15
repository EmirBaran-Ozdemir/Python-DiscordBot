"""
The ChatGPT class is a Python class for interacting with OpenAI's GPT-3 chatbot
API. It has an __init__ method that initializes the OpenAI API key and a
getAnswerFromAI method that takes a question as a string and returns a response
from the GPT-3 chatbot API.
"""
import os
import openai
from APIs import handleAPIs


class ChatGPT:
    """
    A class for interacting with OpenAI's GPT-3 chatbot API.
    """

    def __init__(self, user):
        """
        Initializes the OpenAI API key.
        """
        self.user = user
        self.userAPI = user + "chat"
        handleAPIs.configure()
        openai.api_key = os.getenv(self.userAPI)

    def getAnswerFromAI(self, question):
        """
        Given a `question` as a string, returns a response from the GPT-3 chatbot API using users API.

        Args:
        - question (str): A string representing the user's input question.

        Returns:
        - str: A string representing the AI's response to the input `question`.
        """

        if not os.getenv(self.userAPI):
            return f"""{self.user} has no API key please get api key from\
https://platform.openai.com/account/api-keys and use lwSetAPI"""
        else:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}]
            )
            return completion.choices[0].message.content

    def setAPI(self, userKey):
        """
        This code adds a new API key for a user to use at

        Args:
            userKey (string): userKey to add chatGPT's database

        Returns:
            string: Succes or error message
        """
        handleAPIs.addAPI(self.userAPI, userKey)
        handleAPIs.configure()
        if os.getenv(self.userAPI):
            openai.api_key = os.getenv(self.userAPI)
            return f"Nice, {self.user} your key succesfully added!"
        else:
            return "Error occured while adding your key"
