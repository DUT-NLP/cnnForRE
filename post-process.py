#! /usr/bin/python3
import re
import collections

string = "Chemical_D015738 Disease_D003693, sdf sdfsdf sdfsfd sdf Chemical_D015738-associated Disease_D003693. A series of six cases. Chemical_D015738 is a histamine H2-receptor antagonist used in inpatient settings for prevention of stress Disease_D014456 and is showing increasing popularity because of its low cost. Although all of the currently available H2-receptor antagonists have shown the propensity to cause Disease_D003693, only two previously reported cases have been associated with Chemical_D015738. The authors report on six cases of Chemical_D015738-associated Disease_D003693 in hospitalized patients who cleared completely upon removal of Chemical_D015738. The pharmacokinetics of Chemical_D015738 are reviewed, with no change in its metabolism in the elderly population seen. The implications of using Chemical_D015738 in elderly persons are discussed."

def GetRelations(cdrfilename):
    relations = []
    with open(cdrfilename, 'r') as cdr:
        for line in cdr:
            if not line.find("CID") == -1:
                relations.append(line.strip())
    return relations
def findRelationsStringV2(string):
    chemTag = "Chemical_"
    chemTaglen = len(chemTag) + 7
    diseTag = "Disease_"
    diseTaglen = len(diseTag) + 7

    chemIndexs = []
    diseIndexs = []
    if string.startswith("3289726"):
        id = 12
    relations = collections.defaultdict(lambda : 0)
    chemToDise = collections.defaultdict(lambda : [])
    diseToChem = collections.defaultdict(lambda : [])

    index = 0
    substrIndex = 0
    while True:
        substrIndex = string[index:].find(chemTag)
        index += substrIndex
        if not substrIndex == -1:
            chemIndexs.append(index)
        else:
            break
        index += chemTaglen
            
    index = 0
    substrIndex = 0
    while True:
        substrIndex = string[index:].find(diseTag)
        index += substrIndex
        if not substrIndex == -1:
            diseIndexs.append(index)
        else:
            break
        index += diseTaglen


    for i in range(len(chemIndexs) - 1):
        chemIndex = chemIndexs[i]
        for diseIndex in diseIndexs:
            if diseIndex > chemIndex and diseIndex < chemIndexs[i + 1]:
                chemToDise[chemIndex].append(diseIndex)
    for diseIndex in diseIndexs:
        try:
            if diseIndex > chemIndexs[len(chemIndexs) - 1]:
                chemToDise[chemIndexs[len(chemIndexs) - 1]].append(diseIndex)
        except:
            pass

    for i in range(len(diseIndexs) - 1):
        diseIndex = diseIndexs[i]
        for chemIndex in chemIndexs:
            if chemIndex > diseIndex and chemIndex < diseIndexs[i + 1]:
                diseToChem[diseIndex].append(chemIndex)
    for chemIndex in chemIndexs:
        try:
            if chemIndex > diseIndexs[len(diseIndexs) - 1]:
                diseToChem[diseIndexs[len(diseIndexs) - 1]].append(chemIndex)
        except:
            pass
    maxLen = 50
    relationWords= ['relation between', 
                    'related to', 
                    'during', 
                    'caused', 
                    'associated', 
                    ' induced', 
                    'lead', 
                    'led to',
                    'leading',
                    'induction of',
                    'until',
                    'included',
                    'causes',
                    'manifests']# 'increased' 'following' 'causes'
    for chemIndex in chemToDise:
        lastDiseIndex = chemIndex
        for diseIndex in chemToDise[chemIndex]:
            findit = False
            segmentStr = string[lastDiseIndex:diseIndex + diseTaglen]
            if len(segmentStr.split(" ")) == 2  \
                and segmentStr.find(". ") == -1 \
                and segmentStr.find(", ") == -1 \
                and len(segmentStr) < maxLen:
                #print(string[chemIndex:diseIndex + diseTaglen])###########
                relations[string[chemIndex:chemIndex + chemTaglen].split("_")[1] + '\t' + string[diseIndex:diseIndex + diseTaglen].split("_")[1] + '\t'] += 1
                findit = True
            else:
                for relationword in relationWords:
                    if not segmentStr.find(relationword) == -1 \
                               and segmentStr.find(". ") == -1 \
                               and segmentStr.find(", ") == -1 \
                               and len(segmentStr) < maxLen:
                        #print(string[chemIndex:chemIndex + chemTaglen] + '\t' + string[diseIndex:diseIndex + diseTaglen])######
                        relations[string[chemIndex:chemIndex + chemTaglen].split("_")[1] + '\t' + string[diseIndex:diseIndex + diseTaglen].split("_")[1] + '\t'] += 1
                        findit = True
            #lastDiseIndex = diseIndex
            # if findit:
            #     break
   
    relationWords= ['after', 
                    'during', 
                    'caused by', 
                    'taking', 
                    'effect of', 
                    'complications of',
                    'treated with', 
                    'releted to',
                    'secondary to']#
    for diseIndex in diseToChem:
        lastChemIndex = diseIndex
        for chemIndex in diseToChem[diseIndex]:
            findit = False
            segmentStr = string[lastChemIndex:chemIndex]
            for relationword in relationWords:
                if not segmentStr.find(relationword) == -1 \
                           and segmentStr.find(". ") == -1 \
                           and segmentStr.find(", ") == -1 \
                           and len(segmentStr) < maxLen:
                    #print(string[chemIndex:chemIndex + chemTaglen] + '\t' + string[diseIndex:diseIndex + diseTaglen])######
                    relations[string[chemIndex:chemIndex + chemTaglen].split("_")[1] + '\t' + string[diseIndex:diseIndex + diseTaglen].split("_")[1] + '\t'] += 1
                    findit = True
            #lastChemIndex = chemIndex
            # if findit:
            #     break
    return relations

