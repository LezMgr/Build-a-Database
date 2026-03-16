import sys
import os

#The file where we keep our data
db = "data.db"
#List instead of dict
data=[]

def load():
    if not os.path.exists(db):
        # Create the file if it doesn't exist yet
        f=open(db,"w")
        f.close()
        return

    with open(db,"r") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            
            parts=line.split(" ",2)
            if len(parts)==3 and parts[0]=="SET":
                k,v=parts[1], parts[2]
                update_list(k,v)

def update_list(k, v):
    found=False
    for item in data:
        if item[0]==k:
            item[1]=v
            found=True
            break
    if not found:
        data.append([k,v])

def main():
    load()
    # Read from stdin line by line
    for cmd_line in sys.stdin:
        cmd_line=cmd_line.strip()
        if not cmd_line:
            continue
            
        chunks=cmd_line.split(" ", 2)
        action=chunks[0].upper()

        if action=="SET" and len(chunks)==3:
            key_name=chunks[1]
            val_name=chunks[2]
            
            # 1. Update our memory list
            update_list(key_name, val_name)
            
            # 2. Write to the end of the file (append mode)
            with open(db, "a") as f:
                f.write("SET " + key_name + " " + val_name + "\n")
            
            print("OK", flush=True)

        elif action=="GET" and len(chunks)==2:
            search_key=chunks[1]
            result=""
        
            for item in data:
                if item[0]==search_key:
                    result=item[1]
                    break
            
            print(result, flush=True)

        elif action=="EXIT":
            break
        
        else:
            print("ERROR", flush=True)

if __name__=="__main__":
    main()