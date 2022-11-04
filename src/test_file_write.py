
# Used this to test something out


def main():
    FILE_COUNTER = 0
    
    for i in range(10):
        file_name = f'boo{FILE_COUNTER}.txt'
        print(file_name)
        with open(file_name, 'w') as w:
            w.write("BOO")
            FILE_COUNTER += 1
            print(FILE_COUNTER)


if __name__ == '__main__':
    main()