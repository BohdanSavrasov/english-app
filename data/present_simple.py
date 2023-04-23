import csv
import spacy
from spacy import displacy
from common import *
from root_verb_options import root_verb_options
from aux_verb_options import aux_verb_options


def present_simple():
    global MATCHING
    global TOKEN
    global PARALLEL
    global SEQ

    with open("data/present_simple.txt", mode="r") as f:
        docs = [nlp(line.strip()) for line in f]

    tasks = []

    for doc in docs:
        tokens = []
        shouldSkipNextToken = False
        for token in doc:

            if shouldSkipNextToken:
                shouldSkipNextToken = False
                continue

            auxOptions = aux_verb_options(token)
            if auxOptions is not None:
                shouldSkipNextToken, auxOptions = auxOptions

                if shouldSkipNextToken:
                    tokenOptions = [
                        SEQ(
                            TOKEN(tkn, token.whitespace_),
                            TOKEN(neg, token.nbor().whitespace_)
                        )
                        for tkn, neg in auxOptions
                    ]

                    tokens.append(
                        PARALLEL(
                            SEQ(
                                TOKEN(token.text, token.whitespace_),
                                TOKEN(token.nbor().text, token.nbor().whitespace_)
                            ),
                            *tokenOptions,
                        )
                    )
                else:
                    tokens.append(
                        PARALLEL(
                            TOKEN(token.text, token.whitespace_),
                            *[TOKEN(o, token.whitespace_) for o in auxOptions]
                        )
                    )
                continue

            rootOptions = root_verb_options(token)
            if rootOptions is not None:
                tokens.append(
                    PARALLEL(
                        TOKEN(token.text, token.whitespace_),
                        *[TOKEN(o, token.whitespace_) for o in rootOptions]
                    )
                )
                continue

            tokens.append(TOKEN(token.text, token.whitespace_))

        tasks.append(MATCHING(tokens))

    return tasks


if __name__ == "__main__":
    allTasksJson = json.dumps(present_simple())

    with open("./out.json", mode="w") as f:
        f.write(allTasksJson)
