from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from numpy import pi
import re

def list2str(lst = [], sep = " "):
    ''' converts each element in a list to a string, separated by a specified string '''
    lst = list(lst)

    for i, el in enumerate(lst):
        lst[i] = str(el)
    
    return sep.join(lst)

def parser(n = "", lst = False, op = True):
    ''' essentially a custom word2num '''
    simples = { # dictionary for looking up the simpler conversions, 1-20, and the tens up to 90
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90
    }
    modifs = { # modifiers, basically multiples of ten or orders of magnitude;are used to muliply previous numbers or be stand alone("two hundred" and "one trillion")
        "millionths": 0.000001,
        "thousandths": 0.001,
        "hundredths": 0.01,
        "tenths": 0.1,
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        "billion": 1000000000,
        "trillion": 1000000000000
    }
    operators = { # math operators, need to work out how to do ones that require multiple words to convey;"four divided by two" or "twelve multiplied by ten"
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided": "/",
        "squared": "**2",
        "cubed": "**3"
    }
    signs = {
        "negative": -1,
        "positive": 1
    } # have to multiply the following number by the sign
    ordinals = {
        "zeroth": (0, "th"),
        "first": (1, "st"),
        "second": (2, "nd"),
        "third": (3, "rd"),
        "fourth": (4, "th"),
        "fifth": (5, "th"),
        "sixth": (6, "th"),
        "seventh": (7, "th"),
        "eighth": (8, "th"),
        "ninth": (9, "th"),
        "tenth": (10, "th"),
        "eleventh": (11, "th"),
        "twelfth": (12, "th"),
        "thirteenth": (13, "th"),
        "fourteenth": (14, "th"),
        "fifteenth": (15, "th"),
        "sixteenth": (16, "th"),
        "seventeenth": (17, "th"),
        "eighteenth": (18, "th"),
        "nineteenth": (19, "th"),
        "twentieth": (20, "th"),
        "thirtieth": (30, "th"),
        "fortieth": (40, "th"),
        "fiftieth": (50, "th"),
        "sixtieth": (60, "th"),
        "seventieth": (70, "th"),
        "eightieth": (80, "th"),
        "ninetieth": (90, "th")
    }
    ordinalsMod = {
        "hundredth": (100, "th"),
        "thousandth": (1000, "th"),
        "millionth": (1000000, "th"),
        "billionth": (1000000000, "th"),
        "trillionth": (1000000000000, "th")
    }
    out = []

    # [n := n.lower().replace(i, operators[i]) for i in operators if i in n]

    words = []
    n = n.replace(",", "")
    for t in word_tokenize(n.lower()):
        # print(t)
        if len(t) > 2 and t[-3].isdigit():
            n = t[-2:]
            if n == "th" or n == "nd" or n == "st":
                words.append(t.replace(n, ""))
                words.append(n)
            else:
                words.append(t)
        else:
            words.append(t)

    # words = word_tokenize(n.lower().replace(",", ""))
    for i, w in enumerate(words):# goes through every word level token(splitting at spaces mostly works here, but not in every case)
        if w.isdigit() or (w[0] == "-" and w[1].isdigit):# if it's a number already, let it pass through; might want to do something different for checking negatives
            if i > 0 and str(out[-1]) in signs:# if the previous is in the signs dict, multiply the current by it's number version
                out.append(int(w) * signs[out.pop(-1)])
            else:
                out.append(int(w))
        elif w in simples:# if it's in the simples dictionary, convert it using that
            if i > 0 and str(out[-1]) in signs:# if the previous is in the signs dict, multiply the current by it's number version
                out.append(simples[w] * signs[out.pop(-1)])
            else:
                out.append(simples[w])
        elif "-" in w:# if it's hyphenated, convert it at a smaller level then add the total
            current = 0
            ending = ""
            for m in w.split("-"):
                if m in simples:
                    current += simples[m]
                elif m in ordinals:
                    current += ordinals[m][0]
                    ending = ordinals[m][1]

            if current:
                if ending:
                    out.extend((current, ending))
                else:
                    out.append(current)
            else:
                out.extend(w.split("-"))
        elif w in modifs:# if it's in the modifs dictionary, multiply the last number by its number version
            out.append(int(out.pop(-1)) * modifs[w])
        elif w in signs:# if it's in the signs dictionary let it pass
            out.append(w)
        elif w in operators and op:# if it's an operator, convert it using the dictionary
            if w == 'divided':
                if words[i + 1] == 'by':
                    words[i + 1] = '`&&THISISAPLACEHOLDERSTRING&&`'
                out.append(operators[w])
            else:
                out.append(operators[w])
        elif w in ordinals:
            # out.append(ordinals[w])
            out.extend(ordinals[w])
        elif w in ordinalsMod:
            if type(out[-1]) == int or out[-1].isdigit():
                out.extend((int(out.pop(-1)) * ordinalsMod[w][0], ordinalsMod[w][1]))
            else:
                out.extend(ordinalsMod[w])
        elif w == '`&&THISISAPLACEHOLDERSTRING&&`':
            pass
        else:# if it can't be converted using the previous methods, let it pass
            out.append(w)

    # print(out)
    ind1 = None
    ind2 = None
    while not ind1 and ind1 != 0: # "compound numbers", essentially numbers like 145,002
        for i, n in enumerate(out):
            if not ind1 and ind1 != 0: # if index 1 hasn't been set, check if the current element is an int or float that is evenly divisible by 10
                if type(n) == int or type(n) == float:
                    if n % 10 == 0:
                        ind1 = i
                    else:
                        continue
                else:
                    continue
            else: # if index 1 has been set, check if the current element is an int/float that isn't evenly divisible by 10. if so, set index 2 to the current index
                if type(n) == int or type(n) == float:
                    # print(type(out[i + 1]))
                    if n % 10 != 0:
                        ind2 = i
                        break
                else:#if not, set index two to the previous index
                    ind2 = i - 1
                    break
        
        # print(out)
        if ind1 == ind2: # if the indices weren't able to have been set, stop the process entirely
            break

        if (bool(ind1) or ind1 == 0) and bool(ind2):# if the indices have been set, combine the numbers between the indices and reset
            # print("one", str(ind1), str(out[ind1]))
            # print("two", str(ind2), str(out[ind2]))
            # print("one", str(ind1), bool(ind1))
            # print("two", str(ind2), bool(ind2))
            out[ind1] = sum(out[ind1:ind2 + 1])
            del out[ind1 + 1:ind2 + 1]
            ind1 = None
            ind2 = None
        else:
            break

    if lst:
        return out
    else:
        # return list2str(out)
        return TreebankWordDetokenizer().detokenize(str(i) for i in out)

