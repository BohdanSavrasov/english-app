from common import verbs

def root_verb_options(token):
    if token != token.sent.root:
        return None
    
    if token.pos_ != "VERB":
        return None
    
    global verbs

    if token.lemma_ not in verbs:
        raise Exception("unknown verb: {verb} (to {lemma}) in sentence \"{sent}\"".format(
            verb=token.norm_,
            lemma=token.lemma_,
            sent=token.sent.text,
        ))

    options = list(filter(lambda x: len(x.strip()) != 0, verbs[token.lemma_]))
    dictOptions = set(options)
    dictOptions.discard(token.norm_)
    
    if len(dictOptions) == 0:
        return None
    
    return list(dictOptions)