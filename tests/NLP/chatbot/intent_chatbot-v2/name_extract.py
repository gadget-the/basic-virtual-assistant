import json, spacy, nltk, re#, requests, bs4 as bs
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.tree import Tree
from nltk.tokenize import MWETokenizer

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('stopwords')

NER = spacy.load("en_core_web_sm")
tokenizer = MWETokenizer([("Mr", "."), ("Mrs", "."), ("Ms", "."), ("Mx", "."), ("Dr", "."), ("Hon", "."), ("Prof", "."), ("Rev", "."), ("St", "."), ("Gen", ".")], "")
english_stopwords = stopwords.words('english')

# first_names = bs.BeautifulSoup(requests.get('https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes').content, 'html.parser').text.split("\n") + bs.BeautifulSoup(requests.get('https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/first%20names/all.txt').content, 'html.parser').text.split("\n")
# last_names = bs.BeautifulSoup(requests.get('https://raw.githubusercontent.com/arineng/arincli/master/lib/last-names.txt').content, 'html.parser').text.split("\n") + bs.BeautifulSoup(requests.get('https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/surnames/all.txt').content, 'html.parser').text.split("\n") + bs.BeautifulSoup(requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Miscellaneous/security-question-answers/common-surnames.txt').content, 'html.parser').text.split("\n")
# last_names += ["Brentwood"]

with open('tests\\NLP\\names.json', 'r') as fp:
    names_ = json.load(fp)

first_names = names_['first-names']
last_names = names_['last-names']

# d = {}
# d['first_names'] = first_names
# d['last_names'] = last_names

# with open('tests/names.json', 'w') as fp:
#     json.dump(d, fp)

def nameExt(inStr = ""):
    # print(inStr)
    chunked = ne_chunk(pos_tag(word_tokenize(inStr)))
    # print(chunked)
    pers = []
    # newStr = str(inStr)

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == "PERSON":
            # print(subtree.leaves()[0][0])
            if not (subtree.leaves()[0][0] in pers):
                name = subtree.leaves()[0][0]
                if name in last_names:
                    pers.append((name, "last"))
                elif name in first_names:
                    pers.append((name, "first"))
                else:
                    pers.append(name)
                
    return pers

def nameExt2(inStr = ""):
    pers = []

    for item in word_tokenize(inStr):
        if item in last_names:
            pers.append((item, "last"))
        elif item in first_names:
            pers.append((item, "first"))
        # else:
        #     pers.append(item)

    return pers

