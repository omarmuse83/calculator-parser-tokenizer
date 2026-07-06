import string
import operator
from decimal import Decimal, Overflow # to handle expressions that are too large

class EvaluateExpression:
    ''' Constructor method of the EvaluateExpression class doesn't initialize any attributes.
        The clean_up_expression method takes either a list or a string, and removes whitespace in the
        expression. The alternating terms method sees the pairs "[+-, '--', '-+', '++']", and
        replaces them with -, +, -, or + until the operator behind the term is of length one or less.
        The calculation tokenizer defines how much each term is worth. It makes exceptions like 1-+2.
        In that expression: - is worth 10 points because it serves as the operator. The first number is "1 (5 points)". The second
        number is "+2 (5 points for +, and 5 points for the number 2.)". Since the operator is a minus sign, it does the operation 1-2=-1.
        
        The ten tokenizer handles operators "-", and "+" (worth ten points). The twenty tokenizer handles "*" and "/" (worth twenty points).
        The thirty tokenizer handles the caret key "^" worth (30 points) and consecutive caret keys (second caret symbol in the expression is worth 60, third, 90, and so on).
        Parentheses syntax checks for the validity of parentheses pairs. "()" would be valid pair, but ")(" isn't a valid pair.
        The no parentheses evaluate method evaluates the expression assuming parentheses are absent. However:
        the evaluate method is mainly used for parsing expressions regardless of whether they have parentheses or not.
        The inner most parentheses method scans for the very last opening parentheses "(", uses a for loop starting at that
        index, and breaks out of the for loop as the first closing parentheses ")" is identified.
        
        There is a certain mathematical limit: you can't parse expressions over 35 characters long, and long results are blocked
        to preserve system memory. This is to prevent as much memory leaks as possible as Python's automatic
        memory management system isn't always perfect.
    '''
    def __init__(self):
        pass
    def clean_up_expression(self, calculation: list or str) -> str:
        calculation = list(calculation)
        calculation = [i for i in ("".join(calculation)).replace(" ", "")]
        for ele in range(0, len(calculation)-1):
            if (calculation[ele] in [digit for digit in string.digits]) and (calculation[ele+1] == '('):
                calculation.insert(ele+1, '*')
            elif (calculation[ele] == ')') and (calculation[ele+1] == '('):
                calculation.insert(ele+1, '*')
            elif (calculation[ele] == ')') and (calculation[ele+1] in [digit for digit in string.digits]):
                calculation.insert(ele+1, '*')    
        return ''.join(calculation)
    def alternating_terms(self, mathematical_string: str) -> str:
        while (mathematical_string.count('+')+mathematical_string.count('-')) > 1:
            if '+-' in mathematical_string:
                mathematical_string = mathematical_string.replace('+-', '-')
            elif '-+' in mathematical_string:
                mathematical_string = mathematical_string.replace('-+', '-')
            elif '--' in mathematical_string:
                mathematical_string = mathematical_string.replace('--', '+')
            elif '++' in mathematical_string:
                mathematical_string = mathematical_string.replace('++', '+')
        return mathematical_string
    def calculation_tokenizer(self, calculation: list or str) -> list[int]:
        calculation = self.clean_up_expression(calculation)
        thirty_exponent = 1
        thirty_token_store = []
        tokenizer = []
        for ele in range(0, len(calculation)):
            if ((ele == 0) and (calculation[ele] == '+')):
                tokenizer.append(5)
            elif ((ele == 0) and (calculation[ele] == '-')):
                tokenizer.append(5)
            elif ((calculation[ele] == '-') and (calculation[ele-1] in ['-', '*', '+', '/', '^', 'e', 'E'])):
                tokenizer.append(5)
            elif (calculation[ele] == '+') and (calculation[ele-1] in ['-', '*', '+', '/', '^', 'e', 'E']):
                tokenizer.append(5)
            else:
                if calculation[ele] in [i for i in string.digits]+['.', 'e', 'E']:
                    tokenizer.append(5)
                elif calculation[ele] in ['+', '-']:
                    tokenizer.append(10)
                elif calculation[ele] in ['*', '/']:
                    tokenizer.append(20)
                else:
                    tokenizer.append(30)
        for ele in range(0, len(tokenizer)):
            if (tokenizer[ele] == 30) and (len(thirty_token_store) == 0):
                thirty_token_store.append(tokenizer[ele])
            elif ((tokenizer[ele] != 30) and (tokenizer[ele] != 5)) and (len(thirty_token_store) > 0):
                thirty_token_store = []
            elif (tokenizer[ele] == 30) and (len(thirty_token_store) > 0):
                thirty_exponent += 1
                tokenizer[ele] *= thirty_exponent
        return tokenizer
    def ten_tokenizer(self, calculation_list: list) -> list:
        if 'Infinity' in ''.join(calculation_list):
            return 'expression/result too large'
        first_number, second_number = [0 for i in range(2)]
        calculation_list = list(self.clean_up_expression(calculation_list))
        priority_index, left_index, right_index = self.calculation_tokenizer(calculation_list).index(10), 0, 0
        result = 0
        left_index += priority_index
        right_index += priority_index
        while (self.calculation_tokenizer(calculation_list)[left_index-1] == 5) and (left_index-1 != -1):
            left_index -= 1
        while (right_index != len(self.calculation_tokenizer(calculation_list))-1) and (self.calculation_tokenizer(calculation_list)[right_index+1] == 5):
            right_index += 1
        try:
            if self.alternating_terms(''.join(calculation_list[left_index:priority_index]))[0] == '0' and ((len(self.alternating_terms(''.join(calculation_list[left_index:priority_index]))) > 1) and ('.' not in ''.join(calculation_list[left_index:priority_index]))):
                return 'invalid operation'
            elif self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1]))[0] == '0' and ((len(self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1]))) > 1) and ('.' not in ''.join(calculation_list[priority_index+1:right_index+1]))):
                return 'invalid operation'
            else:
                first_number += float(self.alternating_terms(''.join(calculation_list[left_index:priority_index])))
                second_number += float(self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1])))
        except ValueError:
            return 'invalid operation'
        except IndexError:
            return 'invalid operation'
        if calculation_list[priority_index] == '+':
            try:
                result += operator.add(Decimal(str(first_number)), Decimal(str(second_number)))
            except Overflow:
                return 'expression/result too large'
        elif calculation_list[priority_index] == '-':
            try:
                result += operator.sub(Decimal(str(first_number)), Decimal(str(second_number)))
            except Overflow:
                return 'expression/result too large'
        return calculation_list[:left_index]+[str(num) for num in str(result)]+calculation_list[right_index+1:]
    def twenty_tokenizer(self, calculation_list: list) -> list:
        if 'Infinity' in ''.join(calculation_list):
            return 'expression/result too large'
        first_number, second_number = [0 for i in range(2)]
        calculation_list = list(self.clean_up_expression(calculation_list))
        priority_index, left_index, right_index = self.calculation_tokenizer(calculation_list).index(20), 0, 0
        result = 0
        left_index += priority_index
        right_index += priority_index
        while (self.calculation_tokenizer(calculation_list)[left_index-1] == 5) and (left_index-1 != -1):
            left_index -= 1
        while ((right_index != len(self.calculation_tokenizer(calculation_list))-1)) and (self.calculation_tokenizer(calculation_list)[right_index+1] == 5):
            right_index += 1
        try:
            if self.alternating_terms(''.join(calculation_list[left_index:priority_index]))[0] == '0' and ((len(self.alternating_terms(''.join(calculation_list[left_index:priority_index]))) > 1) and ('.' not in ''.join(calculation_list[left_index:priority_index]))):
                return 'invalid operation'
            elif self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1]))[0] == '0' and ((len(self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1]))) > 1) and ('.' not in ''.join(calculation_list[priority_index+1:right_index+1]))):
                 return 'invalid operation'
            else:
                first_number += float(self.alternating_terms(''.join(calculation_list[left_index:priority_index])))
                second_number += float(self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1])))
        except ValueError:
            return 'invalid operation'
        except IndexError:
            return 'invalid operation'
        if calculation_list[priority_index] == '*':
            try:
                result += operator.mul(Decimal(str(first_number)), Decimal(str(second_number)))
            except Overflow:
                return 'expression/result too large'
        elif calculation_list[priority_index] == '/':
            try:
                result += operator.truediv(Decimal(str(first_number)), Decimal(str(second_number)))
            except ZeroDivisionError:
                return 'invalid operation'
            except Overflow:
                return 'expression/result too large'
        return calculation_list[:left_index]+[str(num) for num in str(result)]+calculation_list[right_index+1:]
    def thirty_tokenizer(self, calculation_list: list) -> list:
        if 'Infinity' in ''.join(calculation_list):
            return 'expression/result too large'
        first_number, second_number = [0 for i in range(2)]
        calculation_list = list(self.clean_up_expression(calculation_list))
        thirty_exponent = 1
        left_index, right_index = 0, 0
        priority_index = 0
        try:
            while True:
                priority_index = self.calculation_tokenizer(calculation_list).index(30*thirty_exponent)
                thirty_exponent += 1
        except ValueError:
            priority_index = self.calculation_tokenizer(calculation_list).index(30*(thirty_exponent-1))
        result = 0
        left_index += priority_index
        right_index += priority_index
        while (self.calculation_tokenizer(calculation_list)[left_index-1] == 5) and (left_index-1 != -1):
            left_index -= 1
        while ((right_index != len(self.calculation_tokenizer(calculation_list))-1)) and (self.calculation_tokenizer(calculation_list)[right_index+1] == 5):
            right_index += 1
        try:
            if self.alternating_terms(''.join(calculation_list[left_index:priority_index]))[0] == '0' and ((len(self.alternating_terms(''.join(calculation_list[left_index:priority_index]))) > 1) and ('.' not in ''.join(calculation_list[left_index:priority_index]))):
                return 'invalid operation'
            elif self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1]))[0] == '0' and ((len(self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1]))) > 1) and ('.' not in ''.join(calculation_list[priority_index+1:right_index+1]))):
                return 'invalid operation'
            else:
                first_number += float(self.alternating_terms(''.join(calculation_list[left_index:priority_index])))
                second_number += float(self.alternating_terms(''.join(calculation_list[priority_index+1:right_index+1])))
        except ValueError:
            return 'invalid operation'
        except IndexError:
            return 'invalid operation'
        try:
            if not (first_number < 0):
                result += Decimal(str(first_number)) ** Decimal(str(second_number))
            elif (first_number < 0):
                result += -1 * (Decimal((str(first_number)[1:])) ** Decimal(str(second_number)))
        except Overflow:
            return 'expression/result too large'
        return calculation_list[:left_index]+[str(num) for num in str(result)]+calculation_list[right_index+1:]
    def parentheses_syntax(self, new_list: list) -> list or str:
        new_list_copy = new_list.copy()
        new_list = [i for i in new_list if i == '(' or i == ')']
        while len(new_list) > 2:
            new_list_token = []
            try:
                left_index = new_list.index('(')
                right_index = new_list.index(')')
            except ValueError:
                return 'invalid operation'
            for ele in range(0, len(new_list)):
                if ele != left_index and ele != right_index:
                    new_list_token.append(new_list[ele])
            new_list = new_list_token
        return new_list_copy if new_list == ['(', ')'] else 'invalid operation'
    def no_parentheses_evaluate(self, mathematical_string: str) -> float:
        clean_up = self.clean_up_expression(mathematical_string)
        mathematical_terms = {ele: clean_up for ele in ['+', '-', '*', '/', '^']}
        for key, value in mathematical_terms.items():
            if key in value:
                break
            elif ((key == '^') and (key not in value)):
                if (len(clean_up) > 1 and clean_up[0] == '0') and ('.' not in clean_up):
                    return 'invalid operation'
                elif ((len(clean_up) > 1 and clean_up[0] == '0') and ('.' in clean_up)) or (clean_up == '0'):
                    return float(clean_up)
                else:
                    return float(clean_up)
        mathematical_list = [ele for ele in mathematical_string]
        while (((10 in self.calculation_tokenizer(''.join(mathematical_list)))
               or (20 in self.calculation_tokenizer(''.join(mathematical_list))))
               or (30 in self.calculation_tokenizer(''.join(mathematical_list)))):
            while 30 in self.calculation_tokenizer(''.join(mathematical_list)):
                mathematical_list = self.thirty_tokenizer(mathematical_list)
                if mathematical_list == 'invalid operation':
                    return 'invalid operation'
                elif mathematical_list == 'expression/result too large':
                    return 'expression/result too large'
            while 20 in self.calculation_tokenizer(''.join(mathematical_list)):
                mathematical_list = self.twenty_tokenizer(mathematical_list)
                if mathematical_list == 'invalid operation':
                    return 'invalid operation'
                elif mathematical_list == 'expression/result too large':
                    return 'expression/result too large'
            while 10 in self.calculation_tokenizer(''.join(mathematical_list)):
                mathematical_list = self.ten_tokenizer(mathematical_list)
                if mathematical_list == 'invalid operation':
                    return 'invalid operation'
                elif mathematical_list == 'expression/result too large':
                    return 'expression/result too large'
        return float(self.alternating_terms(''.join(mathematical_list)))
    def inner_most_parentheses(self, mathematical_string: str) -> float:
        mathematical_string = self.clean_up_expression(mathematical_string)
        if self.parentheses_syntax([i for i in mathematical_string]) == 'invalid operation':
            return 'invalid operation'
        inner_left = 0
        outer_right = 0
        for i in range(0, len(mathematical_string)):
            if mathematical_string[i] == '(':
                inner_left = i
        for j in range(inner_left+1, len(mathematical_string)):
            if mathematical_string[j] == ')':
                outer_right = j
                break
        return (inner_left+1, outer_right)
    def evaluate(self, mathematical_string: str) -> float:
        mathematical_string = self.clean_up_expression(mathematical_string)
        if len(mathematical_string) >= 35:
            return 'expression/result too large', len(mathematical_string)
        if ('(' in mathematical_string) or (')' in mathematical_string):
            while True:
                mathematical_list = self.clean_up_expression([i for i in mathematical_string])
                if ('(' not in mathematical_string) and (')' not in mathematical_string):
                    try:
                        if self.no_parentheses_evaluate(mathematical_string) == float('inf'):
                            return 'expression/result too large'
                        else:
                            return self.no_parentheses_evaluate(mathematical_string)
                    except ValueError:
                        return 'invalid operation'
                identify_inner = self.inner_most_parentheses(mathematical_string)
                if identify_inner == 'invalid operation':
                    return 'invalid operation'
                try:
                    mathematical_string = ''.join((list(mathematical_list[:(identify_inner[0]-1)])
                                           + [i for i in str(self.no_parentheses_evaluate(mathematical_string[identify_inner[0]:identify_inner[1]]))]
                                           + list(mathematical_list[identify_inner[1]+1:])
                                           ))
                    if 'expression/result too large' in mathematical_string:
                        return 'expression/result too large'
                except ValueError:
                    return 'invalid operation'
                except Overflow:
                    return 'expression/result too large'
                try:
                    if self.no_parentheses_evaluate(mathematical_string) == float('inf'):
                        return 'expression/result too large'
                    else:
                        return float(mathematical_string)
                except ValueError:
                    continue
        else:
            try:
                if self.no_parentheses_evaluate(mathematical_string) == float('inf'):
                    return 'expression/result too large'
                else:
                    return self.no_parentheses_evaluate(mathematical_string)
            except ValueError:
                return 'invalid operation'      
if __name__ == '__main__':
    exp1 = EvaluateExpression()
    print(exp1.evaluate('9+49^4136643-+'))
    