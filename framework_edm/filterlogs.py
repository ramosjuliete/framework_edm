import re
import pandas as pd
from deep_translator import GoogleTranslator

#Classe criada para fazer a filtragem de logs apenas de estudante em relatórios de logs gerados pelo Moodle IFCDM
#para generalizar essa classe, deve-se criar um método que verifica as colunas do arquivo e atualizar os nomes das colunas no método logfilltering
class FilterLogs():
    def __init__(self, path_sheet, separator):
        self.path_sheet = path_sheet
        self.separator = separator

    #MÉTODO 1 --> método para extrair o id do usuário da coluna descrição
    def extract_id_user(self,description):
        match = re.search(r"user with id '(\d+)'", description)
        if match:
            return match.group(1)  # Retorna o ID capturado
        return None  # Retorna None se não encontrar um ID
    
    #MÉTODO 2 --> método para tradução dos valores da lista de eventos português --> inglês
    def translate_list(self, listEvents, origin='pt', destination='en'):
        translator = GoogleTranslator(source=origin, target=destination)
        return {item: translator.translate(item) for item in listEvents}

    #MÉTODO 3 --> método para filtrar os logs dos usuários estudantes para relatórios de moodle do IF
    # verificar questões de como generalizar as colunas de nome, identificação, etc
    # Talvez buscar o cabeçalho da planilha e trabalhar com ele, ao invés dos nomes colocados manualmente
    #columnGeneral -> Parametro que indica no arquivo de logs qual a coluna do nome do usuário
    #columnFilter -> Parametro que indica no arquivo de estudantes qual a coluna devo usar para filtrar os logs dos nomes dos estudantes
    #columnDescription -> parametro que indica qual coluna contém a descrição do evento para extrair o id do usuário
    def logfilltering(self, columnGeneral, columnFilter, columnDescription, fileStudents, logPathDestination):
        dfLogs = pd.read_csv(self.path_sheet, delimiter=self.separator)
 
        dfStudents = pd.read_csv(fileStudents)

        df_filterlogs = dfLogs[dfLogs[columnGeneral].isin(dfStudents[columnFilter])]


        # Aplicar a função à coluna "Descrição" e criar a nova coluna "id_user"
        df_filterlogs["id_usuario"] = df_filterlogs[columnDescription].apply(self.extract_id_user)

        #antes de salvar padronizar as colunas em inglês
       # traducoes = {
       #     "hora": "hour",
        #    "nome_completo": "name",
       #     "usuario_afetado": "affected_user",
       #     "contexto_evento": "event_context",
       #     "componente": "component",
        #    "nome_evento": "event_name",
        #    "descricao": "description",
       #     "origem": "origin",
       #     "ip": "ip",
        #    "id_usuario": "iduser"
        #}

        #df_filterlogs.rename(columns=traducoes, inplace=True)
        #print(df_filterlogs.head())
        fileSaved = logPathDestination+'logMoodleFilteredNovo.csv'

        print(f'File logMoodleFilteredNovo.csv saved in: {logPathDestination}')

        df_filterlogs.to_csv(fileSaved, index=False) 


    # MÉTODO PARA FILTRAR LOGS DO MOODLE DO CURSO PYTHON 
    # QUANDO RESOLVER O COMENTÁRIO DO MÉTODO ANTERIOR PODERÁ APAGAR ESSE MÉTODO
    def logfillteringPython(self, fileStudents, separatorStudents, logPathDestination):
        dfLogs = pd.read_csv(self.path_sheet, delimiter=self.separator)
        print(dfLogs.columns)

        print(fileStudents)
        dfStudents = pd.read_csv(fileStudents, delimiter=separatorStudents)
        print(dfStudents.head())
        
        df_filterlogs = dfLogs[dfLogs['nome_completo'].isin(dfStudents['id'])]

        print(df_filterlogs.info())

        # Aplicar a função à coluna "Descrição" e criar a nova coluna "id_user"
        df_filterlogs["id_usuario"] = df_filterlogs["descricao"].apply(self.extract_id_user)

        uniqueEvents = df_filterlogs['nome_evento'].unique().tolist()

        translated_events = self.translate_list(uniqueEvents)

        df_filterlogs['nome_evento'] = df_filterlogs['nome_evento'].replace(translated_events)
        df_filterlogs['nome_evento'] = df_filterlogs['nome_evento'].replace('Course', 'Course Viewed')

        #antes de salvar padronizar as colunas em inglês
        traducoes = {
            "hora": "hour",
            "nome_completo": "name",
            "usuario_afetado": "affected_user",
            "contexto_evento": "event_context",
            "componente": "component",
            "nome_evento": "event_name",
            "descricao": "description",
            "origem": "origin",
            "ip": "ip",
            "id_usuario": "iduser"
        }

        df_filterlogs.rename(columns=traducoes, inplace=True)

        fileSaved = logPathDestination+'logMoodlePythonFiltered.csv'

        print(f'File logMoodlePythonFiltered.csv saved in: {logPathDestination}')

        df_filterlogs.to_csv(fileSaved, index=False)

    


        