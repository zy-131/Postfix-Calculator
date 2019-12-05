'''
Team members: Zaid Yazadi
              Zhuoran Han

Collaboration Statement: N/A

'''

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
        self.count=0

    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    # Checks if stack is empty
    # return: - True/False (boolean)
    def isEmpty(self):
        if self.top:
            return False
        else:
            return True

    # Iterates through stack to determine length
    # return: - length of stack
    def __len__(self):
        cur = self.top
        length = 0
        while cur:
            length += 1
            cur = cur.next
        return length

    # Pushes new node to top of stack
    # Parameters: value (any value)
    # return nothing
    def push(self, value):
        new = Node(value)
        new.next = self.top
        self.top = new

    # Pops top node from stack
    # Top node is removed and value of node is returned
    # return: - None (stack is empty)
    #         - x (value of popped node)
    def pop(self):
        if self.isEmpty():
            return None
        else:
            x = self.top.value
            self.top = self.top.next
            return x

    # Checks and returns value of top node without popping it
    # returns: - None(stack is empty)
    #          - top node's value
    def peek(self):
        if self.isEmpty():
            return None
        return self.top.value


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.expr = None

    # Checks if inputted string can be converted to float
    # Parameters: - txt (string)
    # returns: - True/False (boolean)
    def isNumber(self, txt):
        try:
            x = float(txt)
            return True
        except ValueError:
            return False

    # Takes inputted infix notation and returns converted postfix notation
    # Parameters: - txt(string): infix notation
    # returns: - 'error message' (if infix is not valid)
    #          - 'Argument error in postfix' (if txt not str or len(txt) <= 0)
    #          - Postfix notation (str)
    def postfix(self, txt):
        '''
            Required: postfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x.postfix(' 2 ^        4')
            '2.0 4.0 ^'
            >>> x.postfix('2')
            '2.0'
            >>> x.postfix('2.1*5+3^2+1+4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x.postfix('    2 *       5.34        +       3      ^ 2    + 1+4   ')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x.postfix(' 2.1 *      5   +   3    ^ 2+ 1  +     4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x.postfix('(2.5)')
            '2.5'
            >>> x.postfix ('((2))')
            '2.0'
            >>> x.postfix ('     -2 *  ((  5   +   3)    ^ 2+(1  +4))    ')
            '-2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x.postfix ('  (   2 *  ((  5   +   3)    ^ 2+(1  +4)))    ')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x.postfix ('  ((   2 *  ((  5   +   3)    ^ 2+(1  +4))))    ')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4)    ')
            '2.0 5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'
            >>> x.postfix('2 *    5   +   3    ^ -2       +1  +4')
            'error message'
            >>> x.postfix('2    5')
            'error message'
            >>> x.postfix('25 +')
            'error message'
            >>> x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4    ')
            'error message'
            >>> x.postfix('2*(5 +3)^ 2+)1  +4(    ')
            'error message'
        '''
        if not isinstance(txt,str) or len(txt)<=0:
            print("Argument error in postfix")
            return None

        postStack=Stack()
        
        if txt.count(' ') > 0:              # checks if there are 2 numbers w/o operator between them
            for i in range(len(txt) - 1):
                if self.isNumber(txt[i]):
                    x = i
                    while x < len(txt) and self.isNumber(txt[x]):
                        x += 1
                    while x < len(txt):
                        if self.isNumber(txt[x]):
                            return 'error message'
                        elif txt[x] == ' ':
                            x += 1
                        else:
                            break

        txt = txt.replace(' ', '')          # removes all spaces from infix for easier traversal
        postfix = []
        txtList = []
        num = []
        leftP = txt.count('(')
        rightP = txt.count(')')
        if leftP != rightP:                 # checks if equal # of right/left parentheses
            return 'error message'

        # returns a new list that contains each separated term of infix for easier reading
        precedence = {'^': 1, '*': 2, '/': 2, '+': 3, '-': 3}
        for i in range(len(txt)):           # multiple lines of if statements to validate infix input
            if i == 0 and txt[i] == '-':    # try-except to deal with IndexErrors
                num.append(txt[i])
                continue
            try:
                if self.isNumber(txt[i]) and (self.isNumber(txt[i+1]) or txt[i+1] == '.'):
                    num.append(txt[i])
                elif txt[i] == '.':
                    num.append(txt[i])
                elif txt[i] == '-' and self.isNumber(txt[i+1]) and txt[i-1] not in precedence and txt[i-1] != '(':
                    txtList.append(txt[i])
                elif txt[i] == '-' and self.isNumber(txt[i+1]) and (txt[i-1] in precedence or txt[i-1] == '('):
                    num.append(txt[i])
                elif self.isNumber(txt[i]) and (txt[i+1] in precedence or txt[i+1] == ')' or txt[i+1] == '('):
                    num.append(txt[i])
                    txtList.append(str(float(''.join(num))))
                    num[:] = []
                elif txt[i] == '(' and (txt[i+1]=='-' or self.isNumber(txt[i+1]) or txt[i+1] == '('):
                    txtList.append(txt[i])
                elif txt[i] in precedence and (txt[i+1] == '-' or self.isNumber(txt[i+1])
                                               or txt[i+1] == '('):
                    txtList.append(txt[i])
                elif txt[i] == ')' and (txt[i+1] in precedence or txt[i+1] == ')'):
                    txtList.append(txt[i])
                else:
                    return 'error message'
            except IndexError:
                if self.isNumber(txt[i]):
                    num.append(txt[i])
                    txtList.append(str((float(''.join(num)))))
                elif txt[i] == ')':
                    txtList.append(txt[i])
                else:
                    return 'error message'

        for i in range(len(txtList)):               # after validation, computes postfix using Stack
            if self.isNumber(txtList[i]) or txtList[i] == '.':  # operand is encountered
                postfix.append(txtList[i])
            elif txtList[i] == '(':             # left parentheses encountered
                postStack.push(txtList[i])
            elif txtList[i] == ')':             # right parentheses encountered
                while (not postStack.isEmpty()) and postStack.peek() != '(':
                    postfix.append(postStack.pop())
                if (not postStack.isEmpty()) or postStack.peek == '(':
                    postStack.pop()
                else:
                    return 'error message'
            else:                                                               # operator encountered
                while (not postStack.isEmpty()) and postStack.peek() != '(' \
                        and (precedence[(txtList[i])] >= precedence[(postStack.peek())]):
                    postfix.append(postStack.pop())
                postStack.push(txtList[i])
        while not postStack.isEmpty():
            postfix.append(postStack.pop())
        return " ".join(postfix)                # joins all values in postfix list

    # Property method to calculate expression from postfix
    # returns: - 'error message' (self.expr is not valid)
    #          - 'Argument error in calculate' (self.expr not str or too short)
    #          - Top node of final stack (calculated value)(float)
    @property
    def calculate(self):
        '''
            Required: calculate must call postfix
                      calculate must create and use a Stack to compute the final result as shown in the video lecture
            >>> x=Calculator()
            >>> x.expr='    4  +      3 -2'
            >>> x.calculate
            5.0
            >>> x.expr='  -2  +3.5'
            >>> x.calculate
            1.5
            >>> x.expr='4+3.65-2 /2'
            >>> x.calculate
            6.65
            >>> x.expr=' 23 / 12 - 223 +      5.25 * 4    *      3423'
            >>> x.calculate
            71661.91666666667
            >>> x.expr='   2   - 3         *4'
            >>> x.calculate
            -10.0
            >>> x.expr=' 3 *   (        ( (10 - 2*3)))'
            >>> x.calculate
            12.0
            >>> x.expr=' 8 / 4  * (3 - 2.45      * (  4- 2 ^   3)) + 3'
            >>> x.calculate
            28.6
            >>> x.expr=' 2   *  ( 4 + 2 *   (5-3^2)+1)+4'
            >>> x.calculate
            -2.0
            >>> x.expr='2.5 + 3 * ( 2 +(3.0) *(5^2 - 2*3^(2) ) *(4) ) * ( 2 /8 + 2*( 3 - 1/ 3) ) - 2/ 3^2'
            >>> x.calculate
            1442.7777777777778
            >>> x.expr="4++ 3 +2"
            >>> x.calculate
            'error message'
            >>> x.expr="4    3 +2"
            >>> x.calculate
            'error message'
            >>> x.expr='(2)*10 - 3*(2 - 3*2)) '
            >>> x.calculate
            'error message'
            >>> x.expr='(2)*10 - 3*/(2 - 3*2) '
            >>> x.calculate
            'error message'
            >>> x.expr=')2(*10 - 3*(2 - 3*2) '
            >>> x.calculate
            'error message'
        '''

        if not isinstance(self.expr,str) or len(self.expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack=Stack()

        expr = self.postfix(self.expr)
        if expr != 'error message':         # checks if postfix could return valid notation
            exprList = expr.split()
        else:
            return expr
        for i in exprList:
            if self.isNumber(i):            # number is encountered
                calcStack.push(i)
            elif i == '+':                              # addition
                a = calcStack.pop()
                b = calcStack.pop()
                calcStack.push(float(b) + float(a))
            elif i == '-':                              # subtraction
                a = calcStack.pop()
                b = calcStack.pop()
                calcStack.push(float(b) - float(a))
            elif i == '*':                              # multiplication
                a = calcStack.pop()
                b = calcStack.pop()
                calcStack.push(float(b) * float(a))
            elif i == '/':                              # division
                a = calcStack.pop()
                b = calcStack.pop()
                calcStack.push(float(b) / float(a))
            elif i == '^':                              # exponent
                a = calcStack.pop()
                b = calcStack.pop()
                calcStack.push(float(b) ** float(a))
        return float(calcStack.peek())
