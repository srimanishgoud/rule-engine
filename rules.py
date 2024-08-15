from node import Node, convert_operator
import ast
import pprint

#function to parse the rule and build ast
def create_rule_tree(rule):
    try:
        rule_ast=ast.parse(rule)
    except SyntaxError:
        print("Invalid rule")
        return None
    return build_ast(rule_ast.body[0].value)

def build_ast(expr):
    if isinstance(expr, ast.BoolOp):
        if isinstance(expr.op, ast.And):
            return Node('operator', build_ast(expr.values[0]), build_ast(expr.values[1]), 'and')
        elif isinstance(expr.op, ast.Or):
            return Node('operator', build_ast(expr.values[0]), build_ast(expr.values[1]), 'or')
    elif isinstance(expr, ast.Compare):
        field = expr.left.id
        op = expr.ops[0]
        value = expr.comparators[0].value
        if field=='age' or field=='salary' or field=='experience':
            value=int(value)
        if field=='department':
            value=value[0:]
        def condition_check(context):
            return eval(f"context['{field}'] {convert_operator(op)} {repr(value)}")
    
        return Node(type='operand', value=f"{field}+{convert_operator(op)}+{value}")

# function to create AST with multiple rule inputs
def combine_rules(rules):
    combined_root = None
    for rule in rules:
        rule_ast = create_rule_tree(rule)
        if(rule_ast is None):
            return None
        if combined_root is None:
            combined_root = rule_ast
        else:
            combined_root = Node(type='operator', left=combined_root, right=rule_ast, value='and')
    return combined_root

def evaluate_rule(tree, context):
    return tree.evaluate(context)

# rule1 = "((age > 30 and department == 'Sales') or (age < 25 and department == 'Marketing')) and (salary > 50000 or experience > 5)"
# rule2 = "((age > 30 and department == 'Marketing')) and (salary > 20000 or experience > 5)"
# rule3="(age > 30 and department == 'Marketing')"
# print(type(rule1))
# rule_ast = create_rule_tree(rule3)
# rule_list=[rule1,rule2]
# combined_rule = combine_rules(rule_list)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(vars(rule_ast))
# context = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
# result = evaluate_rule(combined_rule, context)
# print(f"Is the user eligible? {result}")