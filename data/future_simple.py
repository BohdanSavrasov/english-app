import csv
import spacy
from spacy import displacy
import lxml.etree
import lxml.builder
from common import *
from root_verb_options import root_verb_options
from aux_verb_options import aux_verb_options


def future_simple():
    global MATCHING
    global TOKEN
    global PARALLEL
    global SEQ
    global ANSWERS
    global SENTENCE

    with open("data/future_simple.txt", mode="r") as f:
        docs = [nlp(line.strip()) for line in f]

    tasks = []

    for doc in docs:
        xmlTokens = []
        shouldSkipNextToken = False
        for token in doc:

            if shouldSkipNextToken:
                shouldSkipNextToken = False
                continue

            ws = {'ws': 'false'} if token.whitespace_ == "" else {}

            auxOptions = aux_verb_options(token)
            if auxOptions is not None:
                shouldSkipNextToken, auxOptions = auxOptions

                if shouldSkipNextToken:
                    nborws = {'ws': 'false'} if token.nbor(
                    ).whitespace_ == "" else {}

                    tokenOptions = [
                        SEQ(TOKEN(tkn, **ws), TOKEN(neg, **nborws)) for tkn, neg in auxOptions]

                    xmlTokens.append(
                        PARALLEL(
                            SEQ(
                                TOKEN(token.text, **ws),
                                TOKEN(token.nbor().text, **nborws)
                            ),
                            *tokenOptions,
                        )
                    )
                else:
                    xmlTokens.append(
                        PARALLEL(
                            TOKEN(token.text, **ws),
                            *[TOKEN(o, **ws) for o in auxOptions]
                        )
                    )
                continue

            rootOptions = root_verb_options(token)
            if rootOptions is not None:
                xmlTokens.append(
                    PARALLEL(
                        TOKEN(token.text, **ws),
                        *[TOKEN(o, **ws) for o in rootOptions]
                    )
                )
                continue

            xmlTokens.append(TOKEN(token.text, **ws))

        tasks.append(MATCHING(SENTENCE(*xmlTokens), taskId=str(nextTaskId())))

    return tasks


if __name__ == "__main__":
    global TASKS
    allTasks = TASKS(*future_simple())
    xmlBytes = lxml.etree.tostring(allTasks, pretty_print=True)

    with open("./out.xml", mode="wb") as f:
        f.write(xmlBytes)
