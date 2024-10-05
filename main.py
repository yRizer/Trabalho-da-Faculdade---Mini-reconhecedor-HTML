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
iniTagValidatorRegex = '(<\w+(\s\w+(="((\w+)|([\w-]+:\w+;?))*")?)*\s*>)'

# Regex para identificar fechamento de tags
finalTagValidatorRegex = '(<\/\w+>)'

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
        self.endTag = endTag.tagFullContent
        self.startTagIndexes = [startTag.startIndex, startTag.endIndex]
        self.endTagIndexes = [endTag.startIndex, endTag.endIndex]
        
        print(vars(self))
    
    # Retorna o nome da tag
    def getTagName(self, tag):
        preparingTag = re.sub(r'[<>\/]','',tag)
        return re.search(r'\w+',preparingTag).group()
    
    # Retorna o próprio objeto
    def getObject(self):
        return self

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
        endTagPositions = re.search(iniTag[0], input).span()
        objectIniTag = infosTag(iniTag[0], endTagPositions[0], endTagPositions[1])
        
        iniHtmlTags.insert(len(iniHtmlTags), objectIniTag)
    
    # For que percorre um array que contém todas as tags de fechamento
    for closerHtml in arrayCloserHtmls:
            
        if not closerHtml in cacheEndTagsInfos:
            endTagPositions = re.search(closerHtml, input).span()
            cacheEndTagsInfos[closerHtml] = endTagPositions
            
        else :
            endTagPositions = re.search(closerHtml, input[cacheEndTagsInfos[closerHtml][1]:]).span()
            cacheEndTagsInfos[closerHtml] = endTagPositions
        # print(cacheEndTagsInfos)
        
        objectEndTag = infosTag(closerHtml, endTagPositions[0], endTagPositions[1])
        closerHtmlTags.insert(len(closerHtmlTags), objectEndTag)
    
    occurrences = 0
    
    for index, iniTag in enumerate(iniHtmlTags):
        
        for toCompareIniTag in iniHtmlTags[index + 1:]:
            
            if (iniTag.tagName == toCompareIniTag.tagName):
                occurrences += 1
        
        for toCompareEndTag in closerHtmlTags:
            
            if (iniTag.tagName == toCompareEndTag.tagName):
                # print(vars(iniTag),"\n",vars(toCompareEndTag),"\n\n")
                if(occurrences == 0):
                    
                    objectHtml = HTML_Tag(iniTag, toCompareEndTag)
                    # HTMLTags.insert(len(HTMLTags),objectHtml.getObject())
                    break
                else :
                    occurrences -= 1
                    
        occurrences = 0
        # continue
        
    
checkHTMLText(input)