def findRelationsString(string):
    chemTag = "Chemical_"
    chemTaglen = len(chemTag) + 7
    diseTag = "Disease_"
    diseTaglen = len(diseTag) + 7

    relations = collections.defaultdict(lambda : 0)
    if string.startswith("24040781"):
        d= 1
    relationWords= ['related', 'during', 'caused', 'associated', 'induced', 'lead', 'leading']# 'increased' 'following'
    tmpstr = str(string)
    chemIndex = tmpstr.find(chemTag)
    while not chemIndex == -1:
        tmpstr = tmpstr[chemIndex:]
        diseIndex = tmpstr.find(diseTag)
        if not diseIndex == -1:
            if len(tmpstr[0:diseIndex + 1].split(" ")) == 2 and tmpstr[0:diseIndex + 1].find(". ") == -1:
                relations[tmpstr[0:chemTaglen].split("_")[1] + "\t" +tmpstr[diseIndex:diseIndex + diseTaglen].split("_")[1] + "\t"] += 1                
            else:
                for relationword in relationWords:
                    if (not tmpstr[0:diseIndex + 1].find(relationword) == -1) and (tmpstr[0:diseIndex + 1].find(". ") == -1):
                        relations[tmpstr[0:chemTaglen].split("_")[1] + "\t" +tmpstr[diseIndex:diseIndex + diseTaglen].split("_")[1] + "\t"] += 1
                        break
        tmpstr = tmpstr[diseIndex:]
        chemIndex = tmpstr.find(chemTag)

    relationWords= ['after', 'during', 'caused by', 'taking', 'effect of', 'complications of', 'by', 'with'] # 'to'
    tmpstr = str(string)
    diseIndex = tmpstr.find(diseTag)
    while not diseIndex == -1:
        tmpstr = tmpstr[diseIndex:]
        chemIndex = tmpstr.find(chemTag)
        if not chemIndex == -1:
            for relationword in relationWords:
                if (not tmpstr[0:chemIndex + 1].find(relationword) == -1) and (tmpstr[0:chemIndex + 1].find(". ") == -1):
                    relations[tmpstr[chemIndex:chemIndex + chemTaglen].split("_")[1] + "\t" +tmpstr[0:diseTaglen].split("_")[1] + "\t"] += 1
                    break
        tmpstr = tmpstr[chemIndex:]
        diseIndex = tmpstr.find(diseTag)
    
    return relations

def findRelations(string):
    chemTag = "Chemical_D"
    diseTag = "Disease_D"

    relations = collections.defaultdict(lambda : 0)
    
    relationWords= ['related', 'during', 'caused', 'associated', 'induced']
    m = re.findall('Chemical_D(?!Chemical_D)*?Disease_D[0-9]*', string)
    for substr in m:
        print(substr)
        if len(substr.split(" ")) == 2:
            #print("########%s" % substr)
            relations[substr[0:len(chemTag) + 6].split("_")[1] + "\t" +substr[-len(diseTag) - 6:].split("_")[1] + "\t"] += 1
            continue
        for rword in relationWords:
            if substr.find(rword):
                relations[substr[0:len(chemTag) + 6].split("_")[1] + "\t" +substr[-len(diseTag) - 6:].split("_")[1] + "\t"] += 1
                break
    
    # relationWords= ['after', 'during', 'caused by', 'taking', 'effect of', 'complications of', 'by', 'with']
    # m = re.findall('Disease_D.*?Chemical_D[0-9]*', string)
    # for substr in m:
    #     #print(substr)
    #     for rword in relationWords:
    #         if substr.find(rword):
    #             print(substr[-len(chemTag) - 6:].split("_")[1]+ "\t" + substr[0:len(diseTag) + 6].split("_")[1]  + "\t")
    #             relations[substr[-len(chemTag) - 6:].split("_")[1]+ "\t" + substr[0:len(diseTag) + 6].split("_")[1]  + "\t"] += 1
    #             break
        

    return relations

relations = findRelations(string)

if __name__ == "__main__":

    relationsPred = {}
    gold = open("/home/laboratory/corpusYang/post-process/my.gold", "w")
    with open("/home/laboratory/corpusYang/post-process/out.txt") as f:
        for line in f:
            id = line.strip().split("|")[0]
            relations = findRelationsStringV2(line.strip())
            for relation in relations:
                gold.write(id + "\t" + "CID" + "\t" + relation + "\n")
                relationsPred[(id + "\t" + "CID" + "\t" + relation).strip()] = True
    relations = GetRelations("/home/laboratory/corpusYang/post-process/CDR_TestSet.PubTator.txt")
    
    relationPredLen = len(relationsPred)
    counter = 0
    for relation in relations:
        try:
            if relationsPred[relation]:
                counter += 1
                relationsPred.pop(relation)
        except:
            print(relation)
            continue
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    for item in relationsPred:
        print(item)
    print("\n")
    print("correct:         {0}".format(counter))
    print("total pred:      {0}".format(relationPredLen))
    print("total relations: {0}".format(len(relations)))
    print("result: %f" % (float(counter) / float(relationPredLen)))