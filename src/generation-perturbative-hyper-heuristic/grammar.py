import random
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
            '<start>': ['<accept> <heuristic>'],
            '<accept>': ['IO', 'AM'],
            '<heuristic>': [
                '( swap <n> ( <compSel> ) )',
                '( move <n> ( <compSel> ) )',
                '<heuristic> <cop> <heuristic>',
                'if ( <cond> <heuristic> <heuristic> )',
            ],
            '<cop>': ['impl', 'or'],
            '<cond>': ['( <rop> <hValue> <hValue> )'],
            '<n>': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '<n>', '<n> <n>'],
            '<hValue>': ['prevFitness', 'currFitness'],
            '<compSel>': [
                'random ( <comp> )',
                'highestCost ( <comp> )',
                'lowestCost ( <comp> )',
                'highestSize ( <comp> )',
                'lowestSize ( <comp> )',
                'if ( <prob> <compSel> <compSel> )',
            ],
            '<comp>': self._terminal_set,
            '<prob>': [25, 50, 75],
            '<rop>': ['>', '<', '>=', '<=']
        }

    def get_terminal_set(self) -> List[str]:
        """
        Returns the terminal set.
        :return: The terminal set.
        """
        return self._terminal_set
