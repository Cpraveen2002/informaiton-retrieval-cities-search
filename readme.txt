
  ___           _ _                ____ _ _   _             ____                      _     
 |_ _|_ __   __| (_) __ _ _ __    / ___(_) |_(_) ___  ___  / ___|  ___  __ _ _ __ ___| |__  
  | || '_ \ / _` | |/ _` | '_ \  | |   | | __| |/ _ \/ __| \___ \ / _ \/ _` | '__/ __| '_ \ 
  | || | | | (_| | | (_| | | | | | |___| | |_| |  __/\__ \  ___) |  __/ (_| | | | (__| | | |
 |___|_| |_|\__,_|_|\__,_|_| |_|  \____|_|\__|_|\___||___/ |____/ \___|\__,_|_|  \___|_| |_|
                                                                                           

Informaiton Retrieval for cities dataset

Motivation:
    Getting all cities information at one place, all things about hotels, travel, education, climate, geography...

Running:
    $> python indexer.py
    # You will be presented with some kind of user interface
    # ctrl-c to exit

Process:
    Web crawling:
        Collecting data from wikipedia
        Includes collecting seed urls from main page
        Extracting info about cities for every urls using selenium and beautifulsoup
    Creating Inverted Index:
        Creating Tokens for given dataset
        Includes removing special characters and stop words
        Generating Inverted Index
        Includes storing data about [term][doc_freq]->[p|o|s|t|i|n|g| |l|i|s|t]
    Processing Query:
        Applying normal tokenization process for query
        Getting documents which contains that tokens of input
        Applying Search feature, which gets documents based on no of tokens present in a document
    Collecting relevance feedback:
        Getting relevance feedback, using documentIds and text displayed related to that document
        Collecting sequence of documentIds, in an order
        Storing the collected sequence, in form of feedback_dict, which have a datastructure as
            { query: { docId1: 2, docId2: 3, docId3: 6, ... }, ... }
        Updating the global feedback dictionary
    Evaluating the system
        Calculating the recall and precission
        Based on the sequence of documentIds user interacted
        Plotting the recall vs precission curve
