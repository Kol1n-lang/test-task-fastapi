from email.message import EmailMessage

from aiosmtplib import SMTP

from core.configs import all_settings
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker(all_settings.rabbit.rabbit_url)
app = FastStream(broker)


@broker.subscriber("bank-transactions")
async def handle_prediction(user: dict):
    print("Новая транзакция")
    await send_email(to_mail=user["user_email"], amount=user["amount"])


async def send_email(to_mail: str, amount: float):
    message = EmailMessage()
    sender_email = all_settings.external.email_sender
    sender_password = all_settings.external.app_password
    message["From"] = sender_email
    message["To"] = to_mail
    message["Subject"] = "Новая транзкция"
    message.set_content(f"{amount}")
    async with SMTP(
        hostname="smtp.gmail.com",
        port=465,
        use_tls=True,
        username=sender_email,
        password=sender_password,
    ) as smtp:
        print("Sending")
        await smtp.send_message(message)
