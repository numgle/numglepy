from enum import Enum
import requests
import json

datasetUrl = "https://raw.githubusercontent.com/numgle/dataset/main/src/data.json"
try:
    req = requests.get(datasetUrl)
except:
    print("Failed to load dataset")
dataset = json.loads(req.text)

class Token(Enum):
    Empty = 1
    CompleteHangul = 2
    NotCompleteHangul = 3
    EnglishUpper = 4
    EnglishLower = 5
    Number = 6
    SpecialLetter = 7
    Unknown = 8

def numglefy(orig):
    result = []
    for i in orig:
        code = ord(i)
        token = getToken(i, code)

        match token:
            case Token.Empty:
                result.append("")
            case Token.CompleteHangul:
                cho, jung, jong = seperateHangul(code)
                if not(isInData(cho, jung, jong)):
                    result.append("")
                elif jung >= 8 and jung != 20:
                    result.append(dataset["jong"][jong] + dataset["jung"][jung - 8] + dataset["cho"][cho])
                else:
                    result.append(dataset["jong"][jong] + dataset["cj"][min(8, jung)][cho])
            case Token.NotCompleteHangul:
                start = dataset["range"]["notCompleteHangul"]["start"]
                result.append(dataset["han"][code - start])
            case Token.EnglishUpper:
                start = dataset["range"]["uppercase"]["start"]
                result.append(dataset["englishUpper"][code - start])
            case Token.EnglishLower:
                start = dataset["range"]["lowercase"]["start"]
                result.append(dataset["englishLower"][code - start])
            case Token.Number:
                start = dataset["range"]["number"]["start"]
                result.append(dataset["number"][code - start])
            case Token.SpecialLetter:
                result.append(dataset["special"][dataset["range"]["special"].index(code)])
    
    return "<br>".join(result)

def getToken(letter, code):
    rangeData = dataset["range"]
    if letter == "" or letter == "\r" or letter == "\n":
        return Token.Empty
    elif code >= rangeData["completeHangul"]["start"] and code <= rangeData["completeHangul"]["end"]:
        return Token.CompleteHangul
    elif code >= rangeData["notCompleteHangul"]["start"] and code <= rangeData["notCompleteHangul"]["end"]:
        return Token.NotCompleteHangul
    elif code >= rangeData["uppercase"]["start"] and code <= rangeData["uppercase"]["end"]:
        return Token.EnglishUpper
    elif code >= rangeData["lowercase"]["start"] and code <= rangeData["lowercase"]["end"]:
        return Token.EnglishLower
    elif code >= rangeData["number"]["start"] and code <= rangeData["number"]["end"]:
        return Token.Number
    elif code in rangeData["special"]:
        return Token.SpecialLetter
    else:
        return Token.Unknown

def seperateHangul(code):
    return [
        int((code - 44032) / 28 // 21),
        int((code - 44032) / 28 % 21),
        int((code - 44032) % 28)
    ]

def isInData(cho, jung, jong):
    if jong != 0 and dataset["jong"][jong] == "":
        return False
    elif jung >= 8 and jung != 20:
        return dataset["jung"][jung - 8] != ""
    else:
        return dataset["cj"][min(8, jung)][cho] != ""