from calculus import *


one = Function('p', Function('x', Call(Variable('p'), Variable('x'))))

increment = Function('n', Function('p', Function('x',
                                                 Call(
                                                     Variable('p'),
                                                     Call(
                                                         Call(
                                                             Variable('n'), Variable('p')),
                                                         Variable('x'))))))

add = Function('m', Function('n', Function('f', Function('x',
                                                         Call(
                                                             Call(
                                                                 Variable('m'), Variable('f')),
                                                             Call(
                                                                 Call(
                                                                     Variable('n'), Variable('f')),
                                                                 Variable('x')))))))
def test_grammar():
    assert str(one) == 'lambda p: lambda x: p(x)'


def test_grammar_2():
    assert str(increment) == 'lambda n: lambda p: lambda x: p(n(p)(x))'


def test_grammar_3():
    assert str(add) == 'lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))'


def test_grammar_4():
    e = Function('x', Function('y', Call(Function('z', Call('z', 'x')), Variable('y'))))
    assert str(e) == "lambda x: lambda y: (lambda z: z(x))(y)"


def test_semantic_replace():
    e = Variable('x')
    assert str(e.replace('x', Function('y', Variable('y')))) == 'lambda y: y'
    assert str(e.replace('z', Function('y', Variable('y')))) == str(e)


def test_semantic_replace_2():
    e = Call(
            Call(
                Call(Variable('a'), Variable('b')),
                Variable('c')),
            Variable('b'))
    assert str(e.replace('a', Variable('x'))) == 'x(b)(c)(b)'
    assert str(e.replace('b', Function('x', Variable('x')))) == 'a(lambda x: x)(c)(lambda x: x)'


def test_semantic_replace_3():
    e = Call(
            Call(
                Variable('x'), Variable('y')),
            Function('y',
                     Call(Variable('y'), Variable('x'))))
    assert str(e.replace('x', Variable('z'))) == 'z(y)(lambda y: y(z))'
    assert str(e.replace('y', Variable('z'))) == 'x(z)(lambda y: y(x))'


def test_semantic_replace_4():
    e = Function('x',
                 Call(Variable('x'), Variable('y')))
    replacement = Call(Variable('z'), Variable('x'))
    assert str(e.replace('y', replacement)) == "lambda x': x'(z(x))"


def test_semantic_replace_5():
    # e = lambda p: lambda x: lambda z: (lambda x: y(p(x)))(x)(z)
    e = Function('p', Function('x', Function('z', Call(Call(Function('x', Call(Variable('y'), Call(Variable('p'), Variable('x')))), Variable('x')), Variable('z')))))
    replacement = Call(Variable('z'), Variable('x'))
    assert str(e.replace('y', replacement)) == "lambda p: lambda x': lambda z': (lambda x': z(x)(p(x')))(x')(z')"


def test_semantic_reduce():
    e = Call(Call(add, one), one)
    assert str(reduce(e)) == 'lambda f: lambda x: f(f(x))'


def test_semantic_reduce_2():
    e = Function('x', Call(Function('p', Function('x', Variable('x'))), Variable('x')))
    assert str(reduce(e)) == "lambda p: lambda x: x"


def test_alpha():
    e = alpha(one, Variable('f'))
    assert str(e) == 'lambda f: lambda x: f(x)'

    e = alpha(increment, Variable('g'))
    assert str(e) == 'lambda g: lambda p: lambda x: p(g(p)(x))'

    e = alpha(add, Variable('q'))
    assert str(e) == 'lambda q: lambda n: lambda f: lambda x: q(f)(n(f)(x))'


def test_alpha_2():
    e = Function('x', Function('y', Call(Function('x', Call(Variable('x'), Variable('y'))), Variable('x'))))
    assert str(e) == 'lambda x: lambda y: (lambda x: x(y))(x)'
    e = alpha(e, Variable('w'))
    assert str(e) == 'lambda w: lambda y: (lambda x: x(y))(w)'


def test_beta():
    f = Function('x', Function('y', Call(Variable('x'), Variable('y'))))
    arg = Function('z', Variable('z'))
    assert str(beta(f, arg)) == 'lambda y: (lambda z: z)(y)'


def test_eta():
    e = Function('x', Call(Variable('f'), Variable('x')))
    assert str(eta(e)) == 'f'


def test_eta_2():
    e = lambda x: lambda y: lambda z: x(y)(z)(x)
    e = Function('x', Function('y', Function('z', Call(Call(Call(Variable('x'), Variable('y')),Variable('z')),Variable('x')))))
    assert str(eta(e)) == 'lambda x: lambda y: lambda z: x(y)(z)(x)'


def test_repr():
    assert repr(one) == "Function('p', Function('x', Call(Variable('p'), Variable('x'))))"
