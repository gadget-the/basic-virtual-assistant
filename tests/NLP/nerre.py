import nltk, spacy
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tree import Tree
from nltk import ne_chunk, word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer#, PorterStemmer, LancasterStemmer
# from nltk.stem.snowball import SnowballStemmer
# from nltk.tokenize import PunktSentenceTokenizer

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('omw-1.4')

def nnExt(sent = ""):
    words = nltk.word_tokenize(sent)
    tagged = nltk.pos_tag(words)
    enti = []

    for i, item in enumerate(tagged):
        # if item[1] in ["PRP", "NN", "NNP", "NNS", "NNPS"]:
        if item[1] == "PRP" or "NN" in item[1]:
            #print(tagged[i - 1][0] + item[0])
            main = item[0]
            preF = ""
            sufF = ""

            # if tagged[i - 1][1] in ["PRP$", "JJ", "JJS", "JJR"]:
            if tagged[i - 1][1] == "PRP$" or "JJ" in tagged[i - 1][1]:
                preF = tagged[i - 1][0] + " "
                del tagged[i - 1]

            if i < len(tagged) - 1 and tagged[i + 1][1] == "POS":
                sufF = "" + tagged[i + 1][0] + " " + tagged[i + 2][0]
                del tagged[i + 2]
                del tagged[i + 1]

            enti.append(preF + main + sufF)

    return enti


def rootExt(sent=""):
    words = nltk.word_tokenize(sent)
    tagged = nltk.pos_tag(words)
    lemmata = WordNetLemmatizer()
    rel = []

    for i, item in enumerate(tagged):
        # if item[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
        if 'VB' in item[1]:
            # rel.append(item[0])
            rel.append(lemmata.lemmatize(item[0], 'v'))

    return rel

def neExt(sent = ""):
    words = nltk.word_tokenize(sent)
    tagged = nltk.pos_tag(words)
    chunked = ne_chunk(tagged)
    ne = []

    for subtree in chunked:
        if type(subtree) == Tree:
            thing = (subtree.label(), subtree.leaves()[0][0])
            if thing not in ne:
                ne.append(thing)
      
    return ne

def relExt(sent="", relations=[]):
    '''outputs a list of triples(length-3 tuples) containing sets of words that match the specified relation formats.'''
    words = word_tokenize(sent)
    tagged = pos_tag(words)
    chunked = ne_chunk(tagged)
    out = []

    for i, subtree in enumerate(chunked): # go through each labeled word
        if type(subtree) == Tree: # if it's one of interest(i.e a Named Entity)
            for n in relations: # check for each inputed relation formats
                t = word_tokenize(n[1])
                if subtree.label() == n[0]: # check if the word has the label specified in the relation format
                    matching = [x for x, y in zip(t, tagged[i + 1:i + len(t) + 1]) if x == y[0]] # compare the relation format with the words following the current one
                    if len(matching) == len(t): # if all of the words match
                        if type(chunked[i + len(t) + 1]) == Tree: # check if the word folloing the matching words is a word of interest
                            if chunked[i + len(t) + 1].label() == n[2]: # if the word has the label specified in the relation format
                                out.append((subtree.leaves()[0][0], n[1], chunked[i + len(t) + 1].leaves()[0][0])) # add a triple(length-3 tuple) with the first word, the matching relation format, and the following word

    return out

def relExt2(sent="", relations=[]):
    '''(sort of hacked together version of the other one that uses spacy instead of nltk) outputs a list of triples(length-3 tuples) containing sets of words that match the specified relation formats.'''
    NER = spacy.load("en_core_web_sm")
    chunked = NER(sent)
    entities = chunked.ents
    entitiesStr = [str(i) for i in chunked.ents]
    # print(entities)
    out = []

    for i, word in enumerate(chunked): # go through each labeled word
        if str(word) in entitiesStr:
            for n in relations: # check for each inputed relation formats
                t = word_tokenize(n[1])
                if entities[entitiesStr.index(str(word))].label_ == n[0]: # check if the word has the label specified in the relation format
                    matching = [x for x, y in zip(t, [str(i) for i in chunked[i + 1:i + len(t) + 1]]) if x == y] # compare the relation format with the words following the current one
                    if len(matching) == len(t): # if all of the words match
                        if str(chunked[i + len(t) + 1]) in entitiesStr:
                            if entities[entitiesStr.index(str(chunked[i + len(t) + 1]))].label_ == n[2]: # if the word has the label specified in the relation format
                                out.append((str(word), n[1], str(chunked[i + len(t) + 1]))) # add a triple(length-3 tuple) with the first word, the matching relation format, and the following word

    return out

