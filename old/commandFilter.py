from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
# import nltk, re
# from nltk import word_tokenize

weather_command_inputs = [
    "what's the weather like in Miami, Florida",
    "what's the temperature in Atlanta, Georgia",
    "weather in Florence",
    "what's the weather like",
    "how's the temperature in San Diego",
    "what is the weather like in Moscow",
    "what temperature is it in Dubai",
    "what is the temperature in Dubai",
    "weather in Santa Barbara",
    "what is the weather for the next week",
    "what's the weather like for the next week",
    "weather in Timbuktu, Mali",
    "weather for the next week in Valleta, Malta",
    "what's the weather like in Puerto Vallarta",
    "weather in Chihuahua, Mexico",
    "temperature in Darwin, Australia",
    "what is the weather like in Fukuoka, Japan",
    "weather in Johannesburg",
    "is it sunny in Hangzhou",
    "weather Ekuhuleni, South Africa",
    "is the weather nice in Lima, Peru?",
    "weather in Montevideo",
    "temperature in Aachen, Germany",
    "weather for the next week in Reich, Germany",
    "Westheim weather",
    "what's the weather going to be like tomorrow in Earlham Iowa",
    "weather for next week in Bakersfield",
    "weather in Whiteville, NC",
    "Brown City, Michigan weather",
    "what is the weather for Wednesday in Mount Pleasant, ",
    "weather for San Ramon, California",
    "what is the weather like in Santa Angelo",
    "weather in Chimalpa",
    "what is the weather like in Beichan, China",
    "Mercy-le-Bas weather",
    "weather in Stainborough",
    "what's the weather in Jinglou, China",
    "weather for Radizel, Slovenia",
    "temp in Grone, Italy",
    "is it sunny in Chinchinim",
    "what is the temp for the next ten days in Longkamp, Germany",
    "weather for Lincoln, North Dakota",
    "weather for the next ten days in Merefa",
    "weather for the next ten days",
    "what will the temperature be on Wednesday",
    "Bohonye, Hungary weather",
    "what's the weather like in Veltheim, Switzerland",
    "what is the weather like in Cape Town",
    "weather Hiroshima, Japan",
    "Shanghai weather",
    "How's the temperature in Cairo",
    "temperature in Dubai",
    "weather next 10 days in Montreal",
    "how's the weather going to be next week",
    "weather in Beijing",
    "temp in Withington",
    "weather in Saint Petersburg for tomorrow",
    "what's the weather like in Campos, Spain",
    "is it snowing in Dallas",
    "weather in Glenn Heights, TX"#,
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # "",
    # ""
]

smarthouse_command_inputs = [
    "turn on the lights in the living room",
    "set the temperature to 70 degrees",
    "open the garage door",
    "turn off the air conditioner",
    "turn on the fireplace",
    "turn off the heater",
    "lower the temperature in the kitchen",
    "preheat the oven to 350 degrees",
    "close the garage",
    "turn on the lights in the garage",
    "turn off the lights in the yard",
    "close the garage door",
    "dim the lights to 50%",
    "turn kitchen lights out",
    "turn the lights in the kitchen off",
    "set the living room light to blue.",
    "turn the yard lights off",
    "turn the garage lights out",
    "set the bedroom lights to red.",
    "turn the lights down low",
    "turn the lights off",
    "turn all of the lights off",
    "are the lights on in the kitchen?",
    "what is the temperature in the living room?",
    "turn on kitchen lights.",
    "brighten living room lights.",
    "dim family room lights.",
    "set bedroom lights to 70%.",
    "turn basement lights blue.",
    "turn off all lights.",
    "make it warmer.",
    "decrease temperature by 3 degrees.",
    "set temperature to 70 degrees.",
    "what's on back porch camera.",
    "show front door camera on basement TV.",
    "turn on the vacuum.",
    "start the coffee maker.",
    "lower the temp in the living room by 10 degrees",
    "open the security feed for the back yard",
    "show me the front yard",
    "raise the temperature by 4 degrees",
    "are the yard lights on?",
    "are the lights off in the kitchen?",
    "turn the lights off in the back yard",
    "are the lights in the bedroom on?",
    "what is the temperature set to in the living room",
    "lock the back door",
    "lock all the doors",
    "turn on the fireplace",
    "lock all of the doors",
    "lock back door",
    "lock front door",
    "unlock the back door",
    "unlock front door",
    "is the front door locked?",
    "are the doors locked",
    "is the back door locked",
    "preheat the oven to 450",
    "turn off the stove",
    "start the coffee maker at 6 am tomorrow",
    "turn on the garbage disposal",
    "turn on the garburator",
    "turn on the tv",
    "turn down the tv",
    "turn up the tv",
    "turn the tv up",
    "mute the tv",
    "tv mute",
    "all lights off",
    "lights off",
    "turn the lights off",
    "is the tv on?",
    "what is the tv volume at?",
    "increase the tv volume by 25%",
    "lower the tv volume by 5 percent",
    "turn off the lights in the office",
    "are the lights in the office on?",
    "make it colder in the office",
    "lower the temp in the office by 5 degrees",
    "turn off the hall light",
    "turn on the lights in the hallway",
    "is the hallway light on",
    "turn on the lights in the main hallway",
    "brighten the lights in the living room",
    "turn off the porch lights",
    "turn the kitchen lights down to 15%",
    "lower the kitched lights by fifteen percent",
    "turn on the projector in the living room",
    "change the input device on the tv to xbox",
    "connect the vcr to the tv",
    "pause the tv",
    "tv full volume",
    "change tv input to HDMI1",
    "change the input on the tv to VGA",
    "lower the tv brightness",
    "turn on captions",
    "turn on the lights in the dining room",
    "change the lights in the bedroom to purple",
    "turn the stereo down",
    "turn the stereo up",
    "set the color of the lights in the master bedroom to blue",
    "set the color of the lights in the living room to magenta",
    "set the temp of the oven to 450",
    "what is the color of the lights in the living room"
]

