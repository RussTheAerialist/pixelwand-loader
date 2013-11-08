import re

_scanner = re.Scanner([
    (r'{[fis]:[a-z_]+}', lambda scanner,token:("VARIABLE", token)),
    (r'[a-zA-Z0-9_]+', lambda scanner,token:("LITERAL", token)),
])
_integer = re.compile(r'\d+')
_float = re.compile(r'\d+(\.\d+){0,1}')


class Expression(object):
    def __init__(self, expression):
        self._expression = expression
        self._leftover = ""
        self._valid = False

    def __call__(self, realized):
        self._valid = True
        for token,value in self._tokenize_expression():
            func = getattr(self, "do_{0}".format(token))
            realized = func(value, realized) 
            if not self._valid:
                self._leftover=realized
                return False

        self._leftover = realized

        return True

    def do_VARIABLE(self,value,realized):
        value = value[1:-1]
        type_ = value[0]
        value = value[2:]
        func = getattr(self, "do_VARIABLE_{0}".format(type_))
        data,realized = func(value, realized)
        if self._valid:
            setattr(self, value, data)

    def do_VARIABLE_s(self, value,realized):
        return realized.strip(), ""

    def _do_regex(self, realized, regex, convert):
        data = regex.match(realized)
        if not data:
            self._valid = False
            return "", realized

        data = data.group(0)
        
        return convert(data), realized[len(data):]

    def do_VARIABLE_i(self, value,realized):
        return self._do_regex(realized, _integer, int)

    def do_VARIABLE_f(self, value,realized):
        return self._do_regex(realized, _float, float)

    def do_LITERAL(self,value,realized):
        if realized.startswith(value):
            return realized[len(value):]
        
        self._valid = False
        return realized

    def _tokenize_expression(self):
        retval,leftover = _scanner.scan(self._expression)
        if leftover:
           raise ValueError("Expression syntax error: {0}".format(leftover))
        return retval

    @property
    def valid(self):
        return True

    @property
    def leftover(self):
        return self._leftover