def name_extract(input_string = ""):
    ''' Version Three\n\nExtracts each name as one string.\n\nAttempts to get the first, last, and middle names(can get initials).\n\nAlso gets titles and suffixes. '''
    titles = ["mr.", "mrs.", "miss", "ms.", "mx.", "dr.", "doctor", "sir", "hon.", "prof.", "rev.", "st.", "gen.", "saint", "king", "queen", "lord", "lady"] # https://www.btb.termiumplus.gc.ca/tpv2guides/guides/wrtps/index-eng.html?lang=eng&lettr=indx_catlog_a&page=9NBnYuQ324Yc.html
    suffixes = ["esq.", "md", "phd", "ba", "ma", "junior", "jr.", "sr.", "senior", "bt.", "bart", "lmft", "dd"]
    roman_numeral_letters = ["I", "V", "X", "L", "C", "D", "M"]
    # words = word_tokenize(input_string)
    words = tokenizer.tokenize(word_tokenize(input_string))
    # words = word_tokenize(re.sub(r'[^\w\s]', '', input_string))
    # words = [word for word in words if word.isalnum()]
    # words = [word for word in words if word.isalnum() or (word.lower() in titles or word.lower() in suffixes)]
    # words = [word for word in words if word.isalnum() or (len(word) > 1 and word.endswith('.'))]
    # words = [x for x in words if x not in english_stopwords]
    # print(words)
    tagged = pos_tag(words)
    chunked = ne_chunk(tagged)
    names = []

    # spacy_tagged = [word.text for word in NER(input_string).ents if str(word.label_) == "PERSON"]
    # print(spacy_tagged)

    for i, (word, subtree, tag) in enumerate(zip(words, chunked, tagged)):
        # print(i, word, subtree, tag)
        if (type(subtree) == Tree) and (subtree.label() == "PERSON"): # get all the words labeled as PERSON entities
            if not any(word in x.split(" ") for x in names):
                if words[i - 1].lower() in titles: # check for titles
                    name = words[i - 1] + " " + word
                    for n, x in enumerate(names): # combine names if this name is already partially extracted
                        if words[i - 1] in x.split(" "):
                            name = names.pop(n) + " " + word
                            break

                    names.append(name)

                elif words[i - 1] in first_names:# check for first name prior
                    name = words[i - 1] + " " + word
                    for n, x in enumerate(names):
                        if words[i - 1] in x.split(" "):
                            name = names.pop(n) + " " + word
                            break

                    names.append(name)

                elif (i < len(words) - 1) and (words[i + 1].lower() in suffixes): # check for suffixes
                    name = word + " " + words[i + 1]
                    for n, x in enumerate(names):
                        if words[i + 1] in x.split(" "):
                            name = word + " " + names.pop(n)
                            break

                    names.append(name)

                else:
                    name_parts = [str(x[0]) for x in subtree.leaves()]
                    if len(name_parts) > 1:
                        names.append(" ".join(name_parts))

                    else:
                        names.append(word)
                    # names.append(word)

        else: # attempt to get the words that despite not being labeled names, are probably still names
            if 'NN' in tag[1]:
                if (i > 0) and (word[0] == word[0].upper()) and (words[i - 1].lower() in titles): # check if the word is capitalized and preceded by a title
                    if words[i - 1] in names:
                        names.append(names.pop(-1) + " " + word)

                    else:
                        names.append(words[i - 1] + " " + word)

                elif (i > 0) and (word[0] == word[0].upper()) and (words[i - 1] in first_names): # check for first name prior
                    # print(word)
                    # if words[i - 1] in names:
                    if (len(names) > 0) and (words[i - 1] == names[-1].split(" ")[-1]):
                        names.append(names.pop(-1) + " " + word)

                    else:
                        names.append(words[i - 1] + " " + word)

                elif (word in first_names) or (word in last_names): # might cause some false positives but it works
                    # if any(words[i - 1] in n for n in names):
                    # if len(names) > 0 and words[i - 1] in names[-1]:
                    if (len(names) > 0) and (words[i - 1] == names[-1].split(" ")[-1]):
                        names.append(names.pop(-1) + " " + word)

                    else:
                        names.append(word)

                elif (i < len(words) - 1) and (word[0] == word[0].upper()) and (words[i + 1].lower() in suffixes): # check if the word is capitalized and followed by a suffix
                    if words[i + 1] in names:
                        names.append(word + " " + names.pop(-1))

                    else:
                        names.append(word + " " + words[i + 1])

                # elif (i > 0) and (words[i - 1] in last_names) and (word.upper() == word) and all(letter in roman_numeral_letters for letter in word): # if the previous word is a last name, the current word is all capitalized, and it's only comprised of roman numeral letters
                elif (i > 0) and (words[i - 1] in last_names) and all(letter in roman_numeral_letters for letter in word): # if the previous word is a last name, and it's only comprised of roman numeral letters
                    if words[i - 1] == names[-1].split(" ")[-1]: # if the previous word is the same as the last name of the most recent name in the output
                        names.append(names.pop(-1) + " " + word)

                    else:
                        names.append(words[i - 1] + " " + word)

    # go through and combine the middle name duplicates, if there are any(there's probably a better way to do this)
    for _ in names: # do this process multiple times, definitely a better way to do this
        for i, name in enumerate(names):
            if i > 0:
                previous_name_split = names[i - 1].split(" ")
                if (len(previous_name_split) > 1) and (previous_name_split[-1] == name.split(" ")[0]): # if the last name in the previous element is the same as the first name in this element
                        combined_name = names[i - 1].split(" ")[:-1] + name.split(" ")
                        names.remove(names[i - 1])
                        names.insert(i - 1, " ".join(combined_name))
                        names.remove(name)
    
    # a deeper duplicate remover, might cause problems?
    for name in names:
        list_without_name = list(names)
        list_without_name.remove(name)
        # print(p)
        if any(name in m for m in list_without_name):
            names.remove(name)
    
    return names


