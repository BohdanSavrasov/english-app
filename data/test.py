from common import *


def is_present_simple(sent):
    root = sent.root

    if root is None:
        return False

    if root.pos_ == "VERB":
        root_form, root_obj = findVerb(root)

        if root_form not in {VerbForm.BASE, VerbForm.THIRDP}:
            return False

        auxes = [t for t in root.children if t.dep_ == "aux"]

        if len(auxes) > 1:
            return False

        if len(auxes) == 1:
            aux_form, aux_obj = findVerb(auxes[0])

            if aux_form not in {VerbForm.BASE, VerbForm.THIRDP}:
                return False

            if aux_obj[VerbForm.BASE] != "do":
                return False

        return True

    if root.pos_ == "AUX" and root.lemma_ == "be":
        auxes = [t for t in root.children if t.dep_ == "aux"]

        if len(auxes) > 0:
            return False

        root_form, root_obj = findVerb(root)

        if root_form not in [VerbForm.BASE, VerbForm.THIRDP]:
            return False

        return True

    return False


def is_present_continuous(sent):
    root = sent.root

    if root is None:
        return False

    if root.pos_ != "VERB":
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

        if aux_form not in [VerbForm.BASE, VerbForm.THIRDP]:
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

    if aux_form not in [VerbForm.BASE, VerbForm.THIRDP]:
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


wrong_cnt = 0
for source in all_sources:
    with (open(source, mode="r")) as f:
        for line in f:
            handle(next(nlp(line.strip()).sents), source)

print("Wrong detections count:", wrong_cnt)