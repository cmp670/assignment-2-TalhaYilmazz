from random import randint

class Randsentence:

    def __init__(self):
        print("hello from Talha Yılmaz :)")

    def sentence_generator(self, rules, symbol, non_terminal, sentence):
        matching_rules = []

        if symbol not in non_terminal:
            sentence.append(symbol)

        else:
            # o anki satır için tüm kuralları tarıyoruz, satırın non-terminali ile eşleşen rule varsa yeni bir listeye atıyoruz
            for rule in rules:
                if rule[0] == symbol:
                    matching_rules.append(rule)
            r = randint(0, len(matching_rules)-1)

            # select rule according to the number generated and probabilities calculated
            apply_rule = matching_rules[r]

            for s in apply_rule[1:len(apply_rule)]:
                self.sentence_generator(rules, s, non_terminal, sentence)

def main():
    randsentence = Randsentence()
    grammar = open('cfg.txt')
    writtenFile = open('random-sentence.txt','w')
    lines = grammar.readlines()
    rules = []
    non_terminal = []
    for l in lines:
        if l != '\n' and l[0] != '#':
            l_tokens = l.split()

            for token in l_tokens:
                # ignore comments in grammar
                if '#' in token:
                    l_tokens = l_tokens[0:l_tokens.index(token)]
                    break

            non_terminal.append(l_tokens[0])
            rules.append(l_tokens)

    sentence_list = []
    sentence = []
    randsentence.sentence_generator(rules,'ROOT',non_terminal, sentence)
    sentence_list.append(' '.join(sentence))

    print(sentence_list)
    writtenFile.write(' '.join(sentence))
    writtenFile.close()

if __name__ == "__main__":
    main()