def speakerStemRelExt(sent=""):
    words = word_tokenize(sent)
    tagged = pos_tag(words)
    # NER = spacy.load("en_core_web_sm")
    # chunked = NER(sent)
    # entities = [str(i) for i in chunked.ents]
    out = []
    
    for i, (word, tag) in enumerate(tagged):
        if tag == "PRP$":
            if word.lower() == "my":# grab "my" and the words following it that are possessive or "the object of possession"
                # print(tagged[i:])
                current = [word, tagged[i + 1][0]]
                t = tagged[i + 1:]
                # print(t)
                for n, m in enumerate(t): # an undoubtedly inefficient way to go about doing this
                    if m[1] == "POS" or t[n - 1][1] == "POS":
                        current.append(m[0])
                    # else:
                    #     break
                # out.append(tuple(current))
                out.append(TreebankWordDetokenizer().detokenize(current))
        elif tag == "POS":# get the non="my" ones
            if i < len(tagged):
                if not any(tagged[i - 1][0] in x for x in out):
                    # out.append((tagged[i - 1][0], word, tagged[i + 1][0]))
                    out.append(TreebankWordDetokenizer().detokenize([tagged[i - 1][0], word, tagged[i + 1][0]]))

    return out

if __name__ == "__main__":
    tests = [
        "Erica likes Paris.",
        "The old cat ran to Stacy.",
        "I sat on the table.",
        "All the kids sat on tables.",
        "Janet is my sister.",
        "Janet's sister is Erica.",
        "I like cats.",
        "Jamie has a cat named Sprinkles.",
        "I want cookies, cake, and doughnuts.",
        "Janet works at the Tesco down the road.",
        "Erica works at The Dollar Store.",
        "I woke up at 8:00 A.M.",
        "I woke up at eight a.m. today.",
        "My favorite website is youtube.com.",
        "I was thinking about naming my cat Jessie.",
        "I went to the store the other day.",
        "I fell off my bed.",
        "I put my cat in the other room.",
        "Erica's sister, Courtney, went to the concert with us.",
        "Erica went to Paris.",
        "My sister's boyfriend's brother went to the Bahamas last month.",
        "My sister and my brother went to the Bahamas last month.",
        "I saw Linda's son at the shop, today."
    ]
    inSent = tests[-1]

    # rootWords = []
    # ps = PorterStemmer()
    # rootWords = [ps.stem(x) for x in words]
    # ls = LancasterStemmer()
    # rootWords = [ls.stem(x) for x in words]
    # enSS = SnowballStemmer("english")
    # rootWords = [enSS.stem(x) for x in words]
    # lemmata = WordNetLemmatizer()
    # rootWords = [lemmata.lemmatize(x, 'v') for x in words]

    relations = [
        ('PERSON', "'s sister, ", 'PERSON'),
        ('PERSON', "'s brother, ", 'PERSON'),
        ('PERSON', "'s sibling, ", 'PERSON'),
        ('PERSON', "'s sister is", 'PERSON'),
        ('PERSON', "'s brother is", 'PERSON'),
        ('PERSON', "'s sibling is", 'PERSON'),
        ('PERSON', "went to", 'GPE'),
        ('PERSON', "works at", 'GPE'),
        ('PERSON', "'s boss, ", 'PERSON'),
        ('PERSON', "'s boss is", 'PERSON')
    ]

    # words = word_tokenize(inSent)
    # tagged = pos_tag(words)

    # nn = nnExt(inSent)
    # root = rootExt(inSent)
    # ne = neExt(inSent)
    # nnNEShared = [i[1] for i in ne if i[1] in nn]
    # rel = relExt(inSent, relations)
    # rel2 = relExt2(inSent, relations)
    # rel3 = speakerStemRelExt(inSent)

    # print(inSent)
    # print(words, tagged)
    # print("nn:", nn)
    # print("root:", root)
    # print("ne:", ne)
    # print("nn and ne common:", nnNEShared)
    # print("rel:", rel)
    # print("rel2:", rel2)
    # print("speakerStemRelExt:", rel3)
    
    for i in tests:
        words = word_tokenize(i)
        tagged = pos_tag(words)

        nn = nnExt(i)
        root = rootExt(i)
        ne = neExt(i)
        nnNEShared = [i[1] for i in ne if i[1] in nn]
        rel = relExt(i, relations)
        rel2 = relExt2(i, relations)
        rel3 = speakerStemRelExt(i)

        print(i)
        print("tokenize:", words)
        print("pos tag:", tagged)
        print("nn:", nn)
        print("root:", root)
        print("ne:", ne)
        print("nn and ne common:", nnNEShared)
        print("rel:", rel)
        print("rel2:", rel2)
        print("speakerStemRelExt:", rel3)
        print("\n")

