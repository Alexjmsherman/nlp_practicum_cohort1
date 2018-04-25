import os
import boto3
import PyPDF2


def lambda_handler(event, context):

    # get document_name for S3 event record
    document_name = event['Records'][0]['s3']['object']['key']
    download_path = '/tmp/{}'.format(document_name)

    # download document to tmp
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('guild-annual-report')
    bucket.download_file(document_name,download_path)
    
    print('start processing: {}'.format(document_name))
    
    # extract document text
    text = []
    pdfFileObj = open(download_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    for page_num in range(0,num_pages):
        pageObj = pdfReader.getPage(page_num)
        page_text = pageObj.extractText()
        text.append(page_text)
    all_text = ' '.join(text)

    print('complete processing: {}'.format(document_name))

    # connect to dynamodb table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('annual_report')
    
    # insert a record into the table
    table.put_item(
       Item={
            'document_name': document_name,
            'document_text': all_text[0:250],
        }
    )
    print('inserted text for: {}'.format(document_name))