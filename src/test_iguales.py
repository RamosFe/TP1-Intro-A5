



with open("test_with_me.txt", "rb") as file1:
    with open("prueba_1.txt", "rb") as file2:
        if file1.read() == file2.read():
            print("They are the same")
        else:
            print("They are different")