math_command_inputs =  [
    "what's the square root of 49",
    "divide 52 by 8",
    "what is 9 to the 4th power",
    "2 + 2",
    "what is 9 times 72",
    "what is the derivative of x squared",
    "what is 2 + 2",
    "subtract 3 from 5",
    "7 * 12",
    "what is the square root of 64",
    "twelve times two",
    "how many times does 8 go into 64 evenly",
    "how many times does eight go into sixty-four evenly",
    "what is 8 to the 9th",
    "what is eight to the nineth",
    "what is 2 + 2",
    "what is two plus two",
    "fifty-two minus eight",
    "subtract 75 from 150",
    "what is fifty-two divided by eight",
    "what is 48 squared",
    "5 squared",
    "five squared",
    "47 + 89",
    "fifty-two plus eighty-seven",
    "5 + 7",
    "what is 90 + 15",
    "4 + 12",
    "what is 8 + 4?",
    "1 + 2 + 47 + 10",
    "what is 2020 - 1962",
    "what is two-thousand twenty minus one-thousand sixty-two",
    "what is four plus eight",
    "2020 - 1962",
    "what is the remainder of sixty-two divided by thirteen",
    "remainder of 62 divided by 13",
    "ninety plus 15",
    "19,000 + 32",
    "nineteen thousand plus thirty-two",
    "8 to the nineth power",
    "what is eight to the nineth power",
    "19 divided by 2",
    "what is half of thirty-two",
    "what is 18 + 90",
    "46 + 8",
    "what is 6 + 8",
    "19320 + 68",
    "what is the sum of 42, 68, 90, and 14",
    "sum of the numbers, 20, 40, 40, 50, and 150",
    "what is 15 less than 100",
    "what is 90 divided by 18",
    "what is the product of fourteen times seven",
    "how many times does 14 go into 49",
    "what is the square root of 81?",
    "what is the area of a triangle with a base of 12 and a height of 20",
    "what is the area of a parallelogram with a height of 14 and a base of 15",
    "what is the area of a trapezoid where the length of base one is 14, the length of base two is 20, and the height is 25?",
    "what is the area of a circle with a radius of 14",
    "area of a cirlce where the radius is 25",
    "what is 18 cubed",
    "eighteen to the third power",
    "18 to the 3rd",
    "what is eighteen to the third",
    "what is 18 times 12 times 13",
    "eighteen times thirteen time twelve",
    "81 * 17 * 100",
    "what is the area of a sphere where the radius is 18",
    "volume of a sphere with a radius of fifteen",
    "what is the perimeter of a rectangle that is eighteen feet long and twelve feet wide?",
    "perimeter of a circle with a radius of seventeen",
    "what is the circumference of a circle with a diameter of 8",
    "circumference of a circle that is 18 feet across",
    "eight plus fourty minus twelve times two",
    "what is the volume of a cylinder with a radius of 12 and a height of 19",
    "volume of a cylinder where the radius is five and the height is eight",
    "what is half of eighteen",
    "what is double twelve",
    "what is double the sum of five and nine",
    "double the sum of 5 and 9",
    "two times zero",
    "4 + 2 / 3",
    "14 * 3 - 15",
    "fourteen times five minus two",
    "(19 + 2)/3",
    "what is seventeen minus two times three",
    "(17 - 2) * 3",
    "4 + 98",
    "4 * 19",
    "18 / 22",
    "how many times does 8 go into 64",
    "does 8 go into 64 evenly?",
    "how many times does sixteen go into one hundred twenty-eight?",
    "seventeen times three",
    "2 * (5 + 9)",
    "28 + 18",
    "64 - 16",
    "thirteen plus 3 times 4",
    "twenty-eight times two",
    "4 times 8",
    "3 + 7"
]

