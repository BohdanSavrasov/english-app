from common import *


def is_present_simple(sent):
    root = sent.root

    if root is None:
        return False

    if not root.tag_.startswith("VB"):
        return False

    root_form, root_obj = findVerb(root)

    if root_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
        return False

    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) > 1:
        return False

    if len(auxes) == 1:
        if auxes[0].lemma_ != "do":
            return False
        
        aux_form, aux_obj = findVerb(auxes[0])

        if aux_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
            return False

    return True


def is_present_continuous(sent):
    root = sent.root

    if root is None:
        return False

    if not root.tag_.startswith("VB"):
        return False

    form, obj = findVerb(root)

    if form != VerbForm.PRESENT_PART:
        return False

    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) > 1:
        return False

    if len(auxes) == 1:
        if auxes[0].lemma_ != "be":
            return False

        aux_form, aux_obj = findVerb(auxes[0])

        if aux_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
            return False

    return True


def is_present_perfect(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form not in [VerbForm.PAST_PART]:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return False
    
    if auxes[0].lemma_ != 'have':
        return False

    aux_form, aux_obj = findVerb(auxes[0])

    if aux_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
        return False

    return True


def is_present_perfect_continuous(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form not in [VerbForm.PRESENT_PART]:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return False
    
    if not (auxes[0].lemma_ == "have" and auxes[1].lemma_ == "be"):
        return False
    
    have_form, have_obj = findVerb(auxes[0])
    be_form, be_obj = findVerb(auxes[1])

    if have_form not in [VerbForm.BASE, VerbForm.NONTHIRDP, VerbForm.THIRDP]:
        return False
    
    if be_form != VerbForm.PAST_PART:
        return False
    
    return True


def is_past_simple(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    auxes = [t for t in root.children if t.dep_ == "aux"]

    with_main_verb_be = len(auxes) == 0 and root.lemma_ == "be" and root_form == VerbForm.PAST
    is_positive = len(auxes) == 0 and root_form == VerbForm.PAST
    is_negative_or_question = False

    if len(auxes) == 1 and auxes[0].lemma_ == "do":
        aux_form, aux_obj = findVerb(auxes[0])
        is_negative_or_question = aux_form == VerbForm.PAST and root_form == VerbForm.BASE
    
    is_past_simple = with_main_verb_be or (is_positive or is_negative_or_question)

    if not is_past_simple:
        return False

    return True


def is_past_continuous(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.PRESENT_PART:
        return False

    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return False
    
    if auxes[0].lemma_ != "be":
        return False
    
    aux_form, aux_obj = findVerb(auxes[0])

    if aux_form != VerbForm.PAST:
        return False

    return True


def is_past_perfect(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.PAST_PART:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return False
    
    if auxes[0].lemma_ != "have":
        return False

    aux_form, aux_obj = findVerb(auxes[0])

    if aux_form != VerbForm.PAST:
        return False
    
    return True


def is_past_perfect_continuous(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.PRESENT_PART:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return False
    
    if not (auxes[0].lemma_ == "have" and auxes[1].lemma_ == "be"):
        return False
    
    have_form, have_obj = findVerb(auxes[0])
    be_form, be_obj = findVerb(auxes[1])

    if have_form != VerbForm.PAST or be_form != VerbForm.PAST_PART:
        return False
    
    return True


def is_future_simple(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.BASE:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 1:
        return False
    
    if auxes[0].lemma_ != "will":
        return False

    return True


def is_future_continuous(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.PRESENT_PART:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return False
    
    if auxes[0].norm_ != "will" or auxes[1].norm_ != "be":
        return False

    return True


def is_future_perfect(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.PAST_PART:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 2:
        return False
    
    if auxes[0].norm_ != "will" or auxes[1].norm_ != "have":
        return False
    
    return True


def is_future_perfect_continuous(sent):
    root = sent.root

    if root is None:
        return False
    
    if not root.tag_.startswith("VB"):
        return False
    
    root_form, root_obj = findVerb(root)

    if root_form != VerbForm.PRESENT_PART:
        return False
    
    auxes = [t for t in root.children if t.dep_ == "aux"]

    if len(auxes) != 3:
        return False
    
    if auxes[0].norm_ != "will" or auxes[1].norm_ != "have" or auxes[2].norm_ != "been":
        return False
    
    return True


def handle(sent, source):
    def test(func, sent, current_source: str, task_source: str, tag: str):
        res = func(sent)

        if res == False and current_source == task_source:
            print(tag, sent, current_source, "False")
            return False

        if res == True and current_source != task_source:
            print(tag, sent, current_source, "True")
            return False

        return True

    global wrong_cnt

    res = test(is_present_simple, sent, source, "data/present_simple.txt", "PRESENT_SIMPLE")
    wrong_cnt += 0 if res else 1

    res = test(is_present_continuous, sent, source, "data/present_continuous.txt", "PRESENT_CONTINUOUS")
    wrong_cnt += 0 if res else 1

    res = test(is_present_perfect, sent, source, "data/present_perfect.txt", "PRESENT_PERFECT")
    wrong_cnt += 0 if res else 1

    res = test(is_present_perfect_continuous, sent, source, "data/present_perfect_cont.txt", "PRESENT_PERFECT_CONTINUOUS")
    wrong_cnt += 0 if res else 1

    res = test(is_past_simple, sent, source, "data/past_simple.txt", "PAST_SIMPLE")
    wrong_cnt += 0 if res else 1

    res = test(is_past_continuous, sent, source, "data/past_continuous.txt", "PAST_CONTINUOUS")
    wrong_cnt += 0 if res else 1

    res = test(is_past_perfect, sent, source, "data/past_perfect.txt", "PAST_PERFECT")
    wrong_cnt += 0 if res else 1

    res = test(is_past_perfect_continuous, sent, source, "data/past_perfect_continuous.txt", "PAST_PERFECT_CONTINUOUS")
    wrong_cnt += 0 if res else 1

    res = test(is_future_simple, sent, source, "data/future_simple.txt", "FUTURE_SIMPLE")
    wrong_cnt += 0 if res else 1

    res = test(is_future_continuous, sent, source, "data/future_continuous.txt", "FUTURE_CONTINUOUS")
    wrong_cnt += 0 if res else 1

    res = test(is_future_perfect, sent, source, "data/future_perfect.txt", "FUTURE_PERFECT")
    wrong_cnt += 0 if res else 1

    res = test(is_future_perfect_continuous, sent, source, "data/future_perfect_continuous.txt", "FUTURE_PERFECT_CONTINUOUS")
    wrong_cnt += 0 if res else 1


wrong_cnt = 0
for source in all_sources:
    with (open(source, mode="r")) as f:
        for line in f:
            handle(next(nlp(line.strip()).sents), source)

print("Wrong detections count:", wrong_cnt)