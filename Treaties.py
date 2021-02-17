import os
import sys
import importlib
import numpy as np
import math
from collections import defaultdict
sys.path.append("c:\\users\\pawnshop\\appdata\\local\\programs\\python\\python37-32\\lib\\site-packages")
from collections import Counter
Stopwords=set()
whitelist=set()
wordlist={}
FileArray=[]
Totalwords=defaultdict(int)
Numtreaties=defaultdict(int)
AppArray=[]
Allwords=[] #no longer needed
Anywords=set() #no longer needed
Path='C:\\Users\\PAWNSHOP\\Desktop\\Treaties\\'
Stopfile='C:\\Users\\PAWNSHOP\\Desktop\\stopwords.txt'
Whitefile='C:\\Users\\PAWNSHOP\\Desktop\\whitelist.txt'
#Stopfile provides a list of stopwords, built from an original list found on the internet and supplemented with
#things that in my judgment were not informative; includes common English words, some diplomatic conventional forms,
#numbers, geographically specific terms, etc.
with open(Stopfile) as f:
    for string in f:
        data=string.split('\n')
        Stopwords.add(data[0].lower())
from stop_words import get_stop_words
MoreStopwords=get_stop_words('en')
Stopwords=Stopwords|set(MoreStopwords)
#Whitefile includes terms that should not be left out even if they are found with 2-3 letters or if they have capital
#letters not found at the beginning of sentences. Built by a process of trial and error.
with open(Whitefile) as f: #reads Whitefile into something usable by Python
    for string in f:
        data=string.split('\n')
        for thing in data:
            if thing!='':
                word=thing.split(' ')
                word=word[0].lower()
                whitelist.add(word)
                try:
                    (Stopwords.remove(word))
                except:
                    pass
