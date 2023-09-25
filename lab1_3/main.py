class expression:
    pass


coefs = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2']


def arcCountMaxArg(exp, flag, temp=2):
    if isinstance(exp, MatrixCoef):
        if exp.exp is None:
            return temp
        else:
            return arcCountMaxArg(exp.exp, flag, temp)

    elif isinstance(exp, arcMax):
        maxCount = temp
        if (flag == True):
            c = len(exp.args)
        else:
            c = temp
        for arg in exp.args:
            maxCount = max(maxCount, c, arcCountMaxArg(arg, flag, maxCount))
        return maxCount

    elif isinstance(exp, arcSum):
        maxCount = temp
        if (flag == False):
            c = len(exp.args)
        else:
            c = temp
        for arg in exp.args:
            maxCount = max(maxCount, c, arcCountMaxArg(arg, flag, maxCount))
        return maxCount


def DiscloseMax(exp1, exp2):
    # print("exp1= ",exp1 , " exp2=", exp2)
    if isinstance(exp1.exp, arcMax) and exp2.exp is None:
        new_args = []
        for arg in exp1.exp.args: new_args.append(arg)
        new_args.append(exp2)
        return MatrixCoef(None, arcMax(new_args))

    elif isinstance(exp1.exp, arcMax) and isinstance(exp2.exp, arcMax):
        new_args = []
        for arg in exp1.exp.args: new_args.append(arg)
        for arg in exp2.exp.args: new_args.append(arg)
        return MatrixCoef(None, arcMax(new_args))

    else:
        return MatrixCoef(None, arcMax([exp1.exp, exp2.exp]))


class arcMax(expression):
    def __init__(self, args):
        self.args = args

    def __str__(self):
        t = f"(arcMax{len(self.args)} "
        for arg in self.args: t += f"{str(arg)} "
        t = t[:-1] + ")"
        return t


def DiscloseSum(exp, newCoefficient, flag=True):
    if isinstance(exp, MatrixCoef):
        if isinstance(exp.exp, arcMax):
            return MatrixCoef(None, DiscloseSum(exp.exp, newCoefficient, False))
        elif exp.exp is None:
            if flag:
                return MatrixCoef(None, arcSum([exp, newCoefficient]))
            else:
                return arcSum([exp, newCoefficient])
        else:
            return
    elif isinstance(exp, arcMax):
        newArgs = []
        for arg in exp.args:
            newArgs.append(DiscloseSum(arg, newCoefficient, flag))
        return arcMax(newArgs)
    elif isinstance(exp, arcSum):
        return arcSum(exp.args + [newCoefficient])

class arcSum(expression):
    def __init__(self, args):
        self.args = args

    def __str__(self):
        t = f"(arcSum{len(self.args)} "
        for arg in self.args: t += f"{str(arg)} "
        t = t[:-1] + ")"
        return t

class MatrixCoef(expression):
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def __str__(self):
        if self.exp is None:
            return self.name
        else:
            return str(self.exp)

