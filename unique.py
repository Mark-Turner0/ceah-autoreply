import random

def main():
    unique = ""
    for i in range(10):
        if random.randint(0, 1):
            unique += chr(random.randint(97, 122))
        else:
            unique += chr(random.randint(48, 57))
    print(unique)

if __name__ == "__main__":
    main()
