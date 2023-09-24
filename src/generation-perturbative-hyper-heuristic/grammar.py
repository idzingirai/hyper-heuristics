import random
from typing import List


class GrammarGenerator:

    def __init__(self, terminal_set: List[str]):
        self._terminal_set = terminal_set

    def get_grammar(self) -> dict:
        """
        Returns the grammar (Backus-Naur Form) for the grammatical evolution.
        :return: The grammar in the form of a dictionary.
        """
        return {
            '<expr>': ['<var>', random.choice(['( <expr> <op> <expr> )', '<expr> <op> <expr>']), '<pre-op> ( <expr> )'],
            '<op>': ['+', '-', '*', '/'],
            '<pre-op>': ['sqrt', 'abs'],
            '<var>': self._terminal_set
        }

    def get_terminal_set(self) -> List[str]:
        """
        Returns the terminal set.
        :return: The terminal set.
        """
        return self._terminal_set
