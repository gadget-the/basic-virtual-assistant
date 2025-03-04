def search_extract(input_string = "", classification = {"intent": None, "secondary-intent": None, "timing": None}):
    search_engines = ["google", "bing", "yandex", "yahoo", "baidu"]
    search_engine = None
    # finds the specified engine, if a supported one is specified
    [search_engine := e for e in search_engines if e in input_string.lower()]
    classification["engine"] = search_engine
    term = str(input_string) # failsafe/fallback; if the term isn't able to be set by the following code, it will already be set to the original full input

    if search_engine: # if a supported search engine was specified, attempt to remove the engine-specific delimiters
        search_engine_delimiters = [
            str(search_engine) + " search for ",
            str(search_engine) + " search ",
            "search " + str(search_engine) + " for ",
            "search " + str(search_engine) + " ",
            "search on " + str(search_engine) + " for ",
            "search on " + str(search_engine) + " ",
            "search for ",
            "search ",
            " on " + str(search_engine),
            str(search_engine) + " "
        ]

        [term := term.lower().replace(d, "") for d in search_engine_delimiters]
        # for delimiter in search_engine_delimiters:
        #     if delimiter in input_string.lower():
        #         # term = input_string.lower().replace(d, "").replace("search for ", "").replace("search ", "")
        #         term = input_string[input_string.lower().index(delimiter) + len(delimiter):]
        #         break
        
        # if not term or term == "search ":
        #     term = str(input_string)
        #     [term := term.lower().replace(d, "") for d in search_engine_delimiters]

    else: # if no specified search engine was found, attempt to remove the simpler delimiters
        classification["engine"] = None
        simple_search_delimiters = ["search for ", "search "]
        for delimiter in simple_search_delimiters:
            if delimiter in input_string.lower():
                term = input_string.lower().replace(delimiter, "")
                break

    classification["term"] = term