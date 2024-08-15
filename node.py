import ast

def convert_operator(op):
    if isinstance(op, ast.Gt):
        return ">"
    elif isinstance(op, ast.Lt):
        return "<"
    elif isinstance(op, ast.GtE):
        return ">="
    elif isinstance(op, ast.LtE):
        return "<="
    elif isinstance(op, ast.Eq):
        return "=="
    elif isinstance(op, ast.NotEq):
        return "!="
    return None

def str_to_int(s):
    try:
        return int(s)
    except ValueError:
        return s
class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type=type
        self.left=left
        self.right=right
        self.value=value
    def __repr__(self):
        return f"Type: {self.type}, Left: {self.left}, Right: {self.right}, value:{self.value}"
    def evaluate(self, data):
        if self.type=='operator':
            if self.value=='and':
                return self.left.evaluate(data) and self.right.evaluate(data)
            elif self.value=='or':
                return self.left.evaluate(data) or self.right.evaluate(data)
        elif self.type=='operand':
            def condition_check(data, field, op, value):
                # print("Hello")
                # print(type((data[field])), type(value), data[field], value)
                use=str_to_int(data[field])
                if(op=="=="):
                    if(type(use)==type("")):
                        return use.upper()==value.upper()
                    return use==value
                elif op=="!=":
                    return use!=value
                elif op==">":
                    return use>value
                elif op=="<":
                    return use<value
                elif op==">=":
                    return use>=value
                elif op=="<=":
                    return use<=value
                # return eval(f"{use} {op} {repr(value)}")
            data_=self.value
            field, op, value_=data_.split('+')
            print("cond:", field, op, value_)
            if field=='age' or field=='salary' or field=='experience':
                value_=int(value_)
            if field=='department':
                value_=value_[0:]
            return condition_check(data, field, op, value_)

    def to_dict(self):
        node_dict = {
            'type': self.type,
            'value': self.value
        }
        if self.left:
            node_dict['left'] = self.left.to_dict()
        if self.right:
            node_dict['right'] = self.right.to_dict()
        return node_dict
    
    def from_dict(node_dict):
        left = Node.from_dict(node_dict['left']) if 'left' in node_dict else None
        right = Node.from_dict(node_dict['right']) if 'right' in node_dict else None
        return Node(type=node_dict['type'], left=left, right=right, value=node_dict['value'])



            