# def parser2(n = "", lst = False, op = True):
#     simples = { # dictionary for looking up the simpler conversions, 1-20, and the tens up to 90
#         "zero": 0,
#         "one": 1,
#         "two": 2,
#         "three": 3,
#         "four": 4,
#         "five": 5,
#         "six": 6,
#         "seven": 7,
#         "eight": 8,
#         "nine": 9,
#         "ten": 10,
#         "eleven": 11,
#         "twelve": 12,
#         "thirteen": 13,
#         "fourteen": 14,
#         "fifteen": 15,
#         "sixteen": 16,
#         "seventeen": 17,
#         "eighteen": 18,
#         "nineteen": 19,
#         "twenty": 20,
#         "thirty": 30,
#         "forty": 40,
#         "fifty": 50,
#         "sixty": 60,
#         "seventy": 70,
#         "eighty": 80,
#         "ninety": 90
#     }
#     modifs = { # modifiers, basically multiples of ten or orders of magnitude;are used to muliply previous numbers or be stand alone("two hundred" and "one trillion")
#         "millionths": 0.000001,
#         "thousandths": 0.001,
#         "hundredths": 0.01,
#         "tenths": 0.1,
#         "hundred": 100,
#         "thousand": 1000,
#         "million": 1000000,
#         "billion": 1000000000,
#         "trillion": 1000000000000
#     }
#     operators = { # math operators, need to work out how to do ones that require multiple words to convey;"four divided by two" or "twelve multiplied by ten"
#         "plus": "+",
#         "minus": "-",
#         "times": "*",
#         "divided": "/",
#         "squared": "**2",
#         "cubed": "**3"
#     }
#     signs = {
#         "negative": -1,
#         "positive": 1
#     } # have to multiply the following number by the sign
#     ordinals = {
#         "zeroth": (0, "th"),
#         "first": (1, "st"),
#         "second": (2, "nd"),
#         "third": (3, "rd"),
#         "fourth": (4, "th"),
#         "fifth": (5, "th"),
#         "sixth": (6, "th"),
#         "seventh": (7, "th"),
#         "eighth": (8, "th"),
#         "ninth": (9, "th"),
#         "tenth": (10, "th"),
#         "eleventh": (11, "th"),
#         "twelfth": (12, "th"),
#         "thirteenth": (13, "th"),
#         "fourteenth": (14, "th"),
#         "fifteenth": (15, "th"),
#         "sixteenth": (16, "th"),
#         "seventeenth": (17, "th"),
#         "eighteenth": (18, "th"),
#         "nineteenth": (19, "th"),
#         "twentieth": (20, "th"),
#         "thirtieth": (30, "th"),
#         "fortieth": (40, "th"),
#         "fiftieth": (50, "th"),
#         "sixtieth": (60, "th"),
#         "seventieth": (70, "th"),
#         "eightieth": (80, "th"),
#         "ninetieth": (90, "th")
#     }
#     ordinalsMod = {
#         "hundredth": (100, "th"),
#         "thousandth": (1000, "th"),
#         "millionth": (1000000, "th"),
#         "billionth": (1000000000, "th"),
#         "trillionth": (1000000000000, "th")
#     }
#     conversions = []