whitelist.remove('')
Stopwords.add(' ')
FileList=os.listdir(Path)
for FileName in FileList: #Filenames were built using the tribe(s) with whom a treaty was signed and year for ease
    FileArray.append(FileName)
    Applies=[]
    data=FileName.split('_')
    Year=data[-1]
    data.remove(Year)
    Year = Year[0:-4]
    Year=int(Year)
    for thing in data:
        whitelist.add(thing.lower()) #purpose of this is to put tribe names on wordlists
        if thing in Stopwords:       #suspend operation if you want to avoid doing so
            Stopwords.remove(thing)
        if thing.lower() in Stopwords:
            try:
                Stopwords.remove(thing.lower)
            except:
                pass
        if thing=='Shoshoni': #this bit of code addresses the inadvertent use of 2 alternate spellings
            thing='Shoshone'
        if thing=='Chimakuan': #addresses the use of the same name for the language family and tribe
            thing='Chemakum'
        Applies.append(thing) #Applies is a list of tribes, language families, time periods, etc., to which
        #a given treaty applies
        if thing in {'Cherokee','Chickasaw','Choctaw','Creek','Seminole'}:
            Applies.append('FCT')
            Applies.append('South')
        if thing in {'Cherokee','Iroquois','Huron'}:
            Applies.append('Iroquoian')
            if thing!='Cherokee':
                Applies.append('East')
        elif thing in {'Chickasaw','Choctaw','Creek','Seminole','Okmulgee','Tallahassee','Coushatta'}:
            Applies.append('Muskogean')
            Applies.append('South')
        elif thing in {'Apache','Navajo'}:
            Applies.append('Athabaskan')
            Applies.append('Southwest')
        elif thing in {'RogueRiver','Umpqua'}:
            Applies.append('Athabaskan')
            Applies.append('Northwest')
        elif thing in {'Arikara','Caddo','Pawnee','Wichita','Waco','Kitsai','Tawakoni'}:
            Applies.append('Caddoan')
            Applies.append('Plains')
        elif thing in {'Kiowa'}:
            Applies.append('KiowaTanoan')
            Applies.append('Plains')
        elif thing in {'Mandan','Sioux','Crow','Hidatsa','Osage','Quapaw','Winnebago','Iowa','Kansa'}:
            Applies.append('Siouan')
            Applies.append('Plains')
        elif thing in {'Omaha','Otoe','Missouri','Ponca','Assiniboine'}:
            Applies.append('Siouan')
            Applies.append('Plains')
        elif thing in {'CoastSalish','Columbia','Colville','Flathead','Kalispell','Quinault'}:
            Applies.append('Salishan')
            Applies.append('Northwest')
        elif thing in {'Quileute','Chemakum'}:
            Applies.append('Chimakuan')
            Applies.append('Northwest')
        elif thing in {'Molala','NezPerce','Klamath','Modoc','WallaWalla','Umatilla','Yakama'}:
            Applies.append('PlateauPenutian')
            Applies.append('Northwest')
        elif thing in {'Comanche','Shoshone','Ute'}:
            Applies.append('UtoAztecan')
            Applies.append('Southwest')
        elif thing in {'Clackamas','Wasco'}:
            Applies.append('Chinookan')
            Applies.append('Northwest')
        elif thing in {'Makah'}:
            Applies.append('Wakashan')
            Applies.append('Northwest')
        elif thing in {'Tonkawa'}:
            Applies.append('Tonkawan')
            Applies.append('Plains')
        elif thing in {'Kootenai'}:
            Applies.append('Kootenayan')
            Applies.append('Northwest')
        elif thing in {'Natchez'}:
            Applies.append('PresumedGulf')
            Applies.append('South')
        elif thing in {'Kalapuya','Takelma','Cayuse'}:
            Applies.append('PresumedPenutian')
            Applies.append('Northwest')
        elif thing in {'Shasta'}:
            Applies.append('Shastan')
            Applies.append('Northwest')
        elif thing in {'AOC','CSA','Unratified','Canada'}:
            pass
        else:
            Applies.append('Algonquian')
            if thing in {'Delaware','Mahican'}:
                Applies.append('East')
            elif thing in {'Arapaho'}:
                Applies.append('Southwest')
            elif thing=='Blackfeet':
                Applies.append('Northwest')
            else:
                Applies.append('Plains')
        if thing in {'Crow','Blackfeet','Sioux','GrosVentre','Assiniboine','Flathead','Kootenai'}:
            Applies.append('Montana')
        if thing in {'Cheyenne','Cree','Chippewa'}:
            Applies.append('Montana')
    if Year<1789:
        Applies.append('First')
        if 'Canada' not in Applies:
            Applies.append('Early')
    elif Year<1812:
        Applies.append('Second')
        if 'Canada' not in Applies:
            Applies.append('Early')
    elif Year<1832:
        Applies.append('Third')
        if 'Canada' not in Applies:
            Applies.append('Early')
    elif Year<1861:
        Applies.append('Fourth')
        if 'Canada' not in Applies:
            Applies.append('Late')
    elif Year<1872:
        Applies.append('Fifth')
        if 'CSA' not in Applies:
            if 'Canada' not in Applies:
                Applies.append('Late')
                Applies.append('CivilWarEra')
    else:
        Applies.append('Sixth')
        if 'Canada' not in Applies:
            Applies.append('Late')
    if 'FCT' not in Applies:
        Applies.append('OtherTribes')
    if 'Montana' not in Applies:
        Applies.append('NotMontana')
    if ('CSA' not in Applies and 'Canada' not in Applies and 'AOC' not in Applies):
        Applies.append('USA')
    if ('Unratified') not in Applies and 'USA' in Applies:
        Applies.append('RatifiedUSA')
    if ('FCT' in Applies and 'Early' in Applies):
        Applies.append('FCTEarly')
    if ('FCT' in Applies and 'Late' in Applies):
        Applies.append('FCTLate')
    if ('FCT' in Applies or 'Delaware' in Applies or 'Crow' in Applies or 'Hidatsa' in Applies):
        Applies.append('Matrilineal')
    if ('Hopi' in Applies or 'Navajo' in Applies or 'Apache' in Applies or 'Iroquois' in Applies):
        Applies.append('Matrilineal')
    if ('Matrilineal' not in Applies):
        Applies.append('Patrilineal')
    Applies=list(set(Applies)) #removes duplicates
    Applies.append('All')
    AppArray.append(Applies)
    Applies.append(FileName)
    for thing in Applies:
        Numtreaties[thing]+=1
    with open(Path+FileName) as f:
        Newsent=True #This boolean checks whether we would expect a capital letter here to avoid deleting things
        # that should not be deleted
        for string in f:
            line=string.split('\n')
            for thing in line:
                words=thing.split(' ')
                for word in words:
                    if word!='':
                        if word[0]=='$': #Don't care about the particular value, just that the discussion involves $$$
                            word='dollars'
                        newword = '' #Just some cleanup here
                        for char in word:
                            if char in '., ?! /;:-"() [] _ $1234567890':
                                pass
                            elif char == "'":
                                pass
                            else:
                                newword = newword + char
                        word = newword
                        if word=='ball': #sample instruction used to go back to treaties to determine context
                            print(FileName)
                        if word!='':
                            if 'A'<=word[0] and word[0]<='Z': #Removes capitalizations on the assumption that they
                                # are proper nouns
                                if Newsent==False:
                                    if not (word.lower() in whitelist):
                                        Stopwords.add(word.lower())
                            else:
                                if not (word in Stopwords): #Minimizes the accidental exclusion of capitalized words
                                    if len(word)>2:
                                        whitelist.add(word)
                            if word[-1]=='.':
                                Newsent=True
                            else:
                                Newsent=False
                        word=word.lower()
                        if len(word)<3: #We don't need most short words, 3-letter words restored though
                            if word in whitelist:
                                pass
                            else:
                                Stopwords.add(word)
                        if (word in Stopwords)==False:
                            if (word in Anywords)==False: #incuded for bug testing, no longer needed
                                Allwords.append(word)
                            Anywords.add(word)
                            for thing in Applies: #builds a dictionary of word frequencies for each tribe, etc.
                                Totalwords[thing]+=1
                                try:
                                    wordlist[thing][word]+=1
                                except:
                                    try:
                                        wordlist[thing][word]=1
                                    except:
                                        wordlist[thing]={word:1}
