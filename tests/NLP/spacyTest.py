import spacy
# from spacy import displacy

NER = spacy.load("en_core_web_sm")

# raw_text="The Indian Space Research Organisation or is the national space agency of India, headquartered in Bengaluru. It operates under Department of Space which is directly overseen by the Prime Minister of India while Chairman of ISRO acts as executive of DOS as well."
# raw_text = "My name is John."
# raw_text = "My name is John"
raw_text = "My name is Jared Johnson."

text1 = NER(raw_text)
# print(text1)

for word in text1.ents:
    print(word.text, word.label_)

# spacy.explain("ORG")
# spacy.explain("GPE")

# displacy.render(text1,style="ent",jupyter=True)