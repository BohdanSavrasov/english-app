from common import *
import pickle
import os
import hashlib
from datetime import datetime
from dateutil import tz
import subprocess


def present_simple(sent):
    root = sent.root

    if root is None:
        return None

    if not root.tag_.startswith("VB"):
        return None

    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
        return None

    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) > 1:
        return None

    if len(auxes) == 1:
        if auxes[0].lemma_ != "do":
            return None
        
        aux_form, aux_obj = findVerb(auxes[0])

        if aux_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
            return None
        
        found_verbs.append((auxes[0], aux_form, aux_obj))

    return gen_sentence_tasks(found_verbs, Tense.PRESENT)


def present_continuous(sent):
    root = sent.root

    if root is None:
        return None

    if not root.tag_.startswith("VB"):
        return None

    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PRESENT_PART:
        return None

    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) > 1:
        return None

    if len(auxes) == 1:
        if auxes[0].lemma_ != "be":
            return None

        aux_form, aux_obj = findVerb(auxes[0])

        if aux_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
            return None
        
        found_verbs.append((auxes[0], aux_form, aux_obj))

    return gen_sentence_tasks(found_verbs, Tense.PRESENT_CONT)


def present_perfect(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form not in [VerbForm.PAST_PART]:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return None
    
    if auxes[0].lemma_ != 'have':
        return None

    aux_form, aux_obj = findVerb(auxes[0])
    found_verbs.append((auxes[0], aux_form, aux_obj))

    if aux_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
        return None

    return gen_sentence_tasks(found_verbs, Tense.PRESENT_PERF)


def present_perfect_continuous(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form not in [VerbForm.PRESENT_PART]:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return None
    
    if not (auxes[0].lemma_ == "have" and auxes[1].lemma_ == "be"):
        return None
    
    have_form, have_obj = findVerb(auxes[0])
    be_form, be_obj = findVerb(auxes[1])

    if have_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
        return None
    
    found_verbs.append((auxes[0], have_form, have_obj))
    
    if be_form != VerbForm.PAST_PART:
        return None
    
    found_verbs.append((auxes[1], be_form, be_obj))

    return gen_sentence_tasks(found_verbs, Tense.PRESENT_PERF_CONT)


def past_simple(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    auxes = [t for t in root.children if t.dep_ == "aux"]

    with_main_verb_be = len(auxes) == 0 and root.lemma_ == "be" and root_form == VerbForm.PAST
    is_positive = len(auxes) == 0 and root_form == VerbForm.PAST
    is_negative_or_question = False

    if len(auxes) == 1 and auxes[0].lemma_ == "do":
        aux_form, aux_obj = findVerb(auxes[0])
        found_verbs.append((auxes[0], aux_form, aux_obj))
        is_negative_or_question = aux_form == VerbForm.PAST and root_form == VerbForm.BASE
    
    is_past_simple = with_main_verb_be or (is_positive or is_negative_or_question)

    if not is_past_simple:
        return None

    return gen_sentence_tasks(found_verbs, Tense.PAST)


def past_continuous(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PRESENT_PART:
        return None

    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return None
    
    if auxes[0].lemma_ != "be":
        return None
    
    aux_form, aux_obj = findVerb(auxes[0])
    found_verbs.append((auxes[0], aux_form, aux_obj))

    if aux_form != VerbForm.PAST:
        return None

    return gen_sentence_tasks(found_verbs, Tense.PAST_CONT)


def past_perfect(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PAST_PART:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return None
    
    if auxes[0].lemma_ != "have":
        return None

    aux_form, aux_obj = findVerb(auxes[0])
    found_verbs.append((auxes[0], aux_form, aux_obj))

    if aux_form != VerbForm.PAST:
        return None
    
    return gen_sentence_tasks(found_verbs, Tense.PAST_PERF)


def past_perfect_continuous(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PRESENT_PART:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return None
    
    if not (auxes[0].lemma_ == "have" and auxes[1].lemma_ == "be"):
        return None
    
    have_form, have_obj = findVerb(auxes[0])
    found_verbs.append((auxes[0], have_form, have_obj))

    be_form, be_obj = findVerb(auxes[1])
    found_verbs.append((auxes[1], be_form, be_obj))

    if have_form != VerbForm.PAST or be_form != VerbForm.PAST_PART:
        return None
    
    return gen_sentence_tasks(found_verbs, Tense.PAST_PERF_CONT)


def future_simple(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.BASE:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return None
    
    if auxes[0].lemma_ != "will":
        return None

    return gen_sentence_tasks(found_verbs, Tense.FUTURE)


def future_continuous(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PRESENT_PART:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return None
    
    if auxes[0].norm_ != "will" or auxes[1].norm_ != "be":
        return None

    return gen_sentence_tasks(found_verbs, Tense.FUTURE_CONT)


def future_perfect(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PAST_PART:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return None
    
    if auxes[0].norm_ != "will" or auxes[1].norm_ != "have":
        return None
    
    return gen_sentence_tasks(found_verbs, Tense.FUTURE_PERF)


def future_perfect_continuous(sent):
    root = sent.root

    if root is None:
        return None
    
    if not root.tag_.startswith("VB"):
        return None
    
    root_form, root_obj = findVerb(root)
    found_verbs = [(root, root_form, root_obj)]

    if root_form != VerbForm.PRESENT_PART:
        return None
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 3:
        return None
    
    if auxes[0].norm_ != "will" or auxes[1].norm_ != "have" or auxes[2].norm_ != "been":
        return None
    
    return gen_sentence_tasks(found_verbs, Tense.FUTURE_PERF_CONT)


def gen_sentence_tasks(args: list[tuple], tense: Tense) -> list:
    
    def gen_answers(token: str, options: list[str]) -> list:
        for i in range(len(options)):
            if token.lower() == options[i].lower():
                return [str(i)]


    now = datetime.now(tz.tzutc()).isoformat()
    tasks = []
    for token, _, obj in args:
        sent = token.sent
        id = hashlib.sha256(bytes(str(sent) + token.text + "matching", 'utf-8')).hexdigest()[:24]
        options = sorted(set(verb for _, verb in obj))
        
        tokens = []
        for t in sent:
            if token == t:
                tokens.append(PARALLEL([TOKEN(o, t.whitespace_) for o in options]))
            else:
                tokens.append(TOKEN(t.text, t.whitespace_))
        
        answers = gen_answers(token.text, options)

        tasks.append(MATCHING(id, now, tokens, tense, answers))

    return tasks


def verify(docs) -> bool:
    wrong_cnt = 0

    def verify_sentence(sent, tense):
        def test(func, sent, sentence_tense: Tense, expected_tense: Tense) -> int:
            res = func(sent)

            if res is None and sentence_tense == expected_tense:
                print(sentence_tense.name, sent, expected_tense.name, "False")
                return 1

            if res is not None and sentence_tense != expected_tense:
                print(sentence_tense.name, sent, expected_tense.name, "True")
                return 1

            return 0
        
        nonlocal wrong_cnt

        wrong_cnt += test(present_simple, sent, tense, Tense.PRESENT)
        wrong_cnt += test(present_continuous, sent, tense, Tense.PRESENT_CONT)
        wrong_cnt += test(present_perfect, sent, tense, Tense.PRESENT_PERF)
        wrong_cnt += test(present_perfect_continuous, sent, tense, Tense.PRESENT_PERF_CONT)
        wrong_cnt += test(past_simple, sent, tense, Tense.PAST)
        wrong_cnt += test(past_continuous, sent, tense, Tense.PAST_CONT)
        wrong_cnt += test(past_perfect, sent, tense, Tense.PAST_PERF)
        wrong_cnt += test(past_perfect_continuous, sent, tense, Tense.PAST_PERF_CONT)
        wrong_cnt += test(future_simple, sent, tense, Tense.FUTURE)
        wrong_cnt += test(future_continuous, sent, tense, Tense.FUTURE_CONT)
        wrong_cnt += test(future_perfect, sent, tense, Tense.FUTURE_PERF)
        wrong_cnt += test(future_perfect_continuous, sent, tense, Tense.FUTURE_PERF_CONT)
    
    for doc, tense in docs:
        verify_sentence(next(doc.sents), tense)

    return wrong_cnt


def generate(docs):
    funcs = [
        present_simple,
        present_continuous,
        present_perfect,
        present_perfect_continuous,
        past_simple,
        past_continuous,
        past_perfect,
        past_perfect_continuous,
        future_simple,
        future_continuous,
        future_perfect,
        future_perfect_continuous,
    ]

    assert len(funcs) == 12

    tasks = []
    
    for doc, _ in docs:
        sent = next(doc.sents)
        cnt = 0
        
        for func in funcs:
            res = func(sent)
            if res is not None:
                tasks.extend(res)
                cnt += 1
        
        assert cnt == 1
    
    return tasks


if __name__ == "__main__":
    print("Loading docs")
    PICKLED_DOCS_PATH = "/tmp/docs.pickle"

    docs = []
    if os.path.exists(PICKLED_DOCS_PATH):
        with open(PICKLED_DOCS_PATH, mode="br") as f:
            docs = pickle.loads(f.read())
    else:
        for source, tense in all_sources:
            with (open(source, mode="r")) as f:
                docs.extend((doc, tense) for doc in nlp.pipe(line.strip() for line in f))
    
        with open(PICKLED_DOCS_PATH, mode="bw") as f:
            f.write(pickle.dumps(docs, pickle.HIGHEST_PROTOCOL))
    
    print("Loaded docs:", len(docs))
    print("Verifying")
    wrong_cnt = verify(docs)
    if wrong_cnt != 0:
        print("Wrong detections count:", wrong_cnt)
        exit()
    else:
        print("Verified OK")
    
    print("Generating")
    tasks = generate(docs)
    
    if len(tasks) > 0:
        with open("tasks.json", mode="w") as f:
            f.write(json.dumps(tasks))
        
        subprocess.check_output(["mongoimport", "--jsonArray", "--upsert", "-ctasks", "mongodb://localhost/engapp", "./tasks.json"])

        print("Generating OK")