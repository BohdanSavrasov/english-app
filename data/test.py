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
    
    if root.pos_ == "AUX":
        root_form, root_obj = findVerb(root)

    
    return False


def handle(sent, source):
    res = is_present_simple(sent)

    if res == False and source == "data/present_simple.txt":
        print(sent, source)
        return False

    if res == True and source != "data/present_simple.txt":
        print(sent, source)
        return False
    
    return True

total = 0
for source in all_sources:
    with (open(source, mode="r")) as f:
        for line in f:
            res = handle(next(nlp(line.strip()).sents), source)
            total += 0 if res else 1
print("Wrong detections count:", total)