class Interpret:
    def __init__(self, Name, Arg, IsFunc):
        self.name = Name
        self.arg = Arg
        self.isFunc = IsFunc

    def maxNumberArc(self, flag):
        return max(arcCountMaxArg(self.a1, flag),
                   arcCountMaxArg(self.a2, flag),
                   arcCountMaxArg(self.a3, flag),
                   arcCountMaxArg(self.a4, flag),
                   arcCountMaxArg(self.b1, flag),
                   arcCountMaxArg(self.b2, flag))

    def setCoef(self, A1, A2, A3, A4, B1, B2):
        self.a1 = A1
        self.a2 = A2
        self.a3 = A3
        self.a4 = A4
        self.b1 = B1
        self.b2 = B2
        self.nameA = str(A1)
        self.nameB = str(A2)
        self.nameC = str(A3)
        self.nameD = str(A4)
        self.nameE = str(B1)
        self.nameF = str(B2)

    def __str__(self):
        if self.isFunc:
            resStr = f"{self.name}({str(self.arg)},"
            resStr = resStr[:-1]
            resStr += ')'
            return resStr
        else:
            return self.name

    def createTreeComposition(self, currentDict, amountCoef):
        new_dict = currentDict.copy()
        coefIndex = amountCoef
        if self.isFunc:
            if self.arg.isFunc:
                res = self.arg.createTreeComposition(currentDict, amountCoef)
                new_dict.update(res[0])
                coefIndex = res[1]
                if self.name not in new_dict:
                    coefIndex += 1
                    curA1 = MatrixCoef(f"a1{coefIndex}", None)
                    curA2 = MatrixCoef(f"a2{coefIndex}", None)
                    curA3 = MatrixCoef(f"a3{coefIndex}", None)
                    curA4 = MatrixCoef(f"a4{coefIndex}", None)
                    curB1 = MatrixCoef(f"b1{coefIndex}", None)
                    curB2 = MatrixCoef(f"b2{coefIndex}", None)
                else:
                    entFromHist = new_dict[self.name]
                    curA1 = MatrixCoef(entFromHist.nameA, None)
                    curA2 = MatrixCoef(entFromHist.nameB, None)
                    curA3 = MatrixCoef(entFromHist.nameC, None)
                    curA4 = MatrixCoef(entFromHist.nameD, None)
                    curB1 = MatrixCoef(entFromHist.nameE, None)
                    curB2 = MatrixCoef(entFromHist.nameF, None)

                self.nameA = str(curA1)
                self.nameB = str(curA2)
                self.nameC = str(curA3)
                self.nameD = str(curA4)
                self.nameE = str(curB1)
                self.nameF = str(curB2)
                self.a1 = DiscloseMax(DiscloseSum(self.arg.a1, curA1), DiscloseSum(self.arg.a3, curA2))
                self.a2 = DiscloseMax(DiscloseSum(self.arg.a2, curA1), DiscloseSum(self.arg.a4, curA2))
                self.a3 = DiscloseMax(DiscloseSum(self.arg.a1, curA3), DiscloseSum(self.arg.a3, curA4))
                self.a4 = DiscloseMax(DiscloseSum(self.arg.a2, curA3), DiscloseSum(self.arg.a4, curA4))
                self.b1 = DiscloseMax(DiscloseMax(DiscloseSum(self.arg.b1, curA1), DiscloseSum(self.arg.b2, curA2)),
                                      curB1)
                self.b2 = DiscloseMax(DiscloseMax(DiscloseSum(self.arg.b1, curA3), DiscloseSum(self.arg.b2, curA4)),
                                      curB2)
                if self.name not in new_dict:
                    new_dict[self.name] = self
            else:
                if self.name in new_dict:
                    entFromHist = new_dict[self.name]
                    self.setCoef(MatrixCoef(entFromHist.nameA, None), MatrixCoef(entFromHist.nameB, None),
                                 MatrixCoef(entFromHist.nameC, None), MatrixCoef(entFromHist.nameD, None),
                                 MatrixCoef(entFromHist.nameE, None), MatrixCoef(entFromHist.nameF, None))
                else:
                    coefIndex += 1
                    self.setCoef(MatrixCoef(f"a1{coefIndex}", None),
                                 MatrixCoef(f"a2{coefIndex}", None),
                                 MatrixCoef(f"a3{coefIndex}", None),
                                 MatrixCoef(f"a4{coefIndex}", None),
                                 MatrixCoef(f"b1{coefIndex}", None),
                                 MatrixCoef(f"b2{coefIndex}", None))
                    new_dict[self.name] = self
        return new_dict, coefIndex

    def makeTree(self, hist, numOfCoefficients):

        resTree, resNumOfCoefficients = self.createTreeComposition(hist, numOfCoefficients)

        return resTree, resNumOfCoefficients, self.maxNumberArc(True), self.maxNumberArc(False)


