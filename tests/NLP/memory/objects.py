import time
import datetime as dt
# from datetime import datetime, timedelta#, date
import pytz
from tzlocal.win32 import get_localzone_name
from nltk import word_tokenize, pos_tag#, Tree, ne_chunk

timeZone = pytz.timezone(get_localzone_name())

class EVENT():
    def __init__(self, ID = "", time_of_occurrence = None, event_duration = None, time_delta = None, involved_entities = [], quotations = []):
        self.current_time = dt.datetime.now()

        self.event_duration = event_duration
        self.involved_entities = involved_entities
        self.quotations = quotations
        self.time_of_occurrence = time_of_occurrence
        
        if time_of_occurrence:
            self.time_of_occurrence = time_of_occurrence
        elif time_delta:
            self.time_of_occurrence = self.current_time + time_delta
        else:
            self.time_of_occurrence = dt.datetime.min

    def parse_phrase(self, input_phrase = ""):
        relative_time_words = {
            "yesterday": {"days": -1},
            "last night": {"days": -1},
            "today": {"days": 0},
            "tonight": {"days": 0},
            "tomorrow": {"days": 1},
            "last week": {"weeks": -1},
            "next week": {"weeks": 1}
        }

        input_words = word_tokenize(input_phrase.lower())
        input_pos = pos_tag(input_words)

        # for word, pos in zip(input_words, input_pos):
        #     if word in relative_time_words:
        #         self.time_delta = dt.timedelta(days=relative_time_words[word])
        #         print(self.time_delta)

        for term in relative_time_words:
            if term in input_phrase:
                self.time_delta = dt.timedelta(**relative_time_words[term])
                self.time_of_occurrence = self.current_time + self.time_delta

                if self.time_of_occurrence.time() == self.current_time.time():
                    self.time_of_occurrence = dt.datetime.combine(self.time_of_occurrence, dt.time.min)
                # elif self.time_of_occurrence.date() == self.current_time.date():
                #     self.time_of_occurrence = dt.datetime.combine(self.time_of_occurrence, dt.time(relative_time_words[term]['hours'], 0))

    def import_from_dict(self, package = {}):
        pass

    def export(self):
        package = {
            "type": "EVENT",
            "time-of-occurrence": str(self.time_of_occurrence),
            "event-duration": str(self.event_duration),
            "involved": [],
            "quotations": []
        }

        return package

class PERSON():
    def __init__(self, foo = 0):
        pass

class PET():
    def __init__(self, foo = 0):
        pass

class LOCATION():
    def __init__(self, foo = 0):
        pass

class ORGANIZATION():
    def __init__(self, foo = 0):
        pass

class OBJECT():
    def __init__(self, foo = 0):
        pass


if __name__ == '__main__':
    event1 = EVENT()

    # event1.parse_phrase("I went to the store yesterday")
    event1.parse_phrase("I'm going to a party tonight")
    # event1.parse_phrase("I'm gonna go shoppin tomorrow")
    # event1.parse_phrase("The trip is next week")
    # event1.parse_phrase("No, that was last week")
    
    # event1.parse_phrase(input("> "))

    print(event1.export())