'''
POS tag list:
    CC	coordinating conjunction
    CD	cardinal digit
    DT	determiner
    EX	existential there (like: "there is" ... think of it like "there exists")
    FW	foreign word
    IN	preposition/subordinating conjunction
    JJ	adjective	'big'
    JJR	adjective, comparative	'bigger'
    JJS	adjective, superlative	'biggest'
    LS	list marker	1)
    MD	modal	could, will
    NN	noun, singular 'desk'
    NNS	noun plural	'desks'
    NNP	proper noun, singular	'Harrison'
    NNPS	proper noun, plural	'Americans'
    PDT	predeterminer	'all the kids'
    POS	possessive ending	parent\'s
    PRP	personal pronoun	I, he, she
    PRP$	possessive pronoun	my, his, hers
    RB	adverb	very, silently,
    RBR	adverb, comparative	better
    RBS	adverb, superlative	best
    RP	particle	give up
    TO	to	go 'to' the store.
    UH	interjection	errrrrrrrm
    VB	verb, base form	take
    VBD	verb, past tense	took
    VBG	verb, gerund/present participle	taking
    VBN	verb, past participle	taken
    VBP	verb, sing. present, non-3d	take
    VBZ	verb, 3rd person sing. present	takes
    WDT	wh-determiner	which
    WP	wh-pronoun	who, what
    WP$	possessive wh-pronoun	whose
    WRB	wh-abverb	where, when

https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/
    rule: "extract the subject/object along with its modifiers, compound words and also extract the punctuation marks between them"
    rule: "To extract the relation, we have to find the ROOT of the sentence (which is also the verb of the sentence)"

    "The 22-year-old recently won ATP Challenger tournament."

    nsubj = "old"
    root = "won"
    dobj = "tournament"

    to get the entities in their entirety, we must follow the rule regarding modifiers and compound words
    making the first entity "22-year-old", and the second entity "ATP Challenger tournament"

    we're also left with the root/verb of the sentence, which is the relation between the two(though I wonder how adverbs would affect this)

    as a triple it would be:
    ("22-year-old", "won", "ATP Challenger tournament")

    of course, these rules only work for sentences with one subject and one object
        i suppose one could apply a similar thing to the verb/root as is done for the entities

nnExt
    extracts nouns and their modifiers(adjectives, possesives, and some other things)

rootExt
    extracts the root verb(only for single clause sentences?)

neExt
    extracts named entities
    outputs them with their label

relExt
    returns triples of relations based on a list of relation formats and the input sentence
    relation formats require a named entity label, a string of words that goes between them, and a second named entity label, like: ('PERSON', "'s sister, ", 'PERSON') or ('PERSON', "went to", 'GPE')

relExt2
    basically the same thing as relExt, except it uses spacy instead of nltk for the ner
    a little janky, as i essentially just rearranged/modified the code for the other one(might want to remake it, from scratch)

speakerStemRelExt
    a "relation extractor" based on the idea of having the speaker as the "root"
    it basically just checks for "my"(maybe other possessive pronouns?) and checks the words after it for possessives
        'My sister's boyfriend's brother went to the Bahamas last month.' --> ["My sister's boyfriend's brother"]
        'My sister and my brother went to the Bahamas last month.' --> ['My sister', 'my brother']
    it will also output possesive sets in lieu of a possessive pronouns
'''