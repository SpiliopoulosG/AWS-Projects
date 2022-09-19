import json
import requests
import smtplib
import boto3

ssm = boto3.client("ssm", region_name="eu-central-1")

url = ssm.get_parameter(Name='url')
my_email = ssm.get_parameter(Name="MY_EMAIL")  # Your Email
email_to_send = ssm.get_parameter(Name="SEND_EMAIL")  # The Email you want to send to
password = ssm.get_parameter(Name="MY_PASS", WithDecryption=True)  # Your passphrase

url = url['Parameter']["Value"]
my_email = my_email['Parameter']["Value"]
email_to_send = email_to_send['Parameter']["Value"]
password = password['Parameter']["Value"]



def lambda_handler(event, context):
    
    response = requests.get(url)
    res = response.json()

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=email_to_send,
                            msg=f"Subject:Quote of Day\n\n{res[0]['q']}\nFrom {res[0]['a']}")
        connection.close

    return {
        'statusCode': 200,
        'body': json.dumps('Email Sent')
    }
