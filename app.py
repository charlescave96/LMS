from flask import Flask, request, jsonify, send_file
import pandas as pd
import boto3
import os
import uuid  # Import uuid module to generate unique user IDs

app = Flask(__name__)

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_DEFAULT_REGION'))

# Select your DynamoDB table
table = dynamodb.Table('UserSubmissions')

@app.route('/submit', methods=['POST'])
def submit():
    user_id = str(uuid.uuid4())  # Generate a unique userID
    name = request.form['name']
    email = request.form['email']
    team = request.form['team']

    # Insert data into DynamoDB
    table.put_item(
        Item={
            'userID': user_id,  # Use userID as the primary key
            'Name': name,
            'Email': email,
            'Team': team
        }
    )
    return jsonify({"message": "Submitted!", "userID": user_id})

@app.route('/export', methods=['GET'])
def export():
    # Scan the DynamoDB table to get all data
    response = table.scan()
    data = response['Items']
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel('users.xlsx', index=False)

    # Send the file as a response
    return send_file('users.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)