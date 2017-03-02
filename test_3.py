from PDARule import *

def test_DPDA():
    import DPDA
    rulebook = DPDA.DPDARuleBook([
        PDARule(1, '(', 2, '$', ['b', '$']),
        PDARule(2, '(', 2, 'b', ['b', 'b']),
        PDARule(2, ')', 2, 'b', []),
        PDARule(2, None, 1, '$', ['$'])
    ])
    dpda_design = DPDA.DPDADesign(1, [1], rulebook)
    assert dpda_design.is_accepted('(((((((((())))))))))') == True
    assert dpda_design.is_accepted('()(())((()))(()(())))') == False
    assert dpda_design.is_accepted('(()(()(()()(()()))()') == False
    assert dpda_design.is_accepted('())') == False


def test_DPDA_2():
    import DPDA
    rulebook = DPDA.DPDARuleBook([
        PDARule(1, 'a', 2, '$', ['a', '$']),
        PDARule(1, 'b', 2, '$', ['b', '$']),
        PDARule(2, 'a', 2, 'a', ['a', 'a']),
        PDARule(2, 'b', 2, 'b', ['b', 'b']),
        PDARule(2, 'a', 2, 'b', []),
        PDARule(2, 'b', 2, 'a', []),
        PDARule(2, None, 1, '$', ['$'])
    ])
    dpda_design = DPDA.DPDADesign(1, [1], rulebook)
    assert dpda_design.is_accepted('ababab') == True
    assert dpda_design.is_accepted('bbbaaaab') == True
    assert dpda_design.is_accepted('baa') == False


def test_NPDA():
    import NPDA
    rulebook = NPDA.NPDARuleBook([
        PDARule(1, 'a', 1, '$', ['a', '$']),
        PDARule(1, 'a', 1, 'a', ['a', 'a']),
        PDARule(1, 'a', 1, 'b', ['a', 'b']),
        PDARule(1, 'b', 1, '$', ['b', '$']),
        PDARule(1, 'b', 1, 'a', ['b', 'a']),
        PDARule(1, 'b', 1, 'b', ['b', 'b']),
        PDARule(1, None, 2, '$', ['$']),
        PDARule(1, None, 2, 'a', ['a']),
        PDARule(1, None, 2, 'b', ['b']),
        PDARule(2, 'a', 2, 'a', []),
        PDARule(2, 'b', 2, 'b', []),
        PDARule(2, None, 3, '$', ['$']),
    ])
    config = PDAConfig(1, Stack(['$']))
    npda = NPDA.NPDA({config}, {3}, rulebook)
    assert npda.is_accepted() == True
    assert len(npda.current_configs) == 3
    assert npda.read_string('abb').is_accepted() == False
    assert len(npda.current_configs) == 3
    assert npda.__read_char('a').is_accepted() == True


def test_NPDA_2():
    import NPDA
    rulebook = NPDA.NPDARuleBook([
        PDARule(1, 'a', 1, '$', ['a', '$']),
        PDARule(1, 'a', 1, 'a', ['a', 'a']),
        PDARule(1, 'a', 1, 'b', ['a', 'b']),
        PDARule(1, 'b', 1, '$', ['b', '$']),
        PDARule(1, 'b', 1, 'a', ['b', 'a']),
        PDARule(1, 'b', 1, 'b', ['b', 'b']),
        PDARule(1, None, 2, '$', ['$']),
        PDARule(1, None, 2, 'a', ['a']),
        PDARule(1, None, 2, 'b', ['b']),
        PDARule(2, 'a', 2, 'a', []),
        PDARule(2, 'b', 2, 'b', []),
        PDARule(2, None, 3, '$', ['$']),
    ])
    npda_design = NPDA.NPDADesign(1, {3}, rulebook)
    assert npda_design.is_accepted('') == True
    assert npda_design.is_accepted('abba') == True
    assert npda_design.is_accepted('babbbbab') == True
    assert npda_design.is_accepted('abb') == False
    assert npda_design.is_accepted('baabaa') == False
