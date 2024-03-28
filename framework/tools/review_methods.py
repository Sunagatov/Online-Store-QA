from faker import Faker

fake = Faker()


def generate_fake_review():
    review_body = fake.text(max_nb_chars=1505)

    return {"body": review_body}


text = generate_fake_review()
print(text)