#     words = []
#     for t in word_tokenize(n.lower()):
#         if t.replace(",", ""):
#             t = t.replace(",", "")
#         if len(t) > 2 and t[-3].isdigit():
#             n = t[-2:]
#             if n == "th" or n == "nd" or n == "st":
#                 words.append(t.replace(n, ""))
#                 words.append(n)
#         else:
#             words.append(t)

#     for i, word in enumerate(words):
#         if isNumber(word): # if it's a number already, let it pass through
#             conversions.append(word)
#         elif word in simples:
#             conversions.append(simples[word])
#         elif "-" in word:# if it's hyphenated, convert it at a smaller level then add the total
#             current = 0
#             ending = ""
#             for m in word.split("-"):
#                 if m in simples:
#                     current += simples[m]
#                 elif m in ordinals:
#                     current += ordinals[m][0]
#                     ending = ordinals[m][1]

#             if current:
#                 if ending:
#                     conversions.extend((current, ending))
#                 else:
#                     conversions.append(current)
#             else:
#                 conversions.extend(word.split("-"))
#         elif word in signs:
#             conversions.append('sign&' + str(signs[word]))
#         elif word in operators and op:# if it's an operator, convert it using the dictionary
#             if word == 'divided':
#                 if words[i + 1] == 'by':
#                     words[i + 1] = '`&&THISISAPLACEHOLDERSTRING&&`'
#                 conversions.append(operators[word])
#             else:
#                 conversions.append(operators[word])
#         elif word in ordinals:
#             conversions.extend(ordinals[word])

#         elif word in modifs:# if it's in the modifs dictionary, multiply the last number by its number version
#             # out.append(int(out.pop(-1)) * modifs[word])
#             conversions.append("modif&" + str(modifs[word]))
#         elif word in ordinalsMod:
#             if type(conversions[-1]) == int or conversions[-1].isdigit():
#                 conversions.extend(("modif&" + str(ordinalsMod[word][0]), ordinalsMod[word][1]))
#             else:
#                 conversions.extend(ordinalsMod[word])

#         elif word == '`&&THISISAPLACEHOLDERSTRING&&`': # catch the place holder string
#             pass
#         else:
#             conversions.append(word)

#     firstPass = []
#     i = 0
#     while i < len(conversions):
#         word = str(conversions[i])
#         print(word, firstPass)
#         if isNumber(word):
#             firstPass.append(int(word))
#         elif 'modif&' in word:
#             firstPass.append(firstPass.pop(-1) * int(word.replace('modif&', '')))
#             # i -= 1
#         else:
#             firstPass.append(word)

#         if len(firstPass) > 1:
#             if isNumber(firstPass[-1]) and isNumber(firstPass[-2]):
#                 firstPass.append(firstPass.pop(-1) + firstPass.pop(-1))

#         i += 1

#     out = []
#     for i, x in enumerate(firstPass):
#         print(x)
#         if 'sign&' in str(x) and isNumber(firstPass[i + 1]):
#             out.append(firstPass[i + 1] * int(x.replace('sign&', '')))
#             firstPass[i + 1] = '`&&THISISAPLACEHOLDERSTRING&&`'
#             # firstPass[i] = '`&&THISISAPLACEHOLDERSTRING&&`'
#         elif x == '`&&THISISAPLACEHOLDERSTRING&&`':
#             pass
#         else:
#             out.append(x)

#     if lst:
#         return out
#     else:
#         return TreebankWordDetokenizer().detokenize(str(i) for i in out)

