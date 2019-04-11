class Parse:

    def __init__(self):
        print("hello from Talha Yılmaz :)")

    def preapareRuleList(self):
        grammar = open('cfg.txt')
        lines = grammar.readlines()
        rules = []
        for l in lines:
            if l != '\n' and l[0] != '#':
                l_tokens = l.split()

                for token in l_tokens:
                    # ignore comments in grammar
                    if '#' in token:
                        l_tokens = l_tokens[0:l_tokens.index(token)]
                        break

                if(len(l_tokens) == 3):
                    rules.append(l_tokens)
        return rules

    def preapareVocabularyList(self):
        grammar = open('cfg.txt')
        lines = grammar.readlines()
        vocabulary = []
        for l in lines:
            if l != '\n' and l[0] != '#':
                l_tokens = l.split()

                for token in l_tokens:
                    # ignore comments in grammar
                    if '#' in token:
                        l_tokens = l_tokens[0:l_tokens.index(token)]
                        break

                if (len(l_tokens) == 2):
                    vocabulary.append(l_tokens)

        return vocabulary

    def prepareNonterminalsFromSentence(self, sentence):
        vocabulary = self.preapareVocabularyList()
        non_terminal_sentence = []
        words = sentence.split()

        for word in words:
            for vocabItem in vocabulary:
                if word in vocabItem:
                    non_terminal_sentence.append(vocabItem[0].strip())
                    break

        return non_terminal_sentence

    def union(self, downwardElement, diagonalElement):
        unionArray = []

        if downwardElement == "":
            unionArray.append(diagonalElement.strip())

        for dwn in downwardElement.split():
            if diagonalElement == "":
                unionArray.append(dwn.strip())
            for dgn in diagonalElement.split():
                if dgn == "":
                    unionArray.append(dwn.strip())
                else:
                    unionArray.append(dwn.strip() + " " + dgn.strip())
        return unionArray

    def getRuleIfExistInRules(self, union_result_list):
        rules = self.preapareRuleList()
        rule_result = ""
        for rule in rules:
            for union_result in union_result_list:
                if union_result != "" and union_result == rule[1] + " " + rule[2]:
                    rule_result += rule[0].strip() + " "

        return rule_result.strip()

    def parseFirstRowOfCYKTable(self, non_terminal_sentence, table):
        table_size = len(non_terminal_sentence)
        for i in range(table_size):
            table[0][i] = non_terminal_sentence[i]
        return table

    def parseOtherRowsOfCYKTable(self, table, currentWidth, currentHeight):
        width=currentWidth
        height=currentHeight

        diagonalResultList = []
        for x in range(0, currentHeight):
            result = table[height-1][width+1]
            height -= 1
            width += 1
            diagonalResultList.append(result)

        downwardResultList = []
        for y in range(0, currentHeight):
            result = table[y][currentWidth]
            downwardResultList.append(result)

        finalresult = ""
        for z in range(0, len(diagonalResultList)):
            union_result_list = self.union(downwardResultList[z], diagonalResultList[z])
            finalresult += self.getRuleIfExistInRules(union_result_list) + " "

        #this part is done to fix an internal bug
        formed_finalresult = ""
        for formed_word in finalresult.split():
            formed_finalresult += formed_word.strip() + " "
        formed_finalresult = formed_finalresult.strip()

        table[currentHeight][currentWidth] = formed_finalresult.strip()

        return table

def main():
    parse = Parse()
    sentencesFile = open('sentence.txt')
    sentences = sentencesFile.readlines()

    for sentence in sentences:
        non_terminal_sentence = parse.prepareNonterminalsFromSentence(sentence)

        table_size = len(non_terminal_sentence)
        table = [["" for x in range(table_size)] for y in range(table_size)]

        table = parse.parseFirstRowOfCYKTable(non_terminal_sentence, table)

        currentWidth = 0
        currentHeight = 1
        for ch in range(currentHeight, table_size):
            for cw in range(currentWidth, table_size-currentHeight):
                table = parse.parseOtherRowsOfCYKTable(table, cw, ch)
            currentHeight += 1

        sentence = sentence.strip()

        print("Sentence is: " + sentence)
        print(table)

        if "S" in table[table_size-1][0] and sentence.endswith("."):
            print("Sentence is gramatically correct")
        elif "S" in table[table_size - 1][0] and sentence.endswith("!"):
            print("Sentence is gramatically correct")
        elif "S" in table[table_size - 1][0] and sentence.endswith("?") and sentence.startswith("is it true that"):
            print("Sentence is gramatically correct")
        else:
            print("Sentence is not gramatically correct")


if __name__ == "__main__":
    main()