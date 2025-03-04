import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from name_extract import name_extract

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def nameRepl(inStr = ""):
    # print(inStr)
    chunked = ne_chunk(pos_tag(word_tokenize(inStr)))
    # print(chunked)
    pers = []
    newStr = str(inStr)

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == "PERSON":
            # print(subtree.leaves()[0][0])
            if subtree.leaves()[0][0] not in pers:
                pers.append(subtree.leaves()[0][0])
    # print(pers)

    for i, name in enumerate(pers):
        newStr = newStr.replace(name, "{n" + str(i) + "}")
    
    return newStr

def name_replace(input_string):
    out = str(input_string)
    names = name_extract(input_string)

    for i, name in enumerate(names):
        out = out.replace(name, "{n" + str(i) + "}")
    
    return out

if __name__ == "__main__":
    # strin = 'Erica Brentwood went to the store.'
    test_string = 'Mr. Johnson went to the store with his wife, Linda Johnson.'

    print(test_string)
    print("\n")

    x = nameRepl(test_string)
    print(x)
    # print(x.format(n0 = "Jamie", n1 = "Anderson"))
    print(x.format(n0 = "Jamie", n1 = "Anderson", n2 = "Aurelia", n3 = "Anderson"))
    print("\n")

    x1 = name_replace(test_string)
    print(x1)
    # print(x1.format(n0 = "Jamie Anderson"))
    print(x1.format(n0 = "Jamie Anderson", n1 = "Aurelia Anderson"))

    # print("Hello %s and %s" % ("Erica", "Jamie"))