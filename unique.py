from random import randint


def main():
    unique = ""
    for i in range(10):
        if randint(0, 1):
            unique += chr(randint(97, 122))
        else:
            unique += chr(randint(48, 57))
    print(unique)


if __name__ == "__main__":
    main()
