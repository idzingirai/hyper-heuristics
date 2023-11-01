from typing import List


class GrammarGenerator:

    def __init__(self, terminal_set: List[str]):
        self._terminal_set: List[str] = terminal_set

    def get_grammar(self) -> dict:
        """
        Returns the grammar (Backus-Naur Form) for the grammatical evolution.
        :return: The grammar in the form of a dictionary.
        """
        return {
            '<start>': ['<accept> <action> <heuristic>'],
            '<accept>': ['ILTA', 'AI', 'AEI'],
            '<heuristic>': ['<action> <heuristic>', '<action>'],
            '<action>': ['<swap>', '<move>', '<single_move>', '<swap_lectures>', '<swap_slots>', '<action>'],
            '<swap>': ['swap( <n> <comp> <comp> )'],
            '<move>': ['move( <n> <comp> <comp> )'],
            '<single_move>': ['single_move()'],
            '<swap_lectures>': ['swap_lectures()'],
            '<swap_slots>': ['swap_slots()'],
            '<comp>': ['room', 'slot', 'course'],
            '<n>': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        }

    def get_terminal_set(self) -> List[str]:
        """
        Returns the terminal set.
        :return: The terminal set.
        """
        return self._terminal_set
