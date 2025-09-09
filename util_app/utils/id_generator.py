def make_generator():
    counter = 0

    def generate_id():
        nonlocal counter
        counter += 1
        return counter

    return generate_id


generate_id = make_generator()
