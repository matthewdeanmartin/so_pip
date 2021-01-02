import example._vendor.email_a_tuition_classification.main as emailer

if __name__ == "__main__":
    emailer.send_mail(
        send_from="me",
        send_to=["you"],
        subject="hello",
        message="hello",
    )