class Rule_lexer:
    def __init__(self, lines):
        self.funcs = []
        self.LeftRightFuncPair = []
        self.tree = {}
        self.amountCoef = 0
        self.maxMax = 2
        self.maxSum = 2
        for line in lines:
            left = self.insertBrackets(line[0])

            right = self.insertBrackets(line[1])

            resTree, resNumOfCoefficients, maxM, maxS = left.makeTree(self.tree, self.amountCoef)
            self.tree.update(resTree)
            self.amountCoef = resNumOfCoefficients
            self.maxMax = max(self.maxMax, maxM)
            self.maxSum = max(self.maxSum, maxS)
            resTree, resNumOfCoefficients, maxM, maxS = right.makeTree(self.tree, self.amountCoef)

            self.tree.update(resTree)
            self.amountCoef = resNumOfCoefficients
            self.maxMax = max(self.maxMax, maxM)
            self.maxSum = max(self.maxSum, maxS)

            self.funcs.append([left, right])
            self.LeftRightFuncPair.append({left.a1: right.a1, left.a2: right.a2, left.a3: right.a3, left.a4: right.a4, left.b1: right.b1, left.b2: right.b2})


    def insertBrackets(self, line):
        if len(line) == 1:
            return Interpret(line, Interpret("x", None, False), True)
        else:
            return Interpret(line[0], self.insertBrackets(line[1:]), True)


    def generateFormSMT(self):
        result = []
        for i in range(3, self.maxMax + 1):
            args = [f"x{j}" for j in range(1, i + 1)]
            define = f"(define-fun arcMax{i} ("
            for arg in args: define += f"({arg} Int) "
            ar = ' '.join(args[1:])
            define = define[:-1]
            result.append(
                define + f") Int (ite (> {args[0]} (arcMax{i - 1} {ar})) {args[0]} (arcMax{i - 1} {ar})))")

        for i in range(3, self.maxSum + 1):
            args = [f"x{j}" for j in range(1, i + 1)]
            define = f"(define-fun arcSum{i} ("
            for arg in args: define += f"({arg} Int) "
            ar = ' '.join(args[1:])
            define = define[:-1]
            result.append(
                define + f") Int (ite (= {args[0]} -1) {args[0]} (ite (= (arcSum{i - 1} {ar}) -1) (arcSum{i - 1} {ar}) (+ {args[0]} (arcSum{i - 1} {ar})))))")


        for i in range(1, self.amountCoef + 1):
            for name in coefs:
                result.append(f"(declare-fun {name}{i} () Int)")
        for pair in self.LeftRightFuncPair:
            for first, second in pair.items():
                result.append(f"(assert (>> {first} {second}))")
        for i in range(1, self.amountCoef + 1):
            for name in coefs:
                if name != 'a1' and name != 'b1':
                    result.append(f"(assert (or (>= {name}{i} 0) (= {name}{i} -1)))")
                else:
                    result.append(f"(assert (>= {name}{i} 0))")
        return result


smtBegin = [
    "(set-logic QF_NIA)",
    "(define-fun arcMax2 ((x1 Int) (x2 Int)) Int (ite (> x1 x2) x1 x2))",
    "(define-fun arcSum2 ((x1 Int) (x2 Int)) Int (ite (= x1 -1) x1 (ite (= x2 -1) x2 (+ x1 x2))))",
    "(define-fun >> ((a Int) (b Int)) Bool (or (> a b) (and (= a -1) (= b -1))))"
]

smtEnd = [
    "(check-sat)",
    "(get-model)"
]


def main():
    lines = []
    filename = "input2.txt"
    # filename = input()
    with open(filename) as file:
        while data := file.readline():
            data = data.replace(' ', '')
            data = data.replace('\n', '')
            data = data.split("->")
            lines.append(data)
    print(lines)

    parsed = Rule_lexer(lines)

    smtStrings = parsed.generateFormSMT()

    smtStrings = smtBegin + smtStrings + smtEnd

    with open("output.smt2", "w") as f:
        for line in smtStrings:
            f.write(line + "\n")

if __name__ == '__main__': main()