def parser2(input_string = "", output_as_list = False, convert_operators = True):
    ''' essentially a custom word2num '''
    simples = { # dictionary for looking up the simpler conversions, 1-20, and the tens up to 90
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90
    }
    modifs = { # modifiers, basically multiples of ten or orders of magnitude;are used to muliply previous numbers or be stand alone("two hundred" and "one trillion")
        "millionths": 0.000001,
        "thousandths": 0.001,
        "hundredths": 0.01,
        "tenths": 0.1,
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        "billion": 1000000000,
        "trillion": 1000000000000
    }
    operators = { # math operators, need to work out how to do ones that require multiple words to convey;"four divided by two" or "twelve multiplied by ten"
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided": "/",
        "squared": "**2",
        "cubed": "**3"
    }
    ordinals = {
        "zeroth": (0, "th"),
        "first": (1, "st"),
        "second": (2, "nd"),
        "third": (3, "rd"),
        "fourth": (4, "th"),
        "fifth": (5, "th"),
        "sixth": (6, "th"),
        "seventh": (7, "th"),
        "eighth": (8, "th"),
        "ninth": (9, "th"),
        "tenth": (10, "th"),
        "eleventh": (11, "th"),
        "twelfth": (12, "th"),
        "thirteenth": (13, "th"),
        "fourteenth": (14, "th"),
        "fifteenth": (15, "th"),
        "sixteenth": (16, "th"),
        "seventeenth": (17, "th"),
        "eighteenth": (18, "th"),
        "nineteenth": (19, "th"),
        "twentieth": (20, "th"),
        "thirtieth": (30, "th"),
        "fortieth": (40, "th"),
        "fiftieth": (50, "th"),
        "sixtieth": (60, "th"),
        "seventieth": (70, "th"),
        "eightieth": (80, "th"),
        "ninetieth": (90, "th")
    }
    ordinalsMod = {
        "hundredth": (100, "th"),
        "thousandth": (1000, "th"),
        "millionth": (1000000, "th"),
        "billionth": (1000000000, "th"),
        "trillionth": (1000000000000, "th")
    }
    conversion_list = []

    # spliting ordinal figures using digits
    words = []
    input_string = input_string.replace(",", "") # remove commas
    for token in word_tokenize(input_string.lower()):
        if (len(token) > 2) and token[-3].isdigit(): # if the token ends with th, nd, or st, add it and it's ending to the words list. else, just add it to the list
            ending = token[-2:]
            if ending == "th" or ending == "nd" or ending == "st":
                words.append(token.replace(ending, ""))
                words.append(ending)

            else:
                words.append(token)

        else:
            words.append(token)

    for i, word in enumerate(words): # go through every word level token(splitting at spaces mostly works here, but not in every case)
        if word.isdigit() or (word[0] == "-" and word[1].isdigit): # if it's a number already, let it pass
            conversion_list.append(int(word))

        elif word in simples: # if it's in the simples dictionary, convert it using that
            conversion_list.append(simples[word])

        elif ("-" in word) and (word[0] != "-"): # if it's hyphenated(not negative), convert it at a smaller level then add the total
            current = 0
            ending = ""
            for m in word.split("-"):
                if m in simples:
                    current += simples[m]

                elif m in ordinals:
                    current += ordinals[m][0]
                    ending = ordinals[m][1]

            if current:
                if ending:
                    conversion_list.extend((current, ending))

                else:
                    conversion_list.append(current)

            else:
                conversion_list.extend(word.split("-"))

        elif word in modifs: # if it's in the modifs dictionary, multiply the last number by its number version
            conversion_list.append(int(conversion_list.pop(-1)) * modifs[word])

        elif word == "negative": # if the word is "negative", append a negative one to the list
            conversion_list.append(-1)

        elif convert_operators and (word in operators): # if it's an operator, convert it using the dictionary
            if word == 'divided':
                if words[i + 1] == 'by':
                    words[i + 1] = '`&&THISISAPLACEHOLDERSTRING&&`'
                conversion_list.append(operators[word])

            else:
                conversion_list.append(operators[word])

        elif word in ordinals:
            conversion_list.extend(ordinals[word])

        elif word in ordinalsMod:
            if (type(conversion_list[-1]) == int) or isNumber(conversion_list[-1]):
                conversion_list.extend((int(conversion_list.pop(-1)) * ordinalsMod[word][0], ordinalsMod[word][1]))

            else:
                conversion_list.extend(ordinalsMod[word])

        elif word == '`&&THISISAPLACEHOLDERSTRING&&`':
            pass # ignore the place holder string

        else: # if it can't be converted using the previous methods, let it pass
            conversion_list.append(word)

    # print(conversion_list)
    index1 = None
    index2 = None
    while not index1 and index1 != 0: # "compound numbers", essentially numbers like 145,002
        for i, element in enumerate(conversion_list):
            if not index1 and index1 != 0: # if index 1 hasn't been set, check if the current element is an int or float that is evenly divisible by 10
                if type(element) == int or type(element) == float:
                    if element % 10 == 0:
                        index1 = i
                    else:
                        continue
                else:
                    continue
            else: # if index 1 has been set, check if the current element is an int/float that isn't evenly divisible by 10. if so, set index 2 to the current index
                if type(element) == int or type(element) == float:
                    if element % 10 != 0:
                        index2 = i
                        break
                else: # if not, set index two to the previous index
                    index2 = i - 1
                    break
        
        # print(conversion_list)
        if index1 == index2: # if the indices weren't able to have been set, stop the process entirely
            break

        if (bool(index1) or index1 == 0) and bool(index2): # if the indices have been set, combine the numbers between the indices and reset
            conversion_list[index1] = sum(conversion_list[index1:index2 + 1])
            del conversion_list[index1 + 1:index2 + 1]
            index1 = None
            index2 = None
        else:
            break

    # go through and apply the negatives, after combining the "compound numbers"
    output_list = []
    for i, element in enumerate(conversion_list):
        # print(element)
        if i > 0:
            # if (conversion_list[i - 1] == -1) and (type(element) == int or type(element) == float):
            if (conversion_list[i - 1] == -1) and isNumber(element):
                output_list.append(element * -1)
            else:
                if element != -1:
                    output_list.append(element)
        else:
            if element != -1:
                output_list.append(element)
        # print(output_list)

    if output_as_list:
        return output_list
    else:
        return TreebankWordDetokenizer().detokenize(str(i) for i in output_list)

