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
    NONTHIRDP = 1
    THIRDP = 2
    PRESENT_PART = 3
    PAST = 4
    PAST_PART = 5


class VerbsObj():

    def __init__(
        self,
        base: tuple,
        nonthirdp: tuple,
        thirdp: tuple,
        present_part: tuple,
        past: tuple,
        past_part: tuple,
    ):
        self.base = base
        self.nonthirdp = nonthirdp
        self.thirdp = thirdp
        self.present_part = present_part
        self.past = past
        self.past_part = past_part

    def key(self):
        return self.base, self.nonthirdp, self.thirdp, self.present_part, self.past, self.past_part

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, o):
        if not isinstance(o, VerbsObj):
            return False

        return self.key() == o.key()

    def __iter__(self):
        for word in self.base:
            yield VerbForm.BASE, word

        for word in self.nonthirdp:
            yield VerbForm.NONTHIRDP, word

        for word in self.thirdp:
            yield VerbForm.THIRDP, word

        for word in self.present_part:
            yield VerbForm.PRESENT_PART, word

        for word in self.past:
            yield VerbForm.PAST, word

        for word in self.past_part:
            yield VerbForm.PAST_PART, word

    def __str__(self):
        texts = ', '.join(f"{form.name}={word}" for form, word in self)
        return "VerbsObj({texts})".format(texts=texts)

    def __repr__(self):
        return self.__str__()
    
    def hasVerbInForm(self, verb: str, form: VerbForm) -> bool:
        if form == VerbForm.BASE:
            return verb in self.base
        elif form == VerbForm.NONTHIRDP:
            return verb in self.nonthirdp
        elif form == VerbForm.THIRDP:
            return verb in self.thirdp
        elif form == VerbForm.PRESENT_PART:
            return verb in self.present_part
        elif form == VerbForm.PAST:
            return verb in self.past
        elif form == VerbForm.PAST_PART:
            return verb in self.past_part
        
        raise KeyError("No such key supported")


def load_verbs_list():
    verbs = {}
    with open("data/verbs.csv", mode="r") as f:
        for line in f:
            verbForms = [tuple(w.split(";")) for w in line.strip().split(',')]

            assert len(verbForms) == 6

            verbObj = VerbsObj(
                verbForms[0], verbForms[1], verbForms[2], verbForms[3], verbForms[4], verbForms[5]
            )

            for _, text in verbObj:
                if text not in verbs:
                    verbs[text] = {verbObj}
                else:
                    verbs[text].add(verbObj)

    return verbs


def findVerb(token: spacy.tokens.token.Token):
    global verbs

    if token.pos_ not in ['AUX', 'VERB']:
        raise Exception("Token must be a verb or aux")

    norm: str = token.norm_

    if token.lower_ == "did" and token.lemma_ == "do":
        norm = "did"
    
    if token.lower_ == "had" and token.lemma_ == "have":
        norm = "had"
    
    if token.lower_ == "'s" and token.lemma_ == "be":
        norm = "is"

    form = VerbForm.BASE
    if token.tag_ == "VBD":
        form = VerbForm.PAST
    if token.tag_ == "VBG":
        form = VerbForm.PRESENT_PART
    if token.tag_ == "VBN":
        form = VerbForm.PAST_PART
    if token.tag_ == "VBP":
        form = VerbForm.NONTHIRDP
    if token.tag_ == "VBZ":
        form = VerbForm.THIRDP

    if norm not in verbs:
        raise Exception(f"Verb '{norm}' is not in list. Sentence: '{token.sent.text}'")

    verbObjSet = verbs[norm]

    try:
        obj = next(obj for obj in verbObjSet if obj.hasVerbInForm(norm, form))
    except:
        raise Exception(token, token.sent, form, norm, verbObjSet)

    if obj is None:
        print(token, form, token.sent, token.tag_,
              norm, token.orth_, token.text)

    return form, obj


def show(text):
    doc = nlp(text)
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
