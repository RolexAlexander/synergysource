from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()  # Get the JSON body of the request
    response = process_webhook(data)  # Pass the data to your processing function
    return {"status": "success", "data": response}


def process_webhook(data):
    # Your custom logic to process the webhook data
    # This function can do whatever you need with the data
    return {"message": "Webhook processed successfully", "received_data": data}


if __name__ == '__main__':
    app.run(debug=True)