def isNumber(n = None):
    if type(n) == int:
        return n
    elif type(n) == float:
        return n
    elif type(n) == str:
        if (n.replace("-", "").isdigit()) or n.isdigit():
            if "." in n:
                return float(n)
            else:
                return int(n)
    else:
        return None

def stutterZip(n = []):
    return zip(n, [n[i + 1] if i < len(n) - 1 else "" for i, x in enumerate(n)])

def parsEval(n = ""):
    mth = parser(n, True)#use the number parser to convert the inputed words to numbers
    out = None

    for i, n in enumerate(mth):
        # print(n)
        if (type(n) != int) and (type(n) != float) and not (n in ["+", "-", "*", "/", "%", "^", "**", "sum", "and", "subtract"]): # if the current element is not a number or operator, set it to an empty string
            mth[i] = ""
        else:
            mth[i] = str(n)
    
    mth = [x for x in mth if x]

    # print(mth)
    if 'sum' in mth:
        mth.remove('sum')
        # print("+".join(["(" + "".join([y for y in x.split('_') if y]) + ")" for x in "_".join(mth).split("and")]))
        # print(eval("+".join(["(" + "".join([y for y in x.split('_') if y]) + ")" for x in "_".join(mth).split("and")])))
        out = sum([eval("".join([y for y in x.split('_') if y])) for x in "_".join(mth).split("and")])
    else:
        out = eval("".join(mth)) # evaluate the resulting string, I know this is still bad even though I filter the input str
    
    # out = eval("".join(mth)) # evaluate the resulting string, I know this is still bad even though I filter the input str
    return out

# def area_of_shape(shape = "", lengths = []):
#     # could just put the actual names of the dimensions for the arguments area_of_shape(shape = "", base = 0, height = 0, length = 0, width = 0, radius = 0)
#     area = None

#     if shape == 'triangle':
#         area = (lengths[0] * lengths[1])/2
#     elif shape == 'circle':
#         area = pi * pow(lengths[0], 2)
#     elif shape == 'parallelogram':
#         area = lengths[0] * lengths[1]
#     elif shape == 'trapezoid':
#         area = ((lengths[0] + lengths[1])/2)*lengths[2]
#     elif shape == 'rhombus':
#         area = (lengths[0] * lengths[1])/2
#     elif shape == 'ellipse':
#         area = pi * lengths[0] * lengths[1]
#     elif shape == 'pentagon':
#         area = pow(5 * (5 + (2*pow(5, 0.5))), 0.5)*pow(lengths[0], 2)/4
#     elif shape == 'hexagon':
#         area = 3*pow(3, 0.5)*pow(lengths[0], 2)/2
#     elif shape == 'heart':
#         area = pow(lengths[0], 2) + (pi * pow(lengths[0]/2, 2))

#     return area

