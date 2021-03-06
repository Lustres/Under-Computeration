from FA import *
from base import RuleBook, MultiRuleBook


def test_DFA():
    rulebook = RuleBook([
        FARule(1, 'a', 2), FARule(1, 'b', 1),
        FARule(2, 'a', 2), FARule(2, 'b', 3),
        FARule(3, 'a', 3), FARule(3, 'b', 3)
    ])
    dfa_design = FADesign(FAConfig(1), [3], rulebook)
    assert dfa_design.is_accepted('a') == False
    assert dfa_design.is_accepted('baa') == False
    assert dfa_design.is_accepted('baba') == True


def test_NFA():
    rulebook = MultiRuleBook([
        FARule(1, None, 2), FARule(1, None, 4),
        FARule(2, 'a', 3), FARule(3, 'a', 2),
        FARule(4, 'a', 5), FARule(5, 'a', 6), FARule(6, 'a', 4)
    ])
    nfa_design = FADesign({FAConfig(1)}, {2, 4}, rulebook)
    assert nfa_design.is_accepted('aa') == True
    assert nfa_design.is_accepted('aaa') == True
    assert nfa_design.is_accepted('aaaaa') == False
    assert nfa_design.is_accepted('aaaaaa') == True
