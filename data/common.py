import json
import spacy
from spacy import displacy
from enum import Enum


all_sources = [
    "data/present_simple.txt",
    "data/present_continuous.txt",
    "data/present_perfect.txt",
    "data/present_perfect_cont.txt",
    "data/past_simple.txt",
    "data/past_continuous.txt",
    "data/past_perfect.txt",
    "data/past_perfect_continuous.txt",
    "data/future_simple.txt",
    "data/future_perfect.txt",
    "data/future_continuous.txt",
    "data/future_perfect_continuous.txt",
]


class VerbForm(Enum):
    BASE = 0
    THIRDP = 1
    PRESENT_PART = 2
    PAST = 3
    PAST_PART = 4


class VerbsObj():

    def __init__(
        self,
        base: str,
        thirdp: str,
        present_part: str,
        past: str,
        past_part: str,
    ):
        self.base = base
        self.thirdp = thirdp
        self.present_part = present_part
        self.past = past
        self.past_part = past_part

    def key(self):
        return self.base, self.thirdp, self.present_part, self.past

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, o):
        if o is not VerbsObj:
            return False

        return self.key() == o.key()

    def __iter__(self):
        yield VerbForm.BASE, self.base
        yield VerbForm.THIRDP, self.thirdp
        yield VerbForm.PRESENT_PART, self.present_part
        yield VerbForm.PAST, self.past
        yield VerbForm.PAST_PART, self.past_part

    def __str__(self):
        texts = ','.join(text for form, text in self)
        return "VerbsObj({texts})".format(texts=texts)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        if item == self.base:
            return VerbForm.BASE
        elif item == self.thirdp:
            return VerbForm.THIRDP
        elif item == self.present_part:
            return VerbForm.PRESENT_PART
        elif item == self.past:
            return VerbForm.PAST
        elif item == self.past_part:
            return VerbForm.PAST_PART
        elif item == VerbForm.BASE:
            return self.base
        elif item == VerbForm.THIRDP:
            return self.thirdp
        elif item == VerbForm.PRESENT_PART:
            return self.present_part
        elif item == VerbForm.PAST:
            return self.past
        elif item == VerbForm.PAST_PART:
            return self.past_part

        raise KeyError(item)


def load_verbs_list():
    verbs = {}
    with open("data/verbs.csv", mode="r") as f:
        for line in f:
            verbForms = line.strip().split(',')

            assert len(verbForms) == 5

            verbObj = VerbsObj(
                verbForms[0], verbForms[1], verbForms[4], verbForms[2], verbForms[3]
            )

            for form, text in verbObj:
                if text not in verbs:
                    verbs[text] = {verbObj}
                else:
                    verbs[text].add(verbObj)

    return verbs


def findVerb(token):
    global verbs

    if token.pos_ not in ['AUX', 'VERB']:
        raise Exception("Token must be a verb or aux")

    norm = token.norm_

    if token.lower_ == "did" and token.tag_ == "VBD":
        norm = "did"
    
    if token.lower_ == "had" and token.tag_ == "VBD":
        norm = "had"

    form = VerbForm.BASE
    if token.tag_ == "VBD":
        form = VerbForm.PAST
    if token.tag_ == "VBG":
        form = VerbForm.PRESENT_PART
    if token.tag_ == "VBN":
        form = VerbForm.PAST_PART
    if token.tag_ == "VBZ":
        form = VerbForm.THIRDP

    if token.lemma_ == "be":
        return form, None

    if norm not in verbs:
        raise Exception("Verb '{verb}' is not in list. Sentence: '{sent}'".format(
            verb=norm, sent=token.sent.text))

    verbObjSet = verbs[norm]

    try:
        obj = next(obj for obj in verbObjSet if obj[form] == norm)
    except:
        raise Exception(token, token.sent, form, norm, verbObjSet)

    if obj is None:
        print(token, form, token.sent, token.tag_,
              norm, token.orth_, token.text)

    return form, obj


def show(sent):
    doc = nlp(sent)
    for token in doc:
        if token.tag_.startswith("VB"):
            vbform, _ = findVerb(token)
            print(token.text, token.tag_, vbform)
        else:
            print(token.text, token.tag_)
        
    displacy.serve(doc)


taskId = 0


def nextTaskId():
    global taskId
    taskId += 1
    return taskId - 1


def MATCHING(sentence: list):
    return {
        "type": "matching",
        "sentence": sentence,
        "answers": None,
    }


def TOKEN(text: str, ws: str):
    wsParam = {} if ws == None or ws == " " else {"ws": ws}
    return {"type": "exact", "text": text, **wsParam}


def PARALLEL(*args):
    return {"type": "parallel", "children": args}


def SEQ(*args):
    return {"type": "seq", "children": args}


verbs = load_verbs_list()
nlp = spacy.load("en_core_web_trf", disable=["ner"])