def polygon_solver(shape = "", area = 0, base = 0, base2 = 0, height = 0, length = 0, width = 0, radius = 0, diagonal1 = 0, diagonal2 = 0, axis1 = 0, axis2 = 0, side = 0):
    output_value = 0

    if shape == 'square':
        if side and (not area):
            # output_value = pow(side, 2)
            output_value = side * side

        elif area and (not side):
            output_value = pow(area, 0.5)

    elif shape == 'rectangle':
        if (length and width) and (not area):
            output_value = length * width

        elif (area and width) and (not length):
            output_value = area / width

        elif (length and area) and (not width):
            output_value = area / length

    elif shape == 'triangle':
        if (base and height) and (not area): # find area from base and height
            output_value = (base * height) / 2

        elif (area and height) and (not base): # base from height and area
            output_value = (2 * area) / height

        elif (area and base) and (not height): # height from base and area
            output_value = (2 * area) / base

    elif shape == 'circle':
        if radius and (not area):
            output_value = pi * pow(radius, 2) # find area from radius

        elif area and (not radius):
            output_value = pow((area / pi), 0.5) # radius from area
        
        # not sure how i would do circumference

    elif shape == 'parallelogram':
        if (base and height) and (not area): # area from base and height
            output_value = base * height

        elif (area and height) and (not base): # base from height and area
            output_value = area / height

        elif (base and area) and (not height): # height from base and area
            output_value = area / base

    elif shape == 'trapezoid':
        if (base and base2 and height) and (not area): # area from base1, base2, and height
            output_value = (height * (base + base2)) / 2

        elif (base and base2 and area) and (not height): # height from area, base1, and base2
            output_value = (2 * area) / (base + base2)

        elif (height and base2 and area) and (not base): # base1 from area, height, and base2
            output_value = ((2 * area) / height) - base2

        elif (height and base and area) and (not base2): # base2 from area, height, and base1
            output_value = ((2 * area) / height) - base

    elif shape == 'rhombus':
        if (diagonal1 and diagonal2) and (not area): # area from diagonal1 and diagonal2
            output_value = (diagonal1 * diagonal2) / 2

        elif (area and diagonal2) and (not diagonal1): # diagonal1 from area and diagonal2
            output_value = (2 * area) / diagonal2

        elif (diagonal1 and area) and (not diagonal2): # diagonal2 from diagonal1 and area
            output_value = (2 * area) / diagonal1

    elif shape == 'ellipse':
        if (axis1 and axis2) and (not area): # find area from axis1 and axis2
            output_value = pi * axis1 * axis2

        if (area and axis2) and (not axis1): # axis1 from area and axis2
            output_value = area / (pi * axis2)

        if (axis1 and area) and (not axis2): # axis2 from area and axis1
            output_value = area / (pi * axis1)

    elif shape == 'pentagon':
        if side and (not area): # area from side
            output_value = pow(5 * (5 + (2 * pow(5, 0.5))), 0.5) * pow(side, 2) / 4

        if area and (not side): # side from area
            output_value = pow((4 * area) / pow(5 * (5 + (2 * pow(5, 0.5))), 0.5), 0.5)

    elif shape == 'hexagon':
        if side and (not area): # area from side
            output_value = 3 * pow(3, 0.5) * pow(side, 2) / 2

        if area and (not side): # side from area
            output_value = pow((2 * area) / (3 * pow(3, 0.5)), 0.5)

    # elif shape == 'heart':
    #     if not area:
    #         area = pow(lengths[0], 2) + (pi * pow(lengths[0]/2, 2))

    return output_value

def product_from_list(inLst = []):
    out = 1

    [out := out * x for x in inLst]

    return out

def digit2OrdinalFig(n = 0):
    out = ""
    if n == 0:
        out = "0th"
    else:
        if n == 1:
            out = "1st"
        elif n == 2:
            out = "2nd"
        elif n == 3:
            out = "3rd"
        elif n > 3 and  n <= 20: # 5th, 10th, 13th
            out = str(n) + "th"
        elif n > 20:
            if str(n)[-1] == "1": # 21st
                out = str(n) + "st"
            elif str(n)[-1] == "2": # 32nd
                out = str(n) + "nd"
            elif str(n)[-1] == "3": # 23rd
                out = str(n) + "rd"
            else:
                out = str(n) + "th"

    return out

