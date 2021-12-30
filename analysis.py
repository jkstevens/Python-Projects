# ks678
from read_files import read_file, read_files
from ignored_words import IGNORED_WORDS


def remove_header(description: str):
    newlist: list = (description.split("\n\n", 1))
    return newlist[1]


def normalize_word(word: str):
    word1: str = ""
    for char in word:
        if char.isalpha():
            word1 += char.lower()
    return word1


def article_to_words(article: str):
    new_article = remove_header(article)
    list_of_words: list = (new_article.split(" "))
    count = 0
    for word in list_of_words:
        list_of_words[count] = normalize_word(word)
        count += 1
    list_of_words = list(filter(lambda a: a not in IGNORED_WORDS, list_of_words))
    return list_of_words


def count_words(word_list: list):
    count_of_words: dict = dict()
    for word in word_list:
        if word in count_of_words:
            count_of_words[word] += 1
        else:
            count_of_words[word] = 1
    return count_of_words


def merge_with_plus(d1: dict, d2: dict):
    for word in d2:
        if word in d1:
            d1[word] += d2[word]
        else:
            d1[word] = 1
    return d1


def sort_by_value(word_dict: dict):
    lst_wrds: list = []
    lst_cnts: list = []
    for word in word_dict:
        lst_wrds.append(word)
        lst_cnts.append(word_dict[word])
    lst_wrds.sort(key=lambda word: word_dict[word], reverse=True)
    lst_cnts.sort(key=None, reverse=True)
    lst_of_word_and_counts = list(zip(lst_cnts, lst_wrds))
    return lst_of_word_and_counts


def correlated_words(d: dict, word_list: list):
    for mainword in word_list:
        temp_word_list: list = word_list
        temp_word_list = list(filter(lambda a: a != mainword, temp_word_list))
        temp_key_dict: dict = count_words(temp_word_list)
        if mainword not in d:
            d[mainword] = temp_key_dict
        else:
            d[mainword] = merge_with_plus(d[mainword], temp_key_dict)
    return d


def main():
    descr_string_list: list = (read_files(input("Enter path of directory to evaluate:")))
    list_of_dicts_for_merge_plus: list[dict] = []
    base_dict_for_merge_plus: dict = {}
    for article in descr_string_list:
        list_of_words: list = article_to_words(article)
        dict_of_words_and_counts: dict = count_words(list_of_words)
        list_of_dicts_for_merge_plus.append(dict_of_words_and_counts)
    for each_dict in list_of_dicts_for_merge_plus:
        merge_with_plus(base_dict_for_merge_plus, each_dict)
    list_of_words_and_counts: list[tuple] = (sort_by_value(base_dict_for_merge_plus))
    print("Top 10 words:")
    for x in range(10):
        print(f"{list_of_words_and_counts[x][1]} ({list_of_words_and_counts[x][0]} times)")
    while True:
        input_string: str = input("")
        input_string_list: list[str] = []
        input_string_list.append(input_string)
        if input_string == "quit":
            print("Good bye!")
            break
        count_for_word: int = 0
        list_of_lists_of_strings_for_correlation: list[list[str]] = []
        for article_as_list_of_strings in descr_string_list:
            list_of_words_for_correlation: list[str] = article_to_words(article_as_list_of_strings)
            for word in list_of_words_for_correlation:
                if word == input_string:
                    count_for_word += 1
            if input_string in list_of_words_for_correlation:
                list_of_lists_of_strings_for_correlation.append(list_of_words_for_correlation)
        correlated_words_dict: dict = {}
        for string_list in list_of_lists_of_strings_for_correlation:
            correlated_words_dict = (correlated_words(correlated_words_dict, string_list))
        list_of_words_by_correlation: list[tuple] = (sort_by_value(correlated_words_dict[input_string]))
        print(f"The word {input_string} was found {count_for_word} times.\nTop 10 correlations:")
        for x in range(10):
            print(f"{input_string} {list_of_words_by_correlation[x][1]} ({list_of_words_by_correlation[x][0]} times)")


main()
