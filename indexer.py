import os
import pickle
import re
import sys
import json
from matplotlib import pyplot as plt

# import sys
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(5000)
# print(sys.getrecursionlimit())
# sys.exit()

stop_list = {"a", "a's", "able", "about", "above", "according", "accordingly", "across", "actually", "after", "afterwards", "again", "against", "ain't", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", "aren't", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "b", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "c", "c'mon", "c's", "came", "can", "can't", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn't", "course", "currently", "d", "definitely", "described", "despite", "did", "didn't", "different", "do", "does", "doesn't", "doing", "don't", "done", "down", "downwards", "during", "e", "each", "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f", "far", "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "g", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "he's", "hello", "help", "hence", "her", "here", "here's", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "j", "just", "k", "keep", "keeps", "kept", "know", "knows", "known", "l", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "let's", "like", "liked", "likely", "little", "look", "looking", "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely", "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "s", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldn't", "since", "six", "so", "some", "somebody", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that's", "thats", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "there's", "thereafter", "thereby", "therefore", "therein", "theres", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think", "third", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", "usually", "uucp", "v", "value", "various", "very", "via", "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've", "welcome", "well", "went", "were", "weren't", "what", "what's", "whatever", "when", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "who's", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within", "without", "won't", "wonder", "would", "would", "wouldn't", "x", "y", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "z", "zero"}

####### tokenization #######

special_chars = [".", "'", '"', "(", ")", ",", "&", "@", "-", "“", "”", "—", "-", ":", ";", "‘", "’", "\xa0", "\n"]

def tokens_of_word(word):
    word = word.lower()
    for char in special_chars:
        word = word.replace(char, " ")
    return_words = []
    for split in word.split(" "):
        try:
            if split[-2:] == "’s" or split[-2:] == "'s":
                split = split[:-1]
        except:
            split = split
        if split == "" or split == " ":
            continue
        if split in stop_list:
            continue
        return_words.append(split)
    return return_words

def tokenizer(file_path, doc_id):
    tokens_set = set()
    file = open(file_path, "r", encoding = "utf8")
    tokens = []
    for line in file.readlines():
        words = line.split(" ")
        for word in words:
            for token in tokens_of_word(word):
                if token not in tokens_set:
                    tokens.append([token, doc_id])
                    tokens_set.add(token)
    return tokens

def handle_tokenizer(folder_path):
    return_tokens = []
    filenames_dict = {}
    for iter, element in enumerate(os.listdir(folder_path)):
        if os.path.isfile(os.path.join(folder_path, element)):
            # document_id = int(os.path.basename(element)[:-4])
            document_id = iter + 1
            if document_id not in filenames_dict:
                filenames_dict[document_id] = os.path.join(folder_path, element)
            return_tokens.extend(tokenizer(os.path.join(folder_path, element), document_id))
    return_tokens.sort(key = lambda x: (x[0], x[1]))
    return return_tokens, filenames_dict

############################
######## indexer ###########

class LLNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def indexer(tokens):
    return_dict = {}
    prev_node = None
    for token in tokens:
        if token[0] in return_dict:
            prev_node.next = LLNode(token[1])
            prev_node = prev_node.next
            return_dict[token[0]][0] += 1
        else:
            return_dict[token[0]] = [1, None]
            return_dict[token[0]][1] = LLNode(token[1])
            prev_node = return_dict[token[0]][1]
    return return_dict

#############################
######## process-query ######

def make_query(inverted_index, query_str, feedback_dict):
    strings = query_str.split(" ")
    total_words = []
    for string in strings:
        total_words.extend(tokens_of_word(string))
    doc_ids_dict = {}
    for word in total_words:
        if word in inverted_index:
            curr_node = inverted_index[word][1]
            while curr_node != None:
                if curr_node.val in doc_ids_dict:
                    doc_ids_dict[curr_node.val] += 1
                else:
                    doc_ids_dict[curr_node.val] = 1
                curr_node = curr_node.next
    doc_id_freq = []
    for key in doc_ids_dict:
        doc_id_freq.append([key, doc_ids_dict[key]])
    doc_id_freq.sort(key = lambda x: -x[1])

    ## considering relevance feedback
    previous_freq = []
    previous_set = set()
    if query_str in feedback_dict:
        for key in feedback_dict[query_str]:
            previous_freq.append([key, feedback_dict[query_str][key]])
            previous_set.add(key)
    previous_freq.sort(key = lambda x: -x[1])

    for arr in doc_id_freq:
        if arr[0] not in previous_set:
            previous_freq.append(arr)
    doc_id_freq = previous_freq

    # previous_freq.extend(doc_id_freq)
    # doc_id_freq = previous_freq

    # print("The top documents for given text '" + query_str + "' and words match for each document are: ")
    if len(doc_id_freq) > 10:
        # print(doc_id_freq[:20])
        return doc_id_freq[:10]
    # print(doc_id_freq)
    return doc_id_freq

def and_operation(inverted_index, word1, word2):
    return_arr = []
    if (word1 in inverted_index) and (word2 in inverted_index):
        first = inverted_index[word1][1]
        second = inverted_index[word2][1]
        while first != None and second != None:
            if first.val == second.val:
                return_arr.append(first.val)
                first = first.next
                second = second.next
            elif first.val < second.val:
                first = first.next
            else:
                second = second.next
    return return_arr

def handle_and(inverted_index, word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    merge_arr = and_operation(inverted_index, word1, word2)
    if len(merge_arr) == 0:
        print("Both words are not common in any document..")
        return
    print("Common document ids of " + word1 + ", " + word2 + " are: ")
    for elem in merge_arr:
        print(str(elem) + " ", end="")
    print("\n", end = "")

def or_operation(inverted_index, word1, word2):
    return_arr = []
    if (word1 in inverted_index) and (word2 in inverted_index):
        first = inverted_index[word1][1]
        second = inverted_index[word2][1]
        while first != None and second != None:
            if first.val == second.val:
                return_arr.append(first.val)
                first = first.next
                second = second.next
            elif first.val < second.val:
                return_arr.append(first.val)
                first = first.next
            else:
                return_arr.append(second.val)
                second = second.next
        while first != None:
            return_arr.append(first.val)
            first = first.next
        while second != None:
            return_arr.append(second.val)
            second = second.next
    return return_arr

def handle_or(inverted_index, word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    merge_arr = or_operation(inverted_index, word1, word2)
    if len(merge_arr) == 0:
        print("There are no documents, containing the given words..")
        return
    print("Documents ids, where either of " + word1 + ", " + word2 + " are present: ")
    for elem in merge_arr:
        print(str(elem) + " ", end = "")
    print("\n", end="")

def get_short_info(filepath, max_length):
    file = open(filepath, 'r', encoding='utf-8')
    line_string = ""
    for iter, line in enumerate(file.readlines()):
        if iter < 3:
            continue
        line_string += line.replace("\n", " ").replace("\t", " ")
        if len(line_string) > max_length:
            line_string = line_string[:max_length]
            break
    return line_string

def display_results(doc_ids, filepaths_dict):
    print("")
    for id in doc_ids:
        file_path = filepaths_dict[id]
        file_path = file_path[file_path.rfind("\\"):]
        file_path = re.sub(r'\[.+?\]', '', file_path)
        file_path = file_path[:28]
        short_info = get_short_info(filepaths_dict[id], 110)
        print(str(id).zfill(4), end=" ")
        print(file_path.ljust(28), end=" ")
        print(short_info)
    print("")

def print_recall_precision(doc_ids, results, recall, precision):
    print("-------------------------------")
    print("docid    Rel   Rec    Pre")
    for doc in doc_ids:
        print(" ", end="")
        print(str(doc).zfill(4), end="    ")
        if doc in results:
            print("R", end="     ")
            index = results.index(doc)
            print(recall[index], end="    ")
            print(precision[index])
        else:
            print("NR")
    print("-------------------------------")
    # recall_outer.extend(recall)
    # precision_outer.extend(precision)
    plt.plot(precision, recall)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.show()


def collect_feedback(doc_id_freq, filepaths_dict):
    result_set = set()
    # served_order = []
    feedback = {}
    doc_ids = []
    for elem in doc_id_freq:
        result_set.add(elem[0])
        doc_ids.append(elem[0])
    display_results(doc_ids, filepaths_dict)

    results_list = []
    while True:
        input_var = input("Enter Your Choice: ")
        if input_var == "":
            # print(" end ", end="\r")
            sys.stdout.write("\033[F")
            print("Thank For Your Feedback")
            break
        try:
            input_rank = int(input_var.strip())
            if input_rank not in result_set:
                print("Enter documentId from results")
                continue
            # print(rank)
            if input_rank not in results_list:
                results_list.append(input_rank)
            # else:
            #     print(" ", end="\r")
            # rank += 1
            # sys.stdout.write("\033[F")
            # sys.stdout.write("\033[F")
        except:
            print("Enter valid documentId")
    for iter, doc_id in enumerate(results_list):
        feedback[doc_id] = len(results_list)-iter
    
    precision = []
    for iter, item in enumerate(results_list):
        rank = doc_ids.index(item)
        precision.append((iter+1)/(rank+1))
    
    ## imagination
    total_rel = len(doc_ids)
    recall = []
    for iter, item in enumerate(results_list):
        recall.append((iter+1)/total_rel)

    if len(results_list) != 0:
        print_recall_precision(doc_ids, results_list, recall, precision)

    return feedback

def handle_add_feedback(total_dict, query, feedback):
    # total_dict = {}
    # with open('feedback.json', 'r') as json_file:
    #     total_dict = json.load(json_file)
    # print(total_dict)
    if query not in total_dict:
        total_dict[query] = feedback
    else:
        for doc_key in feedback:
            if doc_key in total_dict[query].keys():
                total_dict[query][doc_key] += feedback[doc_key]
            else:
                total_dict[query][doc_key] = feedback[doc_key]
    # with open('feedback.json', 'w') as json_file:
    #     json.dump(total_dict, json_file, indent=4)


###########################
####### driver code #######

# def load_inverted_index():
#     inverted_index = {}
#     try:
#         file = open('inverted-index.pkl', 'rb')
#         inverted_index = pickle.load(file)
#         file.close()
#     except:
#         tokens = handle_tokenizer("./data-collection/cities")
#         inverted_index = indexer(tokens)
#         file = open('inverted-index.pkl', 'wb')
#         pickle.dump(inverted_index, file)
#         file.close()
#     return inverted_index

tokens, filepaths_dict = handle_tokenizer("./data-collection/cities")
inverted_index = indexer(tokens)
feedback_dict = {}

# recall_outer = []
# precision_outer = []

print("----------------------------------------------------------------------------------------")
print("                         wikipedia - cities related search                              ")
print("----------------------------------------------------------------------------------------")

while True:
    #  inverted_index = load_inverted_index()
    query = input("Enter Your Query: ")
    if query == "":
        break
    result_doc_with_freq = make_query(inverted_index, query, feedback_dict)
    feedback = collect_feedback(result_doc_with_freq, filepaths_dict)
    total_dict = handle_add_feedback(feedback_dict, query, feedback)

    # handle_and(inverted_index, "Dustin", "emphatic")
    # handle_or(inverted_index, "Dustin", "emphatic")

print("----------------------------------------------------------------------------------------")
print("                                     Thank You                                          ")
print("----------------------------------------------------------------------------------------")


# plt.plot(recall_outer, precision_outer)
# plt.xlabel("Recall")
# plt.ylabel("Precision")
# plt.show()
############################