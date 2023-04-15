"""
This module contains the Rps class for playing Rock-Paper-Scissors. User choice
will be gathered as a string, then it will be converted to an integer, and
finally, the name of the emoji that will be displayed on Discord will be
returned.
"""


class Rps:
    """
    A class for playing RPS against Bot
    """

    def shapes(self, choices):
        """
        The shapes method returns the corresponding emoji message based on the user's input choice.
        Args:
            choices (int): enumerated user choice

        Returns:
            string: name of the emoji that will be displayed on Discord
        """
        if choices == 0:
            message = ":punch:"
            return message
        elif choices == 1:
            message = ":hand_splayed:"
            return message
        elif choices == 2:
            message = ":vulcan:"
            return message

    def userChoiceConv(self, choice):
        """
        The userChoiceConv method for enumerating user input

        Args:
            choice (string): user choice as string

        Returns:
            int: enumerated user choice
        """
        if choice == "r":
            choice = 0
        elif choice == "p":
            choice = 1
        elif choice == "s":
            choice = 2
        else:
            return "error"
        return choice
