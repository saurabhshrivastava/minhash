import random
import pdb


def minhash (vectors, nh) :
    minhashes = []
    for v in vectors :
        hashes = [None] * nh
        for e in v :
            for i in xrange(nh) :
                h = hash("%d"%i + e)
                hi = hashes[i]
                if (hi is None or h < hi) :
                    hashes[i] = h
        minhashes.append(hashes)
    return minhashes


def lsh (minhashes, b, r, size) :
    lshs = [[set() for _ in xrange(size)] for _ in xrange(b)]
    n = len(minhashes)
    for i in xrange(n) :
        v = minhashes[i]
        for bb in xrange(b) :
            t = tuple([bb]) + tuple(v[bb*r:(bb+1)*r])
            h = hash(t)
            lshs[bb][h%size].add(i)
    return lshs
                



def generate(nv, vl, words) :
    nw = len(words)
    vecs = []
    for i in xrange(nv) :
        v = []
        for i in xrange(vl) :
            r = random.randrange(nw)
            w = words[r]
            v.append(w)
        v.sort()
        vecs.append(v)
    return vecs


def sim(lshs, n) :
    b = len(lshs)
    sims = [[set() for _ in xrange(n)] for _ in xrange(b)]
    for bb in xrange(b) :
        lsh = lshs[bb]
        for s in lsh :
            for i in s :
                for j in s :
                    if i != j :
                        sims[bb][i].add(j)
                        sims[bb][j].add(i)


    simin = {}
    for i in xrange(n) :
        all = set()
        allc = {}
        for bb in xrange(b) :
            for j in sims[bb][i] :
                all.add(j)
                if j not in allc :
                    allc[j] = 1
                else :
                    allc[j] +=1
        m = 0
        ma = None
        for a in all :
            if m < allc[a] :
                m = allc[a]
                ma = a
        simin[i] = (ma, m)

    return simin


def display (vectors, simin, b) :
    n1 = len(simin)
    n2 = len(vectors)
    if n1 != n2 :
        print "display err"
        return
    for i in xrange(n1) :
        s = simin[i]
        if len(s) == 0 : continue
        if s[1]*2 < b : continue
        
        print s
        print vectors[i]
        j = s[0]
        print " ", j
        print " ", vectors[j]
        print
        

def main() :
    file = open("./words1000")
    words = file.read().splitlines()
    n = 10000
    vectors = generate(n, 100, words)

    v = vectors[0][:]
    v[0]= 'a'
    vectors.append(v)
    n += 1

    v = vectors[1][:]
    v[0]= 'b'
    v[1]= 'c'
    vectors.append(v)
    n += 1
    
    
    b = 64
    r = 4
    M = b * r
    minhashes = minhash(vectors, M)
    lshs = lsh(minhashes, b, r, 1024)
    simin = sim(lshs, n)
    display(vectors, simin, b)
    
    

if __name__ == "__main__":
    main()
