"""
Generate a list of 10,000 good words.
"""


def run() -> None:
    """Combine lots of words, remove lots of bad words"""
    # Typo: In word 'acer'
    with open("bad_words.txt") as bad:
        bad_words = [
            _.strip(" ,*.") for _ in bad.read().split("\n") if not _.startswith("#")
        ]

    with open("wordlist.10000.txt") as long_file:
        ten_k = [
            _.strip(" ,*.")
            for _ in long_file.read().split("\n")
            if not _.startswith("#")
        ]
        for word in ten_k:
            if len(word) == 1:
                # letters
                bad_words.append(word)
            if not word.isalpha():
                # letters
                bad_words.append(word)
            if word.upper() == word:
                # accronyms
                bad_words.append(word)
            if len([letter for letter in word if letter in "aeiou"]) == 0:
                bad_words.append(word)
    with open("three_k.txt") as three_file:
        three_k = [
            _.strip(" ,*.")
            for _ in three_file.read().split("\n")
            if not _.startswith("#")
        ]
        for word in three_k:
            if len(word) == 1:
                # letters
                bad_words.append(word)
            if not word.isalpha():
                # letters
                bad_words.append(word)
            if word.upper() == word:
                # accronyms
                bad_words.append(word)
            if len([letter for letter in word if letter in "aeiou"]) == 0:
                bad_words.append(word)

    with open("most-common-nouns-english.csv") as most_common_file:
        most_common = [
            _.strip(" ,*.")
            for _ in most_common_file.read().split("\n")
            if not _.startswith("#")
        ]
        for word in most_common:
            if len(word) == 1:
                # letters
                bad_words.append(word)
            if not word.isalpha():
                # letters
                bad_words.append(word)
            if word.upper() == word:
                # accronyms
                bad_words.append(word)
            if len([letter for letter in word if letter in "aeiou"]) == 0:
                bad_words.append(word)

    most_common_simpler = []
    for word in most_common:
        if "," in word:
            parts = word.split(",")
            first = parts[0]
            most_common_simpler.append(first)
        else:
            most_common_simpler.append(word)

    with open("people_names.txt") as people_file:
        people = [
            _.strip(" ,*.")
            for _ in people_file.read().split("\n")
            if not _.startswith("#")
        ]
        people = people[:1000]
    dedupe = {
        word.strip(", .").lower()
        for word in set(ten_k + three_k + most_common_simpler + people)
    }
    new_set = [word for word in dedupe if word not in bad_words]
    print(len(new_set))
    list.sort(new_set)
    print(new_set)
    with open("clean_ten_k.txt", "w", encoding="utf-8") as clean:
        clean.write("\n".join(list(new_set[:10000])))


if __name__ == "__main__":
    run()
