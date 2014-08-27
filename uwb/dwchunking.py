#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#  Copyright (c) 2014 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Jesse Griffin <jesse@distantshores.org>


"""
"""

import os
import sys
import codecs

TMPL = u'''====== {1} ======


===== TFT: =====

<usfm>
{0}
</usfm>


===== UTB: =====

<usfm>
{0}
</usfm>


===== Important Terms: =====

  * **[[:en:uwb:notes:key-terms:example|example]]**
  * **[[:en:uwb:notes:key-terms:example|example]]**
 

===== Translation Notes: =====


    * **bold words**  - explanation
    * **bold words**  - explanation
  
===== Links: =====

  * **[[en/bible-training/notes:43luk/questions/comprehension/01|Luke Chapter 1 Checking Questions]]**
 

**[[en/bible-training/notes:{2}|<<]] | [[en/bible-training/notes:{3}|>>]]**'''


def splice(s):
    chunks = []
    for i in s.split('\n===== '):
        ref, txt = i.split('=====\n', 1)
        ref = ref.strip()
        filepath = getpath(ref.lower())
        if not filepath: continue
        chunks.append([filepath, txt.strip(), ref])
    chunks.sort(key=lambda chunks: chunks[0])
    return chunks

def getpath(r):
    fill = 2
    try:
        book, ref = r.split(' ')
        #bk = books[book]
        c, vv = ref.split(':')
        v = vv.split('-')[0]
        if 'psa' in book.lower():
           fill = 3
        return '{0}/{1}/{2}.txt'.format(book, c.zfill(fill), v.zfill(fill))
    except:
        return False

def writeFile(f, content):
    makeDir(f.rpartition('/')[0])
    out = codecs.open(f, encoding='utf-8', mode='w')
    out.write(content)
    out.close()

def makeDir(d):
    '''
    Simple wrapper to make a directory if it does not exist.
    '''
    if not os.path.exists(d):
        os.makedirs(d, 0755)

def genNav(chunked):
    '''
    Walks the generated folder and creates next and previous links.
    '''
    for e in chunked:
        #e[0] is filepath, e[1] is text, e[2] is ref
        i = chunked.index(e)
        prv = getNav(chunked, i-1)
        nxt = getNav(chunked, i+1)
        writeFile(e[0], TMPL.format(e[1], e[2], prv, nxt))

def getNav(chunked, i):
    if i == -1:
        return ''
    elif i >= len(chunked):
        return ''
    return chunked[i][0]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filetochunk = str(sys.argv[1]).strip()
        if not os.path.exists(filetochunk):
            print 'Directory not found: {0}'.format(filetochunk)
            sys.exit(1)
    else:
        print 'Please specify the file to chunk.'
        sys.exit(1)
    src = codecs.open(filetochunk, encoding='utf-8').read()
    chunked = splice(src)
    genNav(chunked)