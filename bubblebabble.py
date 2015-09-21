import sha
import md5

VOWELS = list('aeiouy')
CONSONANTS = list('bcdfghklmnprstvzx')
CONSONANTSinv = {c:i for i,c in enumerate(CONSONANTS)}

def bubble_babble(message):
    """Encode a message in bubblebabble format. 

    The Bubble Babble Binary Data Encoding
    ftp://ftp.ietf.org/ietf-mail-archive/secsh/2001-08.mail

    The Bubble Babble Encoding encodes arbitrary binary data into
    pseudowords that are more natural to humans and that can be
    pronounced relatively easily.


    Code is an adapted from the following Perl module: Digest::BubbleBabble v0.01
    http://search.cpan.org/~btrott/Digest-BubbleBabble-0.01/BubbleBabble.pm

    Copied from http://code.activestate.com/recipes/413035-encode-messages-and-message-digests-in-bubble-babb/
    """
    if isinstance(message,(int,long)):
        mval = int2bytebase(message)
    else:
        mval = [ord(str(x)) for x in message]
    r = bubble_babble_int(mval)
    return r

def int2bytebase(x):
    r=[] if x>0 else [0]
    while x>0:
        r.append(x%256)
        x //= 256
    return r[::-1]

def check(message):
    "Checks bubble-babble message for integrity DOESNT WORK"
    parts = message.split("-")
    for i,(a,b,c,d,e) in enumerate(parts):
        print (a-CONSONANTSinv[i])%6 , "< 4"
        print (c-CONSONANTSinv[i])%6 , "< 4"
 

def bubble_babble_int(mval):
    assert len(mval)==0 or min(mval)>=0, "Encoded message items must be non-negative"
    assert len(mval)==0 or max(mval)<256, "Encoded message items must be <256"
    seed = 1
    mlen = len(mval)
    rounds = mlen // 2 + 1
    encparts = ['x']
    eextend = encparts.extend
    for i in xrange(rounds):
        if (i + 1 < rounds) or (mlen % 2 != 0):
            imval2i = int(mval[2 * i])
            idx0 = (((imval2i >> 6) & 3) + seed) % 6
            idx1 = (imval2i >> 2) & 15
            idx2 = ((imval2i & 3) + seed // 6) % 6
            eextend([VOWELS[idx0], CONSONANTS[idx1], VOWELS[idx2]])
            if (i + 1 < rounds):
                imval2i1 = int(mval[2 * i + 1])
                idx3 = (imval2i1 >> 4) & 15
                idx4 = imval2i1 & 15
                eextend([CONSONANTS[idx3], '-', CONSONANTS[idx4]])
                seed = (seed * 5 + imval2i * 7 + imval2i1) % 36
        else:
            idx0 = seed % 6
            idx1 = 16
            idx2 = seed // 6
            eextend([VOWELS[idx0], CONSONANTS[idx1], VOWELS[idx2]])
    eextend(['x'])
    encoded = ''.join(encparts)
    return encoded


def digestbb(message, algo=sha):
    """Compute the digest of a message in Bubble Babble format."""
    mdigest = algo.new()
    mdigest.update(message)
    return bubble_babble(mdigest.digest())


if __name__ == '__main__':
    assert bubble_babble('') == 'xexax'
    assert bubble_babble('1234567890') == 'xesef-disof-gytuf-katof-movif-baxux'
    assert bubble_babble('Pineapple') == 'xigak-nyryk-humil-bosek-sonax'
    assert digestbb('foo',algo=sha) == 'xedov-vycir-hopof-zofot-radoh-tofyt-gezuf-sikus-dotet-pydif-faxux'
    assert digestbb('foo',algo=md5) == 'xorar-takyt-rufys-davuh-suruv-zinog-zifos-genet-moxix'
