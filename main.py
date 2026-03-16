db="data.db"
store=[]


def load_data():
    try:
        file=open(db,"r")
        for line in file:
            parts=line.strip().split(" ", 2)
            if len(parts)==3 and parts[0]=="SET":
                set_in_memory(parts[1], parts[2])
        file.close()
    except FileNotFoundError:
        pass


def set_in_memory(key, value):
    for pair in store:
        if pair[0]==key:
            pair[1]=value
            return
    store.append([key, value])


def get_value(key):
    for pair in store:
        if pair[0]==key:
            return pair[1]
    return None


def persist(key, value):
    file = open(db,"a")
    file.write("SET " + key + " " + value + "\n")
    file.close()


def main():
    load_data()

    while True:
        try:
            command=input().strip()
        except EOFError:
            break

        parts=command.split(" ", 2)

        if parts[0]=="SET" and len(parts)==3:
            key=parts[1]
            value=parts[2]

            set_in_memory(key, value)
            persist(key, value)

            print("OK")

        elif parts[0]=="GET" and len(parts)==2:
            value=get_value(parts[1])

            if value is not None:
                print(value)
            else:
                print("NULL")

        elif parts[0]=="EXIT":
            break

        else:
            print("ERROR")
main()


