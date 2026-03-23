import json
import boto3
import os

glue = boto3.client('glue')

def lambda_handler(event, context):

    print("Evento recebido:", json.dumps(event))
    print("Variáveis:", os.environ)

    try:
        response = glue.start_job_run(
            JobName="glue-job-transform",
            Arguments={
                '--RAW_PATH': os.environ['RAW_PATH'],
                '--REFINED_PATH': os.environ['REFINED_PATH']
            }
        )

        print("Resposta do Glue:", response)

        return {
            'statusCode': 200,
            'body': json.dumps('Glue job iniciado!')
        }

    except Exception as e:
        print("Erro:", str(e))
        raise e
