import twilio
from twilio.rest import Client

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
from langchain.document_loaders import ApifyDatasetLoader

import os

# variaveis de ambiente para tokens gerais
os.environ["OPENAI_API_KEY"] = "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"
os.environ["APIFY_API_TOKEN"] = "apify_api_F0dQ71Q5UMGCj6FpKgNk7FnD6BDgCF1TZTZv"

# variaveis twilio
twilio_number = '+14155238886'
account_sid = 'ACfa0007b06b1bff16dd42ecdd7402e1b2'
auth_token = '046ee94ebf93a66db3ed6481dcb3ce9b'

# instancia do client twilio
client = Client(account_sid, auth_token)

# inicio de scrapping
apify = ApifyWrapper()

loader = ApifyDatasetLoader(
    dataset_id="o3PAuvYSfqOAtXQmv",
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"] or "", metadata={"source": item["url"]}
    ),
)

index = VectorstoreIndexCreator().from_loaders([loader])

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    phone_number = request.values.get('From', '')
    new_phone_number = phone_number.split(":")[1]

    incoming_message = request.values.get('Body', '').lower()

    result = index.query_with_sources(incoming_message)

    new_message = client.messages.create(
        body=result['answer'],
        from_=f'whatsapp:{twilio_number}',
        to=f'whatsapp:{new_phone_number}'
    )

    return 'Mensagem enviada com sucesso'

if __name__ == '__main__':
    app.run(debug=True)