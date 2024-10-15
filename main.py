# Código para o trabalho com o objetivo de criar um script que reconheça estrutura HTML
#   Feito por: Taynan Pereira

# Importação da Biblioteca de Regex
import re

# Carrega o arquivo HTML
arquivoHTML = open("index.html","r")

# Variável representando a string de entrada (input)
input = arquivoHTML.read()

# Regex que identifica abertura HTML que valida tags que podem conter
# multiplas classes css
iniTagValidatorRegex = '(<\w+(\s(\w+)(="((\w+)|(((\w+-?\w+):(\w+);?)+))*")?)*\s*>)'

# Regex para identificar fechamento de tags
finalTagValidatorRegex = '(<\/\w+>)'

cssRegex = '(\w+):(\w+);?|(\w+)'

# Arrays para guardar aberturas e fechamentos de tags
iniHtmlTags = []
closerHtmlTags = []

# Array com os elementos HTMLs encontrados e suas informações básicas
HTMLTags = []

# Criação de uma classe para padronizar informações sobre TAGs HTML encontradas
class HTML_Tag:
    
    # Metodo executada ao criar um objeto da classe
    def __init__(self, startTag, endTag = None):
        
        self.iniTag = startTag.tagFullContent
        self.startTagIndexes = [startTag.startIndex, startTag.endIndex]
        self.nivel = self.checkNivel()
        self.tagName = self.getTagName()
        self.endTag = endTag
        
        if endTag:
            self.endTag = endTag.tagFullContent
            self.endTagIndexes = [endTag.startIndex, endTag.endIndex]
            self.setInnerContent()
        
        self.setAttributesAndValues()
        # print(vars(self),"\n\n")
    
    # Retorna o nome da tag
    def getTagName(self):
        preparingTag = re.sub(r'[<>\/]','',self.iniTag)
        return re.search(r'\w+',preparingTag).group()
    
    def setAttributesAndValues(self):
        attributes = {}
        subAttributeValues = {}
        fullTag = self.iniTag
        
        # print(re.search(iniTagValidatorRegex,fullTag).groups())
        
        attributeName = re.search(iniTagValidatorRegex,fullTag).groups()[2]
        attributeValue = str(re.search(iniTagValidatorRegex,fullTag).groups()[3])
        attributeValue = re.sub(r'[="]','', attributeValue)
        
        arrayAttributesValues = re.split(';',attributeValue)
        
        
        for subValuesAttributes in arrayAttributesValues :
            if subValuesAttributes:
                subValuesAttributesString = re.findall(cssRegex, subValuesAttributes)[0]
                subAttributeValues[subValuesAttributesString[0]]=subValuesAttributesString[1]
        
        if (attributeName):
            attributes[attributeName] = subAttributeValues
            
        # print(attributes)
        
        self.attributes  = attributes
            
    def setInnerContent(self):
        self.innerHTML = input[self.startTagIndexes[1]:self.endTagIndexes[0]]
    
    
    # Retorna o próprio objeto
    def getObject(self):
        return self
    
    def checkNivel(self):
        slicedInput = input[0:self.startTagIndexes[0]]
    
        numOpenTag = len(re.findall(iniTagValidatorRegex, slicedInput))
        numEndTags = len(re.findall(finalTagValidatorRegex, slicedInput))

        return numOpenTag - numEndTags

