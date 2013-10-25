#!/usr/local/bin/python
#
#   f o r t h . p y
#   Author: Chris Meyers @ 
#           http://openbookproject.net/py4fun/forth/forth.html
#
import sys, re

ds       = []          # The data stack
cStack   = []          # The control struct stack
heap     = [0]*2000    # The data heap
heapNext =  0          # Next avail slot in heap
words    = []          # The input stream of tokens

def main() :
    while 1 :
        pcode = compile()          # compile/run from user
        if pcode == None : print; return
        execute(pcode)

#============================== Lexical Parsing
        
def getWord (prompt="... ") :
    global words
    while not words : 
        try    : lin = raw_input(prompt)+"\n"
        except : return None
        if lin[0:1] == "@" : lin = open(lin[1:-1]).read()
        tokenizeWords(lin)
    word = words[0]
    words = words[1:]
    return word

def tokenizeWords(s) :
    global words                                          # clip comments, split to list of words
    words += re.sub("#.*\n","\n",s+"\n").lower().split()  # Use "#" for comment to end of line

#================================= Runtime operation

def execute (code) :
    p = 0
    while p < len(code) :
        func = code[p]
        p += 1
        newP = func(code,p)
        if newP != None : p = newP

def rAdd (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a+b)
def rMul (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a*b)
def rSub (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a-b)
def rDiv (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a/b)
def rEq  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a==b))
def rGt  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a>b))
def rLt  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a<b))
def rSwap(cod,p) : a=ds.pop(); b=ds.pop(); ds.append(a); ds.append(b)
def rDup (cod,p) : ds.append(ds[-1])
def rDrop(cod,p) : ds.pop()
def rOver(cod,p) : ds.append(ds[-2])
def rDump(cod,p) : print "ds = ", ds
def rDot (cod,p) : print ds.pop()
def rJmp (cod,p) : return cod[p]
def rJnz (cod,p) : return (cod[p],p+1)[ds.pop()]
def rJz  (cod,p) : return (p+1,cod[p])[ds.pop()==0]
def rRun (cod,p) : execute(rDict[cod[p]]); return p+1
def rPush(cod,p) : ds.append(cod[p])     ; return p+1

def rCreate (pcode,p) :
    global heapNext, lastCreate
    lastCreate = label = getWord()      # match next word (input) to next heap address
    rDict[label] = [rPush, heapNext]    # when created word is run, pushes its address

def rDoes (cod,p) :
    rDict[lastCreate] += cod[p:]        # rest of words belong to created words runtime
    return len(cod)                     # jump p over these

def rAllot (cod,p) :
    global heapNext
    heapNext += ds.pop()                # reserve n words for last create

def rAt  (cod,p) : ds.append(heap[ds.pop()])       # get heap @ address
def rBang(cod,p) : a=ds.pop(); heap[a] = ds.pop()  # set heap @ address
def rComa(cod,p) :                                 # push tos into heap
    global heapNext
    heap[heapNext]=ds.pop()
    heapNext += 1

rDict = {
  '+'  : rAdd, '-'   : rSub, '/' : rDiv, '*'    : rMul,   'over': rOver,
  'dup': rDup, 'swap': rSwap, '.': rDot, 'dump' : rDump,  'drop': rDrop,
  '='  : rEq,  '>'   : rGt,   '<': rLt,
  ','  : rComa,'@'   : rAt, '!'  : rBang,'allot': rAllot,

  'create': rCreate, 'does>': rDoes,
}
#================================= Compile time 

def compile() :
    pcode = []; prompt = "Forth> "
    while 1 :
        word = getWord(prompt)  # get next word
        if word == None : return None
        cAct = cDict.get(word)  # Is there a compile time action ?
        rAct = rDict.get(word)  # Is there a runtime action ?

        if cAct : cAct(pcode)   # run at compile time
        elif rAct :
            if type(rAct) == type([]) :
                pcode.append(rRun)     # Compiled word.
                pcode.append(word)     # for now do dynamic lookup
            else : pcode.append(rAct)  # push builtin for runtime
        else :
            # Number to be pushed onto ds at runtime
            pcode.append(rPush)
            try : pcode.append(int(word))
            except :
                try: pcode.append(float(word))
                except : 
                    pcode[-1] = rRun     # Change rPush to rRun
                    pcode.append(word)   # Assume word will be defined
        if not cStack : return pcode
        prompt = "...    "
    
def fatal (mesg) : raise mesg

def cColon (pcode) :
    if cStack : fatal(": inside Control stack: %s" % cStack)
    label = getWord()
    cStack.append(("COLON",label))  # flag for following ";"

def cSemi (pcode) :
    if not cStack : fatal("No : for ; to match")
    code,label = cStack.pop()
    if code != "COLON" : fatal(": not balanced with ;")
    rDict[label] = pcode[:]       # Save word definition in rDict
    while pcode : pcode.pop()

def cBegin (pcode) :
    cStack.append(("BEGIN",len(pcode)))  # flag for following UNTIL

def cUntil (pcode) :
    if not cStack : fatal("No BEGIN for UNTIL to match")
    code,slot = cStack.pop()
    if code != "BEGIN" : fatal("UNTIL preceded by %s (not BEGIN)" % code)
    pcode.append(rJz)
    pcode.append(slot)

def cIf (pcode) :
    pcode.append(rJz)
    cStack.append(("IF",len(pcode)))  # flag for following Then or Else
    pcode.append(0)                   # slot to be filled in

def cElse (pcode) :
    if not cStack : fatal("No IF for ELSE to match")
    code,slot = cStack.pop()
    if code != "IF" : fatal("ELSE preceded by %s (not IF)" % code)
    pcode.append(rJmp)
    cStack.append(("ELSE",len(pcode)))  # flag for following THEN
    pcode.append(0)                     # slot to be filled in
    pcode[slot] = len(pcode)            # close JZ for IF

def cThen (pcode) :
    if not cStack : fatal("No IF or ELSE for THEN to match")
    code,slot = cStack.pop()
    if code not in ("IF","ELSE") : fatal("THEN preceded by %s (not IF or ELSE)" % code)
    pcode[slot] = len(pcode)             # close JZ for IF or JMP for ELSE

cDict = {
  ':'    : cColon, ';'    : cSemi, 'if': cIf, 'else': cElse, 'then': cThen,
  'begin': cBegin, 'until': cUntil,
}
  
if __name__ == "__main__" : main()
