import json
import boto3

s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('resultado_votos')

def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    file = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket,Key=file)
    json_file = json_object['Body'].read()
    conteudo = json.loads(json_file)
    votos = conteudo['votos']
    total = 0 
    for item in votos:
        total += votos[item]
        table.put_item(Item={'candidato': item,'total': votos[item]})
        print('Item inserido do dynamodb = '+item+', total'+str(votos[item]))
    table.put_item(Item={'candidato': 'totaldevotos','total': total})
    