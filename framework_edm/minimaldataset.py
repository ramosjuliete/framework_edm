import pandas as pd
import re
class MinimalDataset:
    def __init__(self, path_sheet, separator, generation_method):
        self.path_sheet = path_sheet
        self.separator = separator
        self.generation_method = generation_method
    
    def log_analysis(self):
        print(f'Data Generation Method: {self.generation_method}')
        print('\n--------- Dataframe Informartion ---------------\n')
        if(self.generation_method=='SQL'):
            #leitura do arquivo e print das informações do dataframe
            df_sgbd = pd.read_csv(self.path_sheet, delimiter=self.separator)
            print(df_sgbd.info())

            #quantificando logs e transformando cada evento encontrando em uma coluna do novo dataframe
            pivot_df_sgbd = df_sgbd.pivot_table(index=['iduser','name'], columns='eventname', aggfunc='size', fill_value=0)
            
            #transformando os nomes dos eventos no padrão com _ ao invés de barra
            loglist = pivot_df_sgbd.columns.tolist()
            new_list = [item.replace("\\\\", "_").replace("_event_", "_").strip("'") for item in loglist]
            pivot_df_sgbd.columns = new_list
            
            # resentando o index do dataframe
            pivot_df_sgbd = pivot_df_sgbd.reset_index()
            return pivot_df_sgbd

        elif(self.generation_method=='MOODLE'):
            df_moodle = pd.read_csv(self.path_sheet, delimiter=self.separator)
            print(df_moodle.info())

            #quantificando logs e transformando cada evento encontrando em uma coluna do novo dataframe
            pivot_df_moodle = df_moodle.pivot_table(index=['iduser','name'], columns='event_name', aggfunc='size', fill_value=0)

            # Substituindo os espaços por underline e removendo os pontos no final
            pivot_df_moodle.columns = pivot_df_moodle.columns.str.replace(' ', '_').str.rstrip('.').str.lower()

            # resentando o index do dataframe
            pivot_df_moodle = pivot_df_moodle.reset_index()
            return pivot_df_moodle

        elif(self.generation_method=='MOODLE_PYTHON'):
            df_moodle = pd.read_csv(self.path_sheet, delimiter=self.separator)
            print(df_moodle.info())

            #quantificando logs e transformando cada evento encontrando em uma coluna do novo dataframe
            pivot_df_moodle = df_moodle.pivot_table(index=['iduser','name'], columns='event_name', aggfunc='size', fill_value=0)

            # Substituindo os espaços por underline e removendo os pontos no final
            pivot_df_moodle.columns = pivot_df_moodle.columns.str.replace(' ', '_').str.rstrip('.').str.lower()

            # resentando o index do dataframe
            pivot_df_moodle = pivot_df_moodle.reset_index()
            return pivot_df_moodle

        else:
            print("Non-existent data generation method!")

        print('\n--------------- Logs successfully quantified and transformed into dataframe ----------------\n')

    def mappingToSRL(self, dataframe):
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

    def joinTime(self, fileTime, dataframe):
        print("Método para junção com tempo de acesso, se necessário")   
        df_time = pd.read_csv(fileTime, delimiter=",")
        #essa renomeação deve acontecer sempre que o arquivo tempo estiver com esquema relacional (userid, total_time_spent)
        # retirar essa linha e colocar o padrão de arquivo de tempo com (iduser, time)
        if(self.generation_method=='SQL'):
            df_time = df_time.rename(columns={'userid': 'iduser', 'total_time_spent': 'time'})
            df_final = pd.merge(dataframe, df_time, on='iduser', how='inner')
            return df_final

        elif(self.generation_method=='MOODLE'):
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

    def loadGrades(self, fileGrade):
        df_grade = pd.read_csv(fileGrade, delimiter=",")
        return df_grade

    def generateMinimalDataset(self,path, dataframe):
        print("Método para finalização do dataset e salvamento do arquivo .csv")
        dataframe.to_csv(path+'generaldataset_'+self.generation_method+'.csv', sep=';', encoding='utf-8', index=False)
