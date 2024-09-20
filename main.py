# Código para o trabalho com o objetivo de criar um script que reconheça estrutura HTML
#   Feito por: Taynan Pereira

# Importação da Biblioteca de Regex
import re

# Variável representando a string de entrada (input)
input = '<html> <head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>'

tagValidatorRegex = '(<\w+(\s\w+(="((\w+)|([\w-]+:\w+;?))*")?)*\s*>)'


# Criação de uma classe para padronizar informações sobre TAGs HTML encontradas
class HTML_Tag:
    
    def __init__(self, tagName):
        self.Tag_Name = tagName

def checkHTMLIsValid(input):
    
    
    print(input)
    
    
checkHTMLIsValid(input)


        