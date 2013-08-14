from itertools import cycle
import random

def pairup(core, interns=None):
    '''
    Assigns a name to another name. Assumes that the names are unique.
    '''

    # assign the core group
    random.shuffle(core)
    lucky = None
    if len(core) % 2 != 0:
        # pick lucky core person to be alone
        lucky = core.pop()
    pairings = [[core[i], core[i+1]] for i in range(0, len(core)-1, 2)]
    if lucky:
        pairings += [[lucky]]

    # assign them interns
    if interns:
        pairings.sort(key=len) # to prioritize the lucky person
        random.shuffle(interns)
        # round robin style of assigning until we run out of interns
        pairs = cycle(pairings)
        for intern in interns:
            pair = next(pairs)
            pair.append(intern)
    return map(tuple, pairings)


def main():
    core = ['ben', 'dylan', 'jamie', 'guan', 'richard', 'rui', 'alexsandra', 'steve']
    interns = ['pranav', 'angelique', 'kevin', 'andres', 'aron']
    groups = pairup(core, interns)
    for i, group in enumerate(groups):
        print "Group %d" % (i + 1)
        for person in group:
            print "    %s" % person

if __name__ == '__main__':
    main()
