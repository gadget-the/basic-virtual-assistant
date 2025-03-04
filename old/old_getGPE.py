from nltk import word_tokenize, ne_chunk, pos_tag#, tokenize
from nltk.tree import Tree

def getGPE(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    #prev = None
    nameEnts = []
    current = []

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == 'GPE':
            current.append(" ".join([t[0] for t in subtree.leaves()]))
        elif current:
            named_entity = " ".join(current)
            if named_entity not in nameEnts:
                nameEnts.append(named_entity)
                current = []
        else:
            continue

    return nameEnts
    # code that used to be in the weather part of the intEntFilter, before I replaced this function
    # if inp[-1] not in ["?", ".", "!"]:
    #     inp = inp + "?"

    # loc = None
    # cc = getGPE(inp) # try to extract the location from the input(i might want to redo this, perhaps incorporate all of the following code/process)
    # # print(inp, cc)

    # if cc:
    #     if len(cc) > 1: # adds a comma if the location has more than one word
    #         loc = ", ".join(cc)
    #     else:
    #         loc = cc[0]
    # else:  # if we weren't able to get the location from the original text we capitalize the first letter of everyword, then try again
    #     # print([x[0].upper() + x[1:] for x in inp.lower().split(" ")])
    #     inpLi = inp.lower().split(" ")
    #     for i, l in enumerate(inpLi):
    #         inpLi[i] = l.title()
    #     newInp = " ".join(inpLi)

    #     cc = getGPE(newInp)

    #     if cc:
    #         if cc[0].lower() == "weather":
    #             cc.remove(cc[0])

    #     if cc:
    #         if len(cc) > 1:# if there is more than one word in the location, we combine them with ", "
    #             loc = ", ".join(cc)
    #         else:
    #             loc = cc[0]