if __name__ == "__main__":
    tests = [
        'Dwayne Johnson went to the store with Kari Byron.',
        'Mr. Johnson told me a story the other day.',
        'Mr. Johnson went to the store with his wife, Linda Johnson.',
        'Dr. Williams told me to get more exercise.',
        'Dr. Lane-Rogers assigned the class an individual project.',
        'Arnold Palmer hit a great shot.',
        'I was hanging out with my friend, Johnny.',
        'His name was John Douglass.',
        'I met Jacob Blake the other day.',
        'Mr. Proud was at the soccer game today.',
        'Mrs. Hillwig works at Tesco now.',
        'James and I went to the movies last week.',
        'His name was Chris Lee Davidson',
        'Erik Washer was a total hunk.',
        'Mrs. Dubai went downtown.',
        'Christopher Ashton Kutcher is an actor.',
        'Laura Jeanne Reese Witherspoon is an actress',
        'Christie Anne Dunnam was an author.',
        'Christopher Ashton Kutcher met Christie Anne Dunnam at a party.',
        'Christopher Ashton Kutcher and Laura Jeanne Reese Witherspoon are both actors.',
        'Caleb Casey McGuire Affleck is an actor.',
        'Kathy is turning 28.',
        "Christie Anne Dunnam's sister is Kathy Dunnam.",
        'John is my brother',
        "My sister's name is Julie",
        'I met John Cena today.',
        'Today I saw John.',
        'I met James Arthur Jr. the other day.',
        "I interviewed Lauren L. Kendricks LMFT for a school project.",
        "I interviewed Lauren L. Kendricks, LMFT for a school project.",
        "I saw Jamie Johnson and Jamie Erikson at the mall the other day.", # picks up the " and " for some reason?
        "She was the wife of King Henry VIII.",
        "B.B. King is performing tonight.", # doesn't pick up "B.B."
        "BB King is performing tonight.", # doesn't pick up "BB"
        "B B King is performing tonight.", # works
        "Francis Scott Key Fitzgerald was an American novelist, essayist, short story writer, and screenwriter."
    ]

    for i in tests:
        print(i)
        print("V1", nameExt(i))
        print("V2", nameExt2(i))
        print("V3", name_extract(i))
        print("\n")

    # t = word_tokenize("Mr.")
    # print([i.replace("|", "") for i in tokenizer.tokenize(word_tokenize('Mr.'))])
    # print(tokenizer.tokenize(word_tokenize('Dr.')))
    # print(english_stopwords, "and" in english_stopwords)
    # print("\u02bb")


