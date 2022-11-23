#Módulos
from datetime import datetime, timedelta  
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #Exemplo: Inicia em 9 de Outubro de 2022
    'start_date': datetime(2022, 10, 9),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    #Em caso de erros, tente rodar novamente apenas 1 vez
    'retries': 1,
    #Tente novamente após 30 segundos depois do erro
    'retry_delay': timedelta(seconds=30),
    #Execute uma vez a cada 4 minutos 
    'schedule_interval': '*/4 * * * *'
}



# Exemplo de definição de schedule 
# .---------------- minuto (0 - 59)
# |  .------------- hora (0 - 23)
# |  |  .---------- dia do mês (1 - 31)
# |  |  |  .------- mês (1 - 12) 
# |  |  |  |  .---- dia da semana (0 - 6) (Domingo=0 or 7)
# |  |  |  |  |
# *  *  *  *  * (nome do usuário que vai executar o comando)



# Definimos nossos parâmetros. 
# Vamos agora informar ao nosso DAG o que ele deve fazer. 
# Devemos também definir qual tarefa depende da outra.

with DAG(    
    dag_id='_Webscraping',
    default_args=default_args,
    schedule_interval=None,
    tags=[],
) as dag:    

    #Primeira tarefa 
    RodarScraping = BashOperator(bash_command="python3 app.py", task_id="ExecScraping")

    # Configurar a tarefa x para ser dependente da tarefa RodarScraping
    #RodarScraping >> x