if __name__ == "__main__":
    # print(parser("two plus two")) # convert operator words to their actual operator
    # print(parser("two times five"))
    # print(parser("twelve minus four"))
    # print(parser("eight minus 4"))
    # print(parser("twenty-two")) # convert hyphenated number words
    # print(parser("fifty-five"))
    # print(parser("seventy-nine"))
    # print(parser("seventy-something")) # interesting cases like this
    # print(parser("four hundred")) # convert increasing scales
    # print(parser("five thousand"))
    # print(parser("twelve million"))
    # print(parser("fourteen hundred"))
    # print(parser("five millionths")) # convert decreasing scales
    # print(parser("two thousandths"))
    # print(parser("twelve million four thousand eight hundred forty-two")) # convert compound numbers
    # print(parser("eight trillion forty-nine billion ninety-seven million three thousand four hundred fifty-seven"))
    # print(parser("Please pay thirty-four thousand four hundred fifty dollars")) # preserve the non-number words
    # print(parser("It costs four hundred dollars."))
    # print(parser("It costs four hundred fifty-five dollars."))
    # print(parser("twelve million four thousand eight hundred forty-two plus ten thousand twenty-eight")) # convert multiple compound numbers
    # print(parser("two hundred fifty-nine plus one thousand two hundred thirty-nine"))
    # print(parser("two hundred fifty-nine plus one thousand two hundred thirty-nine plus ten thousand twenty-eight"))
    # print(parser("She lived to be about one hundred twelve.")) # accounts for punctuation
    # print(parser("three thousand eight hundred forty-ninth")) # ordinal forms
    # print(parser("it was the five hundred fiftieth day"))
    # print(parser("seventeenth"))
    # print(parser("five thousandth"))
    # print(parser("twenty-seventh"))
    # print(parser("one thousandth"))
    # print(parser("1,000,000")) # commas removed
    # print(parser("1,000th"))

    # print(parsEval("two plus two"))
    # print(parsEval("what is two plus two?"))
    # print(parsEval("what is the answer for eighteen plus fourteen hundred?"))

    # print(parser("ten thousand 2 hundred twelve")) # problem with combination? "ten thousand two hundred twelve" works fine... Fixed it
    # print(parser("10 thousand two hundred 12"))

    # print(parser("negative seven hundred nineteen")) # problem with combining negative numbers

    # print(parser2("negative seven hundred nineteen")) # fixed negative numbers
    # print(parser2("seven hundred nineteen"))

    # print(parser2("negative twelve million four thousand eight hundred forty-two"))
    # print(parser2("twelve million four thousand eight hundred forty-two"))

    # print(parser2("negative five millionths"))
    # print(parser2("five millionths"))

    # print(parser2("what is negative five thousand plus negative 800"))
    # print(parser2("what is five thousand plus negative 800"))

    # print(parser2("what is negative five thousand plus negative eight hundred"))
    # print(parser2("what is five thousand plus eight hundred"))

    print(parser2("ten five")) # combines adjacent numbers that aren't meant to be; i kind of expected this problem
    print(parser2("ten, five, eight, and twenty"))

    while True:
        # print(parsEval(input("> ")))
        t = input("> ")
        print(parser2(t))
        # print()
        # print(parser(t))
        # print(parser(t, lst=True))

    # print(list2str([1 ,2 ,3, 4, 5]))
    # print("-5".isdigit())
    # print(TreebankWordDetokenizer().detokenize(['the', 'quick', 'brown', 'dog', "'s", 'coat', 'was', 'brown', '.']))
    # print(digit2OrdinalFig(421))
    # for i in range(101):
    #     print(digit2OrdinalFig(i))

    # n = "You are the 1,000th customer!"
    # m = []
    # n = n.replace(",", "")
    # for t in word_tokenize(n.lower()):
    #     if len(t) >= 3 and t[-3].isdigit():
    #         n = t[-2:]
    #         if n == "th" or n == "nd" or n == "st":
    #             # print(t[-2:], t[-3])
    #             # print(t)
    #             for i in t.split(n):
    #                 # print(i)
    #                 if i:
    #                     m.append(i)
    #                 else:
    #                     m.append(n)
    #     else:
    #         m.append(t)
    # print(m)

    # print(area_of_shape(shape='circle', lengths=[5]))
    # print(area_of_shape(shape='triangle', lengths=[5, 7]))
    # print(area_of_shape(shape='trapezoid', lengths=[5, 7, 8]))
    # print(area_of_shape(shape='ellipse', lengths=[5, 7]))
    # print(area_of_shape(shape='pentagon', lengths=[5]))
    # print(area_of_shape(shape='hexagon', lengths=[5]))
    # print(area_of_shape(shape='heart', lengths=[5]))

    # print(product_from_list([8, 9, 10, 13]))
    # print(pow(25, 1/2))
    
    # test = ["this", "is", "a", "test", "abcd1234"]
    # stutterList = [test[i + 1] if i < len(test) - 1 else "" for i, x in enumerate(test)]
    # print(test)
    # print(stutterList)
    # print(len(test), len(stutterList))

    # print(polygon_solver(shape='triangle', base=5, height=7)) # 17.5
    # print(polygon_solver(shape='circle', radius=5)) # ~78.54
    # print(polygon_solver(shape='parallelogram', base=5, height=7)) # 35
    # print(polygon_solver(shape='trapezoid', base=5, base2=7, height=8)) # 48.0
    # print(polygon_solver(shape='rhombus', diagonal1=5, diagonal2=7)) # 17.5
    # print(polygon_solver(shape='ellipse', axis1=5, axis2=7)) # ~109.96
    # print(polygon_solver(shape='pentagon', side=5)) # ~43.01
    # print(polygon_solver(shape='hexagon', side=5)) # ~64.95
    # print("\n")
    # print(polygon_solver(shape='triangle', base=5, area=17.5)) # ~7
    # print(polygon_solver(shape='triangle', height=7, area=17.5)) # ~5
    # print(polygon_solver(shape='circle', area=78.54)) # ~5
    # print(polygon_solver(shape='parallelogram', area=35, height=7)) # 5
    # print(polygon_solver(shape='parallelogram', area=35, base=5)) # 7
    # print(polygon_solver(shape='trapezoid', base2=7, height=8, area=48)) # 5
    # print(polygon_solver(shape='trapezoid', base=5, height=8, area=48)) # 7
    # print(polygon_solver(shape='trapezoid', base=5, base2=7, area=48)) # 8
    # print(polygon_solver(shape='rhombus', area=17.5, diagonal2=7)) # 5
    # print(polygon_solver(shape='rhombus', area=17.5, diagonal1=5)) # 7
    # print(polygon_solver(shape='ellipse', area=109.96, axis1=5)) # ~7
    # print(polygon_solver(shape='ellipse', area=109.96, axis2=7)) # ~5
    # print(polygon_solver(shape='pentagon', area=43.01)) # ~5
    # print(polygon_solver(shape='hexagon', area=64.95)) # ~5


    # https://www.geeksforgeeks.org/python-program-for-converting-roman-numerals-to-decimal-lying-between-1-to-3999/
    # https://www.tutorialspoint.com/roman-to-integer-in-python
    
    # test = [
    #     "King Henry VIII",
    #     "James Jona III",
    #     "MXII",
    #     "XX",
    #     "LMXI",
    #     "Super Bowl XLII",
    #     "Mariam L. Web III",
    #     "Mix the wet ingredients.",
    #     "MLXI"
    # ]

    # # roman_numeral_letters = ["I", "V", "X", "L", "C", "D", "M"]
    # roman_numeral_chart = {
    #     "I": 1,
    #     "V": 5,
    #     "X": 10,
    #     "L": 50,
    #     "C": 100,
    #     "D": 500,
    #     "M": 1000
    # }

    # for i in test:
    #     print(i)
    #     print(word_tokenize(i))
    #     # print([x for x in word_tokenize(i) if any(r in x for r in roman_numeral_chart)]) # only the words that contain the letters used in roman numerals
    #     # print([x for x in word_tokenize(i) if x.upper() == x]) # only the words that are all capitalized
    #     # print([x for x in word_tokenize(i) if re.sub(r'[^\w\s]', '', x) == x]) # only the words without punctuation
    #     # print([x for x in word_tokenize(i) if all(r in roman_numeral_chart for r in x)]) # only the words that contain only letters used in roman numerals; i think that this one works the best to extract them
    #     # print([x for x in word_tokenize(i) if all(r.upper() in roman_numeral_chart for r in x)]) # only the words that contain only letters used in roman numerals, case-insensitive
    #     # print()

    #     numeral_groups = []
    #     # print([x for x in word_tokenize(i) if all(r in roman_numeral_chart for r in x)])
    #     for word in word_tokenize(i):
    #         if all(letter in roman_numeral_chart for letter in word):
    #             numeral_groups.append(word)

    #     print(numeral_groups)

    #     for group in numeral_groups:
    #         group_value = 0
    #         print("start group")

    #         letter_values = [roman_numeral_chart[letter] for letter in group]
    #         print(letter_values)

    #         # is_valid = True
    #         # valid_combos = ["IV", "IX", "XL", "XC", "CD", "CM"]
    #         # invalid_combos = ["IIII", "VV", "XXXX", "CCCC", "DD"]
    #         # for i, letter in enumerate(group):
    #         #     if i < len(group) - 1:
    #         #         value = roman_numeral_chart[letter]
    #         #         if value < roman_numeral_chart[group[i + 1]]:
    #         #             if i > 0:
    #         #                 if not any(group[i - 1] + letter in c for c in valid_combos):
    #         #                     is_valid = False
    #         #             else:
    #         #                 is_valid = False
    #         #         elif any(group[i - 1] + letter in c for c in invalid_combos):
    #         #             is_valid = False
    #         # print(is_valid)

    #         for i, val in enumerate(letter_values):
    #             # print(val)
    #             if val > 1:
    #                 if (i > 0) and (i != len(letter_values) - 1):
    #                         if val > letter_values[i - 1]:
    #                             group_value += val - letter_values[i - 1]
                            
    #                         else:
    #                             group_value += val
    #                 else:
    #                     group_value += val
    #             else:
    #                 group_value += 1

    #         print("end group -", group_value, "\n")



'''
need to work out how to do the other operations


i should to avoid using the eval
i tried to ensure that the only things that go into the method are ints, floats, and strings with the operators in them(as well as empty strings)
but there might still be a danger in it? though, i'm not really planning on doing much public with this
maybe i should try my best to avoid using eval(), in order to build that habit


I think it would be cool to make a function that takes in the dimensions of a shape and based on what's missing(length, height, base, area, radius, etc.) it determines what to calculate and output
    I almost tried to do this sort of thing at one point while working on the area thing

    i can have it check what lengths were inputed, as well as which shape was specified

    https://socratic.org/questions/how-do-you-find-the-area-of-a-parallelogram-with-two-sides-and-an-angle
    https://www.cuemath.com/measurement/area-of-rhombus/
    https://www.wikihow.com/Calculate-the-Area-of-a-Rhombus

    not sure how this would qork with perimeter
        i guess i could check for certain missing values to determine area of perimeter, but for a few shapes the inputed values would be the same
'''