search_command_inputs =  [
    "what is the capital of Russia",
    "How tall is Mount Everest",
    "where is the nearest Walmart",
    "when is Easter",
    "who is the President",
    "who is Vladmir Putin",
    "how did john F kennedy die",
    "what is a marsupial",
    "what is the capital of Alaska",
    "what is a vegan",
    "what is vegan",
    "what is a dalek?",
    "what's a smarthouse",
    "google search how high can you fall and survive",
    "google how high can you fall and survive?",
    "search candle types",
    "how many days are in september",
    "how many days until the 21st night of september?",
    "what are the lyrics of all i want for christmas",
    "what are the lyrics of despicable by grandson",
    "lyrics to rockefeller street",
    "what are the lyrics to happy birthday",
    "where are pandas' habitat",
    "where is minecon being held",
    "who was Abraham Lincoln",
    "who was George Bush",
    "what is a bruh moment?",
    "is pluto a planet",
    "why isn't pluto classified as a planet anymore",
    "search how to adjust the temperature on a conair ac unit",
    "what is obama's last name",
    "how do stars form?",
    "what is at the center of the galaxy",
    "what is the process through diamonds form",
    "what are tectonic plates",
    "how do you bake a cake",
    "where can I go to buy headphones",
    "what year did the civil war end",
    "is flour flammable?",
    "where can I buy a jetski",
    "what is a squatter",
    "what continent is Dubai in",
    "what country is Sussex in",
    "how many terms did Nixion serve?",
    "how many stars are there",
    "how many people are there in the us?",
    "how many planets are there",
    "what is a macbook",
    "google what is a pangolin",
    "google search what is a pangolin",
    "search on google the first president of Russia",
    "search on google the total number of satelites in orbit",
    "search for pizza places near me",
    "what is Mdonalds",
    "where is Paris",
    "restaurants near me",
    "what are the lyrics to Star-Spangled Banner",
    "where is Timbuktu?",
    "what is the capital of France",
    "what is the capital of Vietnam?",
    "is Paris the capital of France",
    "is Paris in France?",
    "what is the Bermuda Triangle",
    "who is Barack Obama",
    "who is Barack Hussein Obama",
    "who was the first president",
    "who was Fred Hampton",
    "what country is Timbuktu in",
    "what is linear regression",
    "what are some stomach ache remedies",
    "how to change a tire",
    "how do I change a tire",
    "how does one changed a tire",
    "stomache ache rememdies",
    "what helps with a migraine",
    "what are some facts about the Bermuda Triangle?",
    "what are some places to get good food nearby",
    "where is Hong Kong",
    "what is youtube",
    "what is google",
    "search on google restaurants near me",
    "search for nearby restaurants",
    "gas stations near me",
    "who is Morgan Freeman",
    "what is the most recent film Laurence Fishburn has acted in?",
    "what is scikit learn",
    "what is the difference between linen and silk",
    "who is Bruce Banner",
    "how old is Bruce Wayne",
    "what is dissociation",
    "what are the symptoms of Bronchitis",
    "what is psychosis",
    "places in the world with the best weather",
    "places with the best weather year round",
    "is Pluto a planet",
    "what is a dwarf planet",
    "what is a quasar",
    "places that sell notebooks",
    "places nearby that sell binders",
    "places that sell tennis balls near me",
    "what places have the best weather",
    "what country has the highest income tax rates",
    "what are the countries with the highest taxes",
    "what places do you pay the most in taxes in",
    "highest point on earth",
    "lowest point on earth",
    "google countries with high tax rates",
    "what does PETA stand for",
    "what does NASA stand for?",
    "what does USSR stand for",
    "google world population",
    "what is the world population",
    "search on google US population",
    "search on bing Ukraine population",
    "search world population",
    "search on google number of satelites in orbit",
    "search on bing number of seats in parliament"
]

