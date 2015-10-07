from utilis import delay

@delay(3.0)
def jou():
    print("jou")

if __name__ == '__main__':
    jou()
    print("asdasd")
