import pandas as pd
import re
class MinimalDataset:
    def __init__(self, generation_method, fileDescriptionSRL):
        self.generation_method = generation_method
        self.fileDescriptionSRL = fileDescriptionSRL
    
    #MÉTODO 1 --> método para extrair o id do usuário da coluna descrição
    def extract_id_user(self,description):
        match = re.search(r"user with id '(\d+)'", description)
        if match:
            return match.group(1)  # Retorna o ID capturado
        return None  # Retorna None se não encontrar um ID
    
    #método para filtrar os logs, caso o tipo de método de geração for MOODLE ou MOODLE PYTHON, uma vez que o relatório de logs gerado pelo ambiente Moodle não separa estudantes, professores, administradores
    def logfilltering(self, fileLogs, fileLogsDelimiter, columnGeneral, columnDescription, fileStudents, columnFilter, logPathDestination):
        dfLogs = pd.read_csv(fileLogs, delimiter=fileLogsDelimiter)
 
        #leitura do arquivo que contem os nomes completos dos estudantes conforme nome destacado no relatório de logs
        dfStudents = pd.read_csv(fileStudents)

        #filtrando os logs dos estudantes do relatório completo de logs
        df_filterlogs = dfLogs[dfLogs[columnGeneral].isin(dfStudents[columnFilter])]

        # Aplicar a função à coluna "Descrição" e criar a nova coluna "id_user"
        df_filterlogs["iduser"] = df_filterlogs[columnDescription].apply(self.extract_id_user)

        fileSaved = logPathDestination+'logMoodleFiltered.csv'

        print(f'File logMoodleFiltered.csv saved in: {logPathDestination}')

        df_filterlogs.to_csv(fileSaved, index=False)


    #MÉTODO  -> Método para analise de logs segundo o tipo de log enviado "SQL", "MOODLE", "MOODLE_PYTHON"
    # retorna um dataframe onde cada coluna é um log e os valores é a quantidade de vezes que aquele log aparece
    def log_analysis(self, fileLogs, fileLogsDelimiter, columnIdentifier, columnLogEvent):
        print(f'Data Generation Method: {self.generation_method}')
        print('\n--------- Dataframe Informartion ---------------\n')
        df_logs = pd.read_csv(fileLogs, delimiter=fileLogsDelimiter)
        print(df_logs.info())
        #quantificando logs e transformando cada evento encontrando em uma coluna do novo dataframe
        pivot_df_logs = df_logs.pivot_table(index=[columnIdentifier], columns=columnLogEvent, aggfunc='size', fill_value=0)

        if(self.generation_method=='SQL'):
            #transformando os nomes dos eventos no padrão de uma única barra
            loglist = pivot_df_logs.columns.tolist()
            new_list = [item.replace("\\\\", '\\').strip("'") for item in loglist]
            pivot_df_logs.columns = new_list
            pivot_df_logs = pivot_df_logs.reset_index()
            return pivot_df_logs

        elif(self.generation_method=='MOODLE'):
            # Substituindo os espaços por underline e removendo os pontos no final
            pivot_df_logs.columns = pivot_df_logs.columns.str.replace(' ', '_').str.rstrip('.').str.lower()
            pivot_df_logs = pivot_df_logs.reset_index()
            return pivot_df_logs

        elif(self.generation_method=='MOODLE_PYTHON'):      
            #substituir os nomes dos eventos (colunas) pelo log técnico do moodle presente no arquivo de mapeamento srl
            df_srl = pd.read_csv(self.fileDescriptionSRL, sep=';')
            map_eventos = dict(zip(df_srl['event_name'], df_srl['event_log']))
            pivot_df_logs.rename(columns=map_eventos, inplace=True)
            pivot_df_logs = pivot_df_logs.reset_index()
            return pivot_df_logs
        else:
            print("Non-existent data generation method!")

        print('\n--------------- Logs successfully quantified and transformed into dataframe ----------------\n')


    #MÉTODO  -->   Realiza a criação do dataframe a partir de um CSV contendo o mapeamento de logs em estratégias SRL pré-definidos
    def mappingToSRL(self, dataframe):
        # Lê o CSV com separador ';'
        df = pd.read_csv(self.fileDescriptionSRL, sep=';')

        # Filtra os registros onde 'excluded' é 0

        df_filtrado = df[df['excluded'] == 0]

        # Agrupa os logs por estratégia
        srl_dict = df_filtrado.groupby('srl_estrategy')['event_log'].apply(list).to_dict()

        new_df = dataframe[['iduser']].copy()
        # Realizando a soma das colunas de acordo com o mapeamento
        for attribute, columns in srl_dict.items():
            new_df[attribute] = dataframe[columns].sum(axis=1)

        # Resetando o index
        new_df = new_df.reset_index(drop=True)

        print(f'Log mapping in SRL strategies completed!')

        # Renomeando colunas com uma linha só
        new_df.columns = [
            re.sub(r'_+', '_', re.sub(r'\s+', '_', col.lower().replace('and', '').replace('-', '_'))).strip('_')
            for col in new_df.columns
        ]

        return new_df
       
                
    #MÉTODO ANTIGO --> Método para mapeamento de logs para estratégias SRL --> antes de ter o arquivo 
    def mappingToSRLAntigo(self, dataframe):
        # Copiando as colunas iduser e firtname
        new_df = dataframe[['iduser', 'name']].copy()
        mapping_srl = {}
        if(self.generation_method=='SQL'):
        #aqui tem-se o mapeamento manual realizado por especialistas --> pensar em uma forma de automatizar ou deixar que o usuário faça esse mapeamento manuamente na aplicação antes de entrar aqui no código
            mapping_srl = {
                "seeking_social_assistance": ["_assignsubmission_comments_comment_created", "_core_message_viewed", "_core_user_list_viewed","_mod_forum_assessable_uploaded","_mod_forum_course_module_viewed","_mod_forum_discussion_subscription_created","_mod_forum_discussion_subscription_deleted","_mod_forum_discussion_viewed","_mod_forum_post_created"],
                "goal_setting_planning": ["_assignsubmission_onlinetext_assessable_uploaded", "_assignsubmission_onlinetext_submission_created","_core_course_module_completion_updated","_mod_assign_assessable_submitted","_mod_assign_submission_form_viewed","_mod_quiz_attempt_started","_mod_quiz_attempt_submitted"],
                "self_evaluation": ["_assignsubmission_onlinetext_submission_updated","_gradereport_overview_grade_report_viewed","_gradereport_user_grade_report_viewed","_mod_assign_submission_status_viewed","_mod_forum_post_deleted","_mod_forum_post_updated"],
                "seeking_information": ["_core_blog_external_viewed","_mod_forum_course_searched"],
                "keepinp_records_monitoring": ["_core_course_viewed","_core_dashboard_viewed","_core_tag_added","_core_tag_created","_core_webservice_function_called","_core_webservice_token_created","_core_webservice_token_sent","_mod_assign_course_module_viewed","_mod_url_course_module_viewed"],
                "environmental_structuring": ["_core_user_loggedin","_tool_usertours_step_shown","_tool_usertours_tour_ended","_tool_usertours_tour_started"],
                "reviewing_records": ["_mod_quiz_attempt_summary_viewed","_mod_quiz_attempt_viewed","_mod_quiz_course_module_viewed","_mod_resource_course_module_viewed","_mod_quiz_attempt_reviewed"]
            } 

        elif(self.generation_method=='MOODLE'):
            mapping_srl = {
                'seeking_social_assistance': ['created_signature','list_of_users_viewed','post_created','signature_of_discussion_created','some_content_has_been_published','visualized_discussion'],
                'goal_setting_planning': ['attempted_questionnaire_delivered','attempted_questionnaire_started','conclusion_of_updated_course_activity'],
                'self_evaluation': ['attempt_of_the_viewed_questionnaire','excluded_discussion_signature','excluded_signature','post_deleted','updated_post','user_profile_seen','viewed_vision_report'],
                'keeping_records_monitoring': ['course_viewed','list_of_instances_of_course_module_viewed', 'report_of_a_viewer_of_the_viewed_course', 'sought_course', 'viewed_user_notice_report',  'viewed_course_module'],
                'review_records': ['attempt_of_the_reviewed_questionnaire','summary_of_the_view_of_the_viewed_questionnaire']
            }
        elif(self.generation_method=='MOODLE_PYTHON'):
            mapping_srl = {
                "seeking_social_assistance": ['signature_of_discussion_created','excluded_discussion_signature','comment_created','visualized_discussion','list_of_users_viewed','post_created'],
                "goal_setting_planning": ['a_submission_was_subjected','an_online_text_was_made','attempted_questionnaire_started','attempted_questionnaire_delivered','submission_created','the_user_saved_a_shipment','viewed_submission_form','step_shown','sought_course'],
                "self_evaluation": ['conclusion_of_updated_course_activity','viewed_emblems_listing','the_status_of_submission_was_viewed','updated_post','post_deleted','viewed_user_notice_report','viewed_vision_report','attempt_of_the_reviewed_questionnaire'],
                "keepinp_records_monitoring": ['tag_added_to_an_item','viewed_course_module','course_viewed'],
                "environmental_structuring": ['started_demonstration','finished_demonstration'],
                "reviewing_records": ['attempt_of_the_viewed_questionnaire','summary_of_the_view_of_the_viewed_questionnaire']
            } 

        else:
            print("Non-existent data generation method!")
        
        # Realizando a soma das colunas de acordo com o mapeamento
        for attribute, columns in mapping_srl.items():
            new_df[attribute] = dataframe[columns].sum(axis=1)

        # Resetando o index
        new_df = new_df.reset_index(drop=True)

        print(f'Log mapping in SRL strategies completed!')
        return new_df
    
    #MÉTODO 3 --> Faz a conversão do padrão de tempo de relatório do configurable reports para número inteiro
    def converToSeconds(self, tempo_str):
        # Inicializando as variáveis
        horas, minutos, segundos = 0, 0, 0
    
    # Procurando as partes de horas, minutos e segundos usando expressões regulares
        match_horas = re.search(r'(\d+)\s*horas?', tempo_str)
        match_minutos = re.search(r'(\d+)\s*minutos?', tempo_str)
        match_segundos = re.search(r'(\d+)\s*segundos?', tempo_str)
    
        # Se encontrar as horas, converte para inteiro e atribui
        if match_horas:
            horas = int(match_horas.group(1))
    
        # Se encontrar os minutos, converte para inteiro e atribui
        if match_minutos:
            minutos = int(match_minutos.group(1))
    
        # Se encontrar os segundos, converte para inteiro e atribui
        if match_segundos:
            segundos = int(match_segundos.group(1))
    
        # Calculando o total de segundos
        total_segundos = (horas * 3600) + (minutos * 60) + segundos
    
        return total_segundos

    # MÉTODO 4 --> realiza a junção do dataframe pós mapeamento com o arquivo de tempo enviado pelo ususário
    # PRECISO REVER ESTE MÉTODO E REESCREVÊ-LO PARA TRABALHAR COM ID DO USUÁRIO E NAO COM O NOME NO CASO DE RELATÓRIO DE TEMPO GERADO PELO CONFIGURABLE REPORT
    def joinTime(self, fileTime, dataframe):
        print("Método para junção com tempo de acesso, se necessário")   
        df_time = pd.read_csv(fileTime, delimiter=",")
        #essa renomeação deve acontecer sempre que o arquivo tempo estiver com esquema relacional (userid, total_time_spent)
        # retirar essa linha e colocar o padrão de arquivo de tempo com (iduser, time)
        if(self.generation_method=='SQL'):
            #RETIRA-SE ESSA LINHA: arquivo de tempo deve ser configurado com esquema relacional: iduser, time
            #df_time = df_time.rename(columns={'userid': 'iduser', 'total_time_spent': 'time'})
            df_final = pd.merge(dataframe, df_time, on='iduser', how='inner')
            return df_final

        elif(self.generation_method=='MOODLE'):
            #essa parte precisa ser melhorada, pois o relatório de tempo do configurable report não vem com id
            df_filtrado = df_time[df_time['Nome do aluno'].isin(dataframe['name'])].drop_duplicates(subset='Nome do aluno')

            df_filtrado['tempo_em_segundos'] = df_filtrado['Tempo de dedicação ao curso'].apply(self.converToSeconds)

            df_filtrado = df_filtrado.rename(columns={'Nome do aluno':'name'})

            df_junto = pd.merge(dataframe, df_filtrado, on='name', how='inner')

            df_junto = df_junto.rename(columns={'tempo_em_segundos':'time'})

            df_final = df_junto[['iduser', 'name','seeking_social_assistance','goal_setting_planning','self_evaluation','keeping_records_monitoring','review_records','time']]
            return df_final

        elif(self.generation_method=='MOODLE_PYTHON'):
            df_time = df_time.rename(columns={'id': 'name', 'tempo_curso_segundos': 'time'})
            df_final = pd.merge(dataframe, df_time, on='name', how='inner')
            return df_final

    #MÉTODO 5 --> Método para carregar e retornar um dataframe com notas do usuário
    def loadGrades(self, fileGrade):
        df_grade = pd.read_csv(fileGrade, delimiter=",")
        return df_grade

    #MÉTODO 6 --> Vari receber um dataframe e salvar em arquivo .csv; deve ser chamado após método de log analise, mapeamento e jointime
    def generateMinimalDataset(self,path, dataframe):
        dataframe.to_csv(path+'generaldataset_'+self.generation_method+'.csv', sep=';', encoding='utf-8', index=False)
        print(f"MinimalDataset saved in {path}")
