def isss(struct):
    for s in struct:
        if s not in ['BCC', 'FCC', 'HCP']:
            return False
    return True


def issss(struct):
    if isss(struct):
        if len(struct) == 1:
            return True
    else:
        return False