def topk(tribe, k): #returns a list of the top k words by frequency for all treaties pertaining to a given tribe
    # with the number of times that word appears
    a=sorted(wordlist[tribe].items(),key=lambda x:x[1],reverse=True)
    if k>0:
        return a[0:k]
    else:
        return a
def particular(tribe1,listtribes,k): #listtribes is a list of tribes, returns the k most frequent words found in
    # tribe1 treaties that are not found in any of the treaties on the other list
    wordlist['temp']=wordlist[tribe1].copy()
    for key in wordlist[tribe1]:
        bad=0
        for tribe2 in listtribes:
            if key in wordlist[tribe2]:
                bad=1
        if bad==1:
            del wordlist['temp'][key]
    return topk('temp',k)

#muchmore function below takes as arguments a tribe (or other key in Wordlist), a list of other tribes, and a factor.
#it returns a dictionary for which the keys are words that are found much more times in the tribe1 treaties than in
#all the other treaties compared to the total number of words in each. The values are a tuple of tuples where the first
#tuple is the total count for tribe1 followed by the per-1000 proportion of the total (non-stop) words in the pertinent
#treaties. The second tuple is the total count for all the treaties pertaining to the tribes in listtribes followed by
# the ratio of percentages, by which the list of words is sorted. So for example
# print(muchmore('CSA',['CivilWarEra'],8)) returns as its first entry ('affix', ((22, 0.14), (1, 46.06))) since 'affix'
# appears 22 times or as .14% of all words in the CSA treaties while it appears only once in the U.S. treaties
# of the same time period for an average frequency about 1/46 as high.


def muchmore(tribe1,listtribes,factor):
    wordlist['temp']={}
    fre1 = sum(wordlist[tribe1].values())
    q=set(list(wordlist[listtribes[0]].keys()))
    fre2=sum(wordlist[listtribes[0]].values())
    if len(listtribes)>1:
        for tribe2 in listtribes[1:]:
            q=q.union(wordlist[tribe2].keys())
            fre2+=sum(wordlist[tribe2].values())
    q=list(q.intersection(set(list(wordlist[tribe1].keys()))))
    for word in q:
        rest=0
        for tribe in listtribes:
            try:
                rest+=wordlist[tribe][word]
            except:
                pass
        m=(1000*wordlist[tribe1][word])/fre1
        n=(1000*rest*factor)/fre2
        if m>n:
#            if wordlist[tribe1][word]>3: #filters out very rare values, can be suspended if desired
                wordlist['temp'][word]=((wordlist[tribe1][word],round(m,2)),(rest,round((m*factor)/n,2)))
    return sorted(wordlist['temp'].items(),key=lambda x:x[1][1][1],reverse=True)
#muchless does the same as muchmore except it prints words that occur much less in the first argument.

def muchless(tribe1,listtribes,factor):
    wordlist['temp'] = {}
    fre1 = sum(wordlist[tribe1].values())
    q = set(list(wordlist[listtribes[0]].keys()))
    fre2 = sum(wordlist[listtribes[0]].values())
    if len(listtribes) > 1:
        for tribe2 in listtribes[1:]:
            q = q.union(wordlist[tribe2].keys())
            fre2 += sum(wordlist[tribe2].values())
    q = list(q.intersection(set(list(wordlist[tribe1].keys()))))
    for word in q:
        rest = 0
        for tribe in listtribes:
            try:
                rest += wordlist[tribe][word]
            except:
                pass
        m = (1000 * wordlist[tribe1][word])*factor / fre1
        n = (1000 * rest ) / fre2
        if n>m:
            wordlist['temp'][word] = ((wordlist[tribe1][word], round(m, 2)), (rest, round((n*factor)/m, 2)))
    return sorted(wordlist['temp'].items(), key=lambda x: x[1][1][1], reverse=True)

#Code below breaks down treaty language for a given tribe by category, based on a file of category assignments.
#Biggest limitation is the large number of words that aren't included in that category file.
#This part of code is more for getting ideas than for returning useful information at this point
Catfile='C:\\Users\\PAWNSHOP\\Desktop\\catlist.txt'
Listcats={}
with open(Catfile) as f:
    for string in f:
        data=string.split('\n')[0]
        if data=='':
            pass
        elif data[0]==data[0].upper():
            word=data
        else:
            Listcats[data]=word
def Catbrdn(tribe):
    Catdict=defaultdict(int)
    for word in wordlist[tribe]:
        if word in Listcats:
            Catdict[Listcats[word]]+=wordlist[tribe][word]
        #else:   #Normally returns something like 2/3 unclassified, suspended to get relative breakdowns
        #    Catdict['unclassified']+=wordlist[tribe][word]
    return Catdict
def Catpct(tribe):
    Catdict=Catbrdn(tribe)
    sv=sum(Catdict.values())
    for k in Catdict:
        print (k, Catdict[k]*100/sv)
#following function builds a vector of word frequencies for a given tribe or descriptive attribute
wordkeys=list(wordlist['All'].keys())
lwkz=len(wordkeys)
def buildvec(tribe):
    vec=np.zeros((lwkz,1))
    cntr=0
    for word in wordkeys:
        try:
            vec[cntr,0]=wordlist[tribe][word]
        except:
            vec[cntr,0]=0
        cntr+=1
    return vec
#following function computes a measure of similarity between two lists
def findsim(tribe1, tribe2):
    firstvec=buildvec(tribe1)
    secondvec=buildvec(tribe2)
    normfirst=math.sqrt(np.transpose(firstvec)@firstvec)
    normsecond=math.sqrt(np.transpose(secondvec)@secondvec)
    firstvec=np.transpose(firstvec)
    simmeas=(firstvec@secondvec)/(normfirst*normsecond)
    return simmeas
def allsims(tribelist):
    enn=len(tribelist)
    cntr1=0
    while cntr1<enn-1:
        cntr2=cntr1+1
        while cntr2<enn:
            print(tribelist[cntr1],tribelist[cntr2],findsim(tribelist[cntr1],tribelist[cntr2]))
            cntr2+=1
        cntr1+=1