conversation_inputs =  [
    "hello",
    "how are you",
    "what is up",
    "i like cheese",
    "my favourite animal is the panda",
    "you're nice",
    "fire is bad",
    "i'm fine",
    "i'm good",
    "i'm doing fine",
    "i am great",
    "lovely weather we're having",
    "this is dumb",
    "where are you from",
    "no",
    "yes",
    "that's nice",
    "cool",
    "bad",
    "why",
    "do you like the McRib",
    "do you like Bill Gates",
    "who is your favourite president",
    "bruh",
    "i think Pluto is still a planet",
    "ugh",
    "um",
    "uh",
    "shoot",
    "dang it",
    "dang",
    "darn",
    "how was your day",
    "hi",
    "hello",
    "hey",
    "yo",
    "what's up",
    "howdy",
    "thank you",
    "you're welcome",
    "bye",
    "goodbye",
    "see you later",
    "what was the homework from last Friday?",
    "hiya",
    "heyo",
    "what are you doing?",
    "yeah",
    "yes",
    "no",
    "nah",
    "is this forever?",
    "'sup",
    "sup",
    "not much",
    "sorry",
    "I'm sorry",
    "just working on a little project",
    "what is your name",
    "about the same",
    "are you busy later?",
    "dude",
    "bro",
    "are daleks real?",
    "where are you from?",
    "how old are you?",
    "what is your favorite color",
    "what is you favorite movie",
    "whatcha doing",
    "whatcha up to?",
    "what about you",
    "Hello! How are you?",
    "Oh, Hi!",
    "I'm great! How are you?",
    "I'm fine.",
    "Goodbye!",
    "See you later!",
    "Have a great day!",
    "Bye!",
    "Oh, that's okay.",
    "It's okay.",
    "I forgive you.",
    "All is forgiven.",
    "No apology needed.",
    "Just working on a little project.",
    "What've you been up to?",
    "Can you meet me there?",
    "It's good. It's real Italian food, and you'll get to see how I am in a real Italian restaurant.",
    "I'm thinking about taking you out to dinner to an Italian place.",
    "Can you meet me there?",
    "Well, I'm thinking about it.",
    "Oh! Are you still planning on taking me out?",
    "Oh. What's going on?",
    "I'm feeling about the same.",
    "Yeah. That would've been awkward.",
    "Yep! I found it, at last!",
    "You find that thing you were looking for?",
    "how is it over there?",
    "how have you been holding up?",
    "Are you serious?",
    "what do you do for a living?",
    "hmm",
    "hm",
    "hmmm",
    "what process?"
]

open_app_inputs = [
    "open firefox",
    "open visual studio code",
    "please open command prompt",
    "open file explorer",
    "open minecraft",
    "open discord",
    "open spotify",
    "could you open task manager",
    "open omen command center",
    "open malwarebytes",
    "please open firefox",
    "would you kindly open mspaint",
    "can you open the calculator",
    "would you open discord for me?",
    "please open minecraft"
]

browser_inputs = [
    "open outlook",
    "open youtube.com",
    "open google.com",
    "open minecraft.net",
    "go to wikipedia",
    "open up google",
    "go to towardsdatascience.com"
]

time_inputs = [
    "what time is it?",
    "do you have the time",
    "the time",
    "you wouldn't happen to have the time?",
    "what's the time?",
    "what is the current time?",
    "do you have the time",
    "could you tell me what time it is?",
    "tell me the time",
    "tell me what time it is",
    "have you got the time?"
]

test_inputs = [
    "8 + 4",
    "turn on the heater in the living room",
    "what is the weather like in Redmond, Washington",
    "what are you up to",
    "open the garage",
    "ten squared",
    "what is the capital of Alaska",
    "two plus two",
    "what is 48 + 32",
    "where is timbuktu?",
    "how to change a tire",
    "please open the garage door",
    "weather in Palo Alto",
    "places with the best weather",
    "dim the lights in the living room",
    "open steam",
    "go to bing.com",
    "what time is it?",
    "is the light on in the garage",
    "weather forecast for the next week",
    "search for rash causes"
]

training_inputs = weather_command_inputs + smarthouse_command_inputs + math_command_inputs + conversation_inputs + search_command_inputs + open_app_inputs + browser_inputs + time_inputs
training_labels = ["weather"] * len(weather_command_inputs) + ["smarthouse"] * len(smarthouse_command_inputs) + ["math"] * len(math_command_inputs) + ["conversation"] * len(conversation_inputs) + ["search"] * len(search_command_inputs) + ["app"] * len(open_app_inputs) + ["browser"] * len(browser_inputs) + ["time"] * len(time_inputs)
#print(training_inputs)
#print(training_labels)