'''
the goal is to extract names from an input text.

nameExt
    uses nltk to recognize named entities of 'PERSON' type
    it then attempts to give them a "last" or "first" name label based on if they're in a list of names(scraped from the internet)
    this doesn't work super well
        it doesn't always pick out every name
        it tends to mislabel names
        the concept of middle names is lost on it
        titles don't effect the label for a name

nameExt2
    only uses the first name and last name lists to check for a name
    it gives it a label, and something's not in either of the lists it doesn't get extracted
    this doesn't work all that well
        tends to mislabel names
        picks out "I" as a name?
        titles still don't effect the label for a name
        middle names can't be picked out

nameExt3
    uses a combination of nltk's ner, the name lists, and checking previous words to pick out whole names

    goes through each word and checks if it's a "PERSON" entity
    if so it checks if it's still in the output, checks if it is preceded by a title or a first name, and adds the combined output(combining titles/names) to the output list
    if not, it checks if it's a noun, it then again checks the preceding word for titles and first names, it then outputs the combined
    
    after that in order to get middle names, it first uses the subtree leaves thing for nltk's ner
    if that doesn't work, the middle names are lumped together with the first and last name separately as a byproduct of the previous steps(i.e. ['Christopher Ashton'. 'Ashton Kutcher'])
    so to put them together it loops through the output list and compares each one with the one before it, if the first name of the current name == the last name of the previous name it combines them in the output
    after all that it removes duplicates(some of which happen as a result of the leaves thing)

    this works pretty well most of the time
        it doesn't label names, though it combines them for the output
        it most likely won't pick out "I" as a name accidentally
        it gets titles
        middle names are picked out(even when there are more than one)
        it doesn't always get each name(i could try using spacy's ner instead of nltk's, or a combination of the two)
            'Caleb Casey McGuire Affleck is an actor.' --> ['Caleb Casey McGuire'] In this instance, it is probably because 'McGuire' is not a in the first names list(This has since been fixed)
        i'm sure that there is a possible problem w/ the way i combine the middle names in for the output(what if someone has the same last name as someone else's first name? ['John James', 'James Jacobs'])


    problems/examples
        'Christopher Ashton Kutcher met Christie Anne Dunnam at a party.'
            it works for multiple n-length names, n > 2

        'His name was Chris Lee Davidson'
            used the tree/leaves thing to work this out
        'Christopher Ashton Kutcher is an actor.'
            made a second for loop to recombine names like this as they were outputed like: ['Christopher Ashton'. 'Ashton Kutcher']
        'Laura Jeanne Reese Witherspoon is an actress'
            put the new for loop in another for loop to combine names that aren't in just one loop, ['Laura Jeanne Reese', ' Reese Witherspoon']
        'Kathy is turning 28.' => ['Kathy']
            added an additional check for if the word was in the first or last names lists
        'Caleb Casey McGuire Affleck is an actor.' => ['Affleck', 'Caleb Casey McGuire'], now ['Caleb Casey McGuire Affleck']
            at first it didn't pick out 'Affleck', but when i added the additional check it did. 
                Still doesn't combine the names into one. 
            Fixed it? made a change to the additional check that might cause problems for certain other cases
        "Christie Anne Dunnam's sister is Kathy Dunnam." => ['Christie Anne Dunnam'], now ['Christie Anne Dunnam', 'Kathy Dunnam'], now ['Kathy Dunnam', 'Kathy', 'Christie Anne Dunnam']
            at first, only picked out 'Christie Anne Dunnam' and not 'Kathy Dunnam'
            i changed some stuff and got it to pick out both names
            then i ran the code a second time, after changing nothing, and then it outputed ['Kathy Dunnam', 'Kathy', 'Christie Anne Dunnam']
            then i created a "deeper duplicate remover" to get rid of the duplicate that appeared for some reason
        'I met John Cena today.' => ['John Cena today']
            this is because it checks for first names before nouns, and 'Cena' is in the first names list
            not sure how I should fix this
                I could try removing 'Cena' from the first name list, but I kind of want to find a way to avoid this(that would cause it to not be classified as a first name even when it should)
            ended up fixing it by checking for capitalization
            
        'Today I saw John'
            this is because i don't check if the index is more than 1 when checking the noun thing
            fixed by adding a 'i > 0' check to two of the checks in the noun check part

        'I saw Jamie Johnson and Jamie Erikson at the mall the other day.' => ['Jamie Johnson and Jamie Erikson']
            not sure what I changed to cause this

            it seems to be due to the code I added to catch the full(-er) names from subtrees
                name_parts = [str(x[0]) for x in subtree.leaves()]
                if len(name_parts) > 1:
                    names.append(" ".join(name_parts))
                else:
                    names.append(word)

            was going to try using spacy to supplement/replace nltk in it, in order to remedy the problem
                spacy doesn't catch certain things, and might end up making things a bit more difficult/complicated
                    misses some parts of names and even names due to punctuation

                    I'm sure it's probably simple stuff that I could fix the same way I did with nltk(perhaps a version 4, built around Spacy?)

                it does catch some things better than nltk(and even better the stuff I built around nltk?)

                i also keeps possessives?
                    'Christie Anne Dunnam's sister is Kathy Dunnam.' => ["Christie Anne Dunnam's", 'Kathy Dunnam']

        'I interviewed Lauren L. Kendricks, LMFT for a school project.' => ['Lauren L. Kendricks']
            i caught the "LMFT" before
            not sure what I changed to cause this
            if there isn't a comma between the last name and the postnominal title, it gets picked up
                maybe I should remove punctuation? that might cause some problems
'''