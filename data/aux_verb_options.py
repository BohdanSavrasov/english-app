from common import verbs

def aux_verb_options(token):
    if token not in token.sent.root.children:
        return None
    
    if token.pos_ != "AUX":
        return None

    global verbs
    
    negToken = next((c for c in token.head.children if c.dep_ == "neg"), None)
    isJoinedToNegToken = negToken is not None and token.whitespace_ == "" and token.nbor() == negToken
    
    if token.lemma_ not in verbs:
        raise Exception("unknown verb: {verb} (to {lemma}) in sentence \"{sent}\"".format(
            verb=token.norm_,
            lemma=token.lemma_,
            sent=token.sent.text,
        ))
    
    options = list(filter(lambda x: len(x.strip()) != 0, verbs[token.lemma_]))
    dictOptions = set(options)
    dictOptions.discard(token.norm_)

    if isJoinedToNegToken:
        dictOptions.discard('doing')

    dictOptionsLen = len(dictOptions)

    if dictOptionsLen == 0:
        return None
    
    if isJoinedToNegToken:
        nots = [negToken.text] * dictOptionsLen
        return True, list(zip(dictOptions, nots))
    
    return False, list(dictOptions)