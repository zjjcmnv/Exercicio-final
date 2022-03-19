import json
import boto3

# Configurando o boto3
s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('resultado_votos')

#Função de update e create do item caso não exista dentro do dynatrace. De forma que a chamada seja organizada.
def update_create(item,valor_item):
    result = table.update_item(
        Key={
            'candidato': item,
        },
        UpdateExpression="ADD total_votos :i",
        ExpressionAttributeValues={
            ':i': valor_item,
        },
        ReturnValues="UPDATED_NEW"
    )
    
## Função handler para lidar com a lógica.
def handler(event, context):
    ##Configurando variaveis para controlar o arquivo dentro do bucket.
    bucket = event['Records'][0]['s3']['bucket']['name']
    file = event['Records'][0]['s3']['object']['key']
    ## lógica para pegar conteúdo do arquivo.
    json_object = s3_client.get_object(Bucket=bucket,Key=file)
    json_file = json_object['Body'].read()
    conteudo = json.loads(json_file)
    votos = conteudo['votos']
    ##Definindo variavel para ser utilizada fora do for.
    total_votos = 0
    ##Loop de Adição de votos
    for item in votos:
        total_votos += votos[item]
        update_create(item,votos[item])
        print('Item inserido do dynamodb = '+item+', total'+str(votos[item]))
    ##Adição do total de votos
    update_create('totaldevotos',total_votos)
        

    
    