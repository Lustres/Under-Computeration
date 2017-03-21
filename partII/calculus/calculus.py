class Variable:
    """
    Variable objects could be captured or passed in lambda expression.
    """
    def __init__(self, name):
        """
        :type str
        :param name: a string used to refer this object
        """
        self.name = name

    def replace(self, name, another):
        """
        replace a variable with another expression.
        :type str
        :param name: name of aim variable
        :param another: an expression used to replace
        :return: expression passed in if name marched or self
        """
        if self.name == name:
            return another
        else:
            return self

    def bound_vars(self):
        """
        Variable never bound variable.
        """
        return {}

    def free_vars(self):
        """
        Variable always introduce free variable into context.
        """
        return {self.name}

    def __repr__(self):
        return self.name


class Function:
    """
    Function objects represent a single parameter lambda expression.
    """
    def __init__(self, parameter, body):
        """
        :type str
        :param parameter: the name of variable which passed in

        :type Function | Call | Variable
        :param body: the rest of lambda
        """
        self.parameter = parameter
        self.body = body

    def replace(self, name, another):
        """
        replace a free variable in the body of this function with another expression.
        Please make sure replacement doesn't have free variable of which name appear in aim function.

        The free variable in replacement maybe captured by outer lambda parameter in accident .
            eg:
                e = lambda x: x(y)
                let y = z(x)
                => e = lambda x: x(z(x))
                                     ^ free variable captured

        The right behavior is rename parameter when conflict happened:
            eg:
                e = lambda x: x(y)
                let y = z(x) # free variable conflict
                => e = lambda w: w(y) # rename parameter with a unique id
                     = lambda w: w(z(x))

        We could record variable name used in term to solve this problem.
        This implement are still effective as long as we make sure the replacement never contain free variable.
        :type str
        :param name: name of aim variable
        :param another: an expression used to replace
        :type Function
        :return: function after replace in if name marched or self
        """
        if self.parameter == name:
            return self
        else:
            return Function(self.parameter, self.body.replace(name, another))

    def bound_vars(self):
        """
        Function only bound variable once as its parameter.
        """
        return {self.parameter}

    def free_vars(self):
        """
        Function will bound its parameter on body.
        """
        return self.body.free_vars() - self.bound_vars()

    def __repr__(self):
        return f"lambda {self.parameter}: {self.body}"


def alpha(func, rename, aim = None):
    """
    :type Function
    :param func:
    :type Variable
    :param rename:
    """
    if isinstance(func, Function):
        if aim is None:
            # first call
            # replace parameter and apply alpha_conv to body
            return Function(rename, alpha(func.body, rename, func.parameter))
        else:
            # not first call
            if func.parameter is aim:
                # inner bounded
                return func
            else:
                # alpha_conv to body
                return Function(func.parameter, alpha(func.body, rename, aim))
    elif isinstance(func, Call):
        return Call(alpha(func.left, rename, aim), alpha(func.right, rename, aim))
    elif isinstance(func, Variable):
        if func.name == aim:
            return rename
        else:
            return func
    else:
        raise TypeError()


def beta(func, argument):
    """
    :type Function
    :param func:
    """
    return func.body.replace(func.parameter, argument)


def eta(func):
    """
    :type Function
    :param func:
    """
    if isinstance(func.body, Call) \
            and repr(func.body.right) is func.parameter \
            and func.parameter not in func.body.left.free_vars():
        return func.body.left
    else:
        return func


class Call:
    """
    Call objects define a call action on an entity.
    """
    def __init__(self, left, right):
        """
        :type Function | Call | Variable
        :param left: called entity
        :type Function | Call | Variable
        :param right: the parameter which will be passed in
        """
        self.left = left
        self.right = right

    def replace(self, name, another):
        """
        replace a variable in this call with another expression.
        :type str
        :param name: name of aim variable
        :param another: an expression used to replace
        :type Call
        :return: Call after replace in if name marched or self
        """
        return Call(self.left.replace(name, another), self.right.replace(name, another))

    def reduce(self):
        """
        reduce a call expression
        This method will call `reduce` on two parts recursively.
        And then make call on it self.
        """
        if is_reducible(self.left):
            return Call(self.left.reduce(), self.right)
        elif is_reducible(self.right):
            return Call(self.left, self.right.reduce())
        else:
            return beta(self.left, self.right)

    def bound_vars(self):
        """
        Call never bound variable cause all bounded value inside are not visible outside.
        """
        return {}

    def free_vars(self):
        """
        All free variable in sub pair of Call are still visible outside.
        """
        return self.left.free_vars() | self.right.free_vars()

    def __repr__(self):
        return f"{self.left}({self.right})"


def is_reducible(term):
    """
    check a term whether reducible, raise a TypeError when term is not Variable, Function or Call
    :type Variable | Function | Call
    :param term: must be a instance of Variable, Function or Call
    :type bool
    :return: True if term is reducible or False
    """
    if isinstance(term, Variable) or isinstance(term, Function):
        return False
    elif isinstance(term, Call):
        return is_reducible(term.left) or is_reducible(term.right) or isinstance(term.left, Function)
    else:
        raise TypeError()