class infosTag:
    
    def getTagName(self, tag):
        preparingTag = re.sub(r'[<>\/]','',tag)
        return re.search(r'\w+',preparingTag).group()
    
    def __init__(self,tagFullContent,startIndex,endIndex):
        self.tagFullContent = tagFullContent
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.tagName = self.getTagName(tagFullContent)
    
    
# Função que chega uma entrada de texto HTML
def checkHTMLText(input):
    
    cacheIniTagsInfos = {}
    cacheEndTagsInfos = {}
    
    arrayIniHtmls = re.findall(iniTagValidatorRegex,input)
    arrayCloserHtmls = re.findall(finalTagValidatorRegex,input)
    
    # For que percorre o array que contém todas as tags iniciais
    for iniTag in arrayIniHtmls:
        if not iniTag[0] in cacheIniTagsInfos:
            endTagPositions = re.search(iniTag[0], input).span()
            cacheIniTagsInfos[iniTag[0]] = endTagPositions
        
        else :
            endTagPositions = re.search(iniTag[0], input[cacheIniTagsInfos[iniTag[0]][1]:]).span()
            
            newPositionsAbsolute = [
                endTagPositions[1] + cacheIniTagsInfos[iniTag[0]][0] + 1,
                endTagPositions[1] + cacheIniTagsInfos[iniTag[0]][1] + 1]
            
            cacheIniTagsInfos[iniTag[0]] = newPositionsAbsolute
        
        objectIniTag = infosTag(iniTag[0], endTagPositions[0], endTagPositions[1])
        
        iniHtmlTags.insert(len(iniHtmlTags), objectIniTag)
    
    # For que percorre um array que contém todas as tags de fechamento
    for closerHtml in arrayCloserHtmls:
            
        if not closerHtml in cacheEndTagsInfos:
            endTagPositions = re.search(closerHtml, input).span()
            cacheEndTagsInfos[closerHtml] = endTagPositions
        else :
            endTagPositions = re.search(closerHtml, input[cacheEndTagsInfos[closerHtml][1]:]).span()
            
            newPositionsAbsolute = [
                endTagPositions[1] + cacheEndTagsInfos[closerHtml][0] + 1,
                endTagPositions[1] + cacheEndTagsInfos[closerHtml][1] + 1]
            
            cacheEndTagsInfos[closerHtml] = newPositionsAbsolute
            
        objectEndTag = infosTag(closerHtml, cacheEndTagsInfos[closerHtml][0], cacheEndTagsInfos[closerHtml][1])
        closerHtmlTags.insert(len(closerHtmlTags), objectEndTag)
    
    occurrences = 0
    
    for index, iniTag in enumerate(iniHtmlTags):
        whitEndTag = False
        
        for toCompareIniTag in iniHtmlTags[index + 1:]:
            if (iniTag.tagName == toCompareIniTag.tagName):
                for toCompareEndTag in closerHtmlTags:
                    if(iniTag.tagName == toCompareEndTag.tagName and toCompareEndTag.startIndex > toCompareIniTag.startIndex):
                        occurrences += 1
                    else: break
        
        for toCompareEndTag in closerHtmlTags:
            if (iniTag.tagName == toCompareEndTag.tagName and toCompareEndTag.startIndex > iniTag.startIndex):
                if(occurrences == 0):
                    objectHtml = HTML_Tag(iniTag, toCompareEndTag)
                    HTMLTags.insert(len(HTMLTags),objectHtml)
                    whitEndTag = True
                    break
                else :
                    occurrences -= 1
                    
        if whitEndTag == False:
            objectHtml = HTML_Tag(iniTag)
            HTMLTags.insert(len(HTMLTags),objectHtml)
        
        occurrences = 0

def listAllHTMLObjects(arrayHTML):
    for element in arrayHTML:
        print("\nTag de abertura: ", element.iniTag, "Nivel: ", element.nivel)
        print("Nome da Tag: ", element.tagName, "\nIndex de Inicio e Fim da tag: ", element.startTagIndexes)
        
        if element.attributes:
            attributes = element.attributes
            
            for key in attributes:
                print("Atributos: ", key)
                for attributeKey in attributes[key]:
                    print("Conteudo do", attributeKey, "|Valor: ",attributes[key][attributeKey])
            
        
        if element.endTag:
            print("Inner HTML: ", element.innerHTML)
            print("Tag de fechamento: ", element.endTag, "\nIndex de Inicio e Fim da tag: ", element.endTagIndexes)
        
        print("\n")
    
checkHTMLText(input)
listAllHTMLObjects(HTMLTags)
