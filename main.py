import sqlite3

while True:
    databaseName = "database.db"
    tableName = "images"
    mainDatabase = sqlite3.connect(databaseName)
    crsr = mainDatabase.cursor()

    crsr.execute(f"""
    CREATE TABLE IF NOT EXISTS {tableName} (
        name text,
        data blob
    )
    """)

    mainDatabase.commit()

    action = (input("What do you want to do? (Store / View): ")).lower()

    if action == "store" or action == "s":
        fileName = input("Enter the name of the file you want to store in the database including the file extension: ")

        try:
            with open(fileName, "rb") as f:
                readByte = f.read()
        except Exception as e:
            print("Error, incorrect file name specified!")
            continue

        crsr.execute(f"INSERT INTO {tableName} VALUES (?, ?)", (fileName, readByte))

        print("Successfully completed task!")

        mainDatabase.commit()
        crsr.close()
        mainDatabase.close()
        
    elif action == "view" or action == "v":
        crsr.execute(F"SELECT * FROM {tableName}")
        images = crsr.fetchall()

        for image in images:
            img = image[1]
            imgName = image[0]

            with open(imgName, "wb") as w:
                w.write(img)

        print("Successfully completed task!")

    else:
        print("Invalid Choice")
        continue