# following functions work together to implement multinomial naive Bayes prediction model
def Bayespr(tribelist,target):
    restoflist=tribelist.copy()
    restoflist.remove(target)
    restofset=set(restoflist)
    ltl=len(tribelist)
    winvec=np.zeros((1,ltl))
    Totaltreaties=0
    littleint=0
    count=0
    ndx=tribelist.index(target)
    priorprob=[0]*ltl
    Newvec={}
    relfreq=np.zeros((lwkz,ltl))
    while count<ltl:
        Totaltreaties+=Numtreaties[tribelist[count]]
        count+=1
    count=0
    while count<ltl:
        if count==ndx:
            numer8r=Numtreaties[tribelist[count]]-1 #subtracting 1 for the test treaty
        else:
            numer8r=Numtreaties[tribelist[count]]
        denomin8r=Totaltreaties-1
        if numer8r==0:
            priorprob[count]=-math.inf
        else:
            priorprob[count]=math.log(numer8r/denomin8r)
        Newvec[count]=buildvec(tribelist[count])
        count+=1
    newcntr = 0
    while newcntr < ltl: #every column
        cntr = 0
        while cntr < lwkz: #every row
            const=np.sum(Newvec[newcntr][:,0])
            proportion = (Newvec[newcntr][cntr, 0] + 1/ltl) / (const + 1)
            relfreq[cntr, newcntr] = math.log(proportion)  # additive smoothing
            cntr += 1
        newcntr += 1
    n=len(FileArray)
    ckck=0
    while ckck<n:
        if tribelist[ndx] in AppArray[ckck] and restofset.intersection(AppArray[ckck])==set(): #only gets treaties
                                                                        # assigned to only 1 list element to test
            FileName=FileArray[ckck]
            Filevec=buildvec(FileName)
            predvec=[]
            littleint+=1
            cntr=0
            Countvec = Newvec[ndx] - Filevec
            Countvecsum = np.sum(Countvec[:, 0])
            while cntr<lwkz:
                proportion=(Countvec[cntr,0]+1/ltl)/(Countvecsum+1)
                relfreq[cntr,ndx]=math.log(proportion) #additive smoothing
                cntr+=1

            #above code builds a matrix for which the columns are adjusted relative frequencies for each list element
            summation=np.transpose(Filevec)@relfreq #returns a row vector for which the columns are proportional to the
                                                    #probability based on word count alone
            cntr=0
            while cntr<ltl:
                predvec.append(summation[0,cntr]+priorprob[cntr])
                cntr+=1
            winner=predvec.index(max(predvec))
            winvec[0,winner]+=1
        else:
            pass
        ckck+=1
    return(winvec)
def Bayesauto(tribelist):
    lgth=len(tribelist)
    cmat=np.zeros((lgth,lgth+1)).astype(object)
    itr8r=0
    while itr8r<lgth:
        victor=Bayespr(tribelist,tribelist[itr8r])
        cmat[itr8r, 0:lgth]=victor
        ckv=np.sum(victor[0,:])
        if ckv>0:
            cmat[itr8r,lgth]=tribelist[itr8r]
            cmat[itr8r,lgth]=cmat[itr8r,lgth]+':'+str((victor[0,itr8r]*100/ckv))[0:4]
            cmat[itr8r, lgth] = cmat[itr8r, lgth] + '% classified'
        else:
            cmat[itr8r,lgth]=tribelist[itr8r]+':no distinct treaties'
        itr8r+=1
    print(cmat)
    print(' ',end=' ')
    itr8r=0
    while itr8r<lgth:
        print(itr8r+1,end='   ')
        itr8r+=1
    print('  predicted values below, actual values at right',end='\n')
    itr8r=0
    while itr8r<lgth:
        print (itr8r+1,'=',tribelist[itr8r])
        itr8r+=1
#what follows is execution instructions used to get specific information
print('Early')
Catpct('Early')
print('Late')
Catpct('Late')
print('Canada')
Catpct('Canada')
print('Matrilineal')
Catpct('Matrilineal')
print('Patrilineal')
Catpct('Patrilineal')
print(findsim('First','Second'))
print(findsim('Second','Third'))
print(findsim('Third','Fourth'))
print(findsim('Fourth','Fifth'))
print(findsim('Fifth','Sixth'))