# print([" ".join(word_tokenize(re.sub(r'[^\w\s]', ' ', x))) for x in training_inputs][:15])
# print([" ".join(word_tokenize(x)) for x in training_inputs][:15])

testing_labels = ['math', 'smarthouse', 'weather', 'conversation', 'smarthouse', 'math', 'search', 'math', 'math', 'search', 'search', 'smarthouse', 'weather', 'search', 'smarthouse', 'app', 'browser', 'time', 'smarthouse', 'weather', 'search']

vectorizer = CountVectorizer()#converts the text into a numerical representation through the use of the "bag of words" technique

# vectorizer.fit(training_inputs)
training_vectors = vectorizer.fit_transform(training_inputs)
# print(vectorizer.vocabulary_)

# training_vectors = vectorizer.transform(training_inputs)
testing_vectors = vectorizer.transform(test_inputs)

def decTrClass(inP = ""):
    raw_x = [inP]
    vectors = vectorizer.transform(raw_x)

    classifier = tree.DecisionTreeClassifier() # https://www.codementor.io/@garethdwyer/introduction-to-machine-learning-with-python-and-repl-it-rln7ywkhc
    classifier.fit(training_vectors, training_labels)
    prediction = classifier.predict(vectors)

    tree.export_graphviz( # http://www.webgraphviz.com/
        classifier,
        out_file='old/tree.dot',
        feature_names=vectorizer.get_feature_names(),
    )

    return prediction

def knnClass(inP = ""):
    raw_x = [inP]
    vectors = vectorizer.transform(raw_x)

    classifier = KNeighborsClassifier() # https://stackabuse.com/overview-of-classification-methods-in-python-with-scikit-learn
    classifier.fit(training_vectors, training_labels)
    prediction = classifier.predict(vectors)
    return prediction

def lsvcClass(inP = ""):
    raw_x = [inP]
    vectors = vectorizer.transform(raw_x)

    classifier = LinearSVC()
    classifier.fit(training_vectors, training_labels)
    prediction = classifier.predict(vectors)
    return prediction

def forClass(inP = ""):
    raw_x = [inP]
    vectors = vectorizer.transform(raw_x)

    classifier = RandomForestClassifier(n_estimators=10)
    classifier.fit(training_vectors, training_labels)
    prediction = classifier.predict(vectors)
    return prediction

if __name__ == '__main__':
    # classifier = tree.DecisionTreeClassifier()
    classifier = KNeighborsClassifier()
    # classifier = LinearSVC()
    # classifier = RandomForestClassifier(n_estimators=15)
    classifier.fit(training_vectors, training_labels)
    predictions = classifier.predict(testing_vectors)
    # con = confusion_matrix(testing_labels, predictions)
    acc = accuracy_score(testing_labels, predictions)

    print("weather", len(weather_command_inputs))
    print("smarthouse", len(smarthouse_command_inputs))
    print("math", len(math_command_inputs))
    print("search", len(search_command_inputs))
    print("conversation", len(conversation_inputs))
    print("app", len(open_app_inputs))
    print("browser", len(browser_inputs))
    print("time", len(time_inputs))
    print("\ntrain", len(training_inputs))
    print("test", len(test_inputs))

    num = 20
    for pred, inp, lbl in zip(predictions[:num], test_inputs[:num], testing_labels[:num]):
        if pred != lbl:
            m = "X"
        else:
            m = "O"
        print(m, "-", inp, "-", pred, "<->", lbl)

    # print(predictions)
    
    # print(con)
    # print("Accuracy:", acc)
    print("{:.2%} Accuracy".format(acc))

    # print('"",\n'*86)

    x = ""
    while x != "stop":
        x = input("> ")
        print(decTrClass(x))
        # print(knnClass(x))
        # print(lsvcClass(x))
        # print(forClass(x))


'''
https://www.codementor.io/@garethdwyer/introduction-to-machine-learning-with-python-and-repl-it-rln7ywkhc

I need a better classification method(higher accuracy)
things seem to be returning as math when they shouldn't, and I'm not too sure why

decision trees don't work super well
i think i might use knn(knearestneighbors) or linear regression for classification
https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-classification

apparently linear regression shouldn't be used for classification

knn isn't working well all of a sudden
overfitting?

linearsvc?
linear support vector machine/classification

I also have a very small amount of training data
I apparently need at least 1000, but for "average" problems I should have 10,000 to 100,000
https://qr.ae/pGHAzf
https://machinelearningmastery.com/much-training-data-required-machine-learning/

semantic parsing

intent determination
entity extraction

multilabel/multi-output classification?
could be used for the importance filter
["age", "name", "relationship", "likes", "dislikes", "remember", "None"]
'''