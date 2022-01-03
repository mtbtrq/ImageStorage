import sqlite3
import os

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
        fileName = input("Enter the name of the file you want to store in the database including the file extension (or enter 'a' to store every image in the current directory): ")
        if fileName == "a":
            fileExtension = input("Enter the name of the file type you want to store (e.g: .png, .jpg): ")
            filesInDirectory = os.listdir()
            for file in filesInDirectory:
                if file.endswith(fileExtension):
                    try:
                        with open(file, "rb") as f:
                            readByte = f.read()
                    except Exception as e:
                        print("No PNG files found!")
                        continue

                    crsr.execute(f"INSERT INTO {tableName} VALUES (?, ?)", (file, readByte))

                    print("Successfully completed task!")

                    mainDatabase.commit()
                else:
                    pass
        else:
            try:
                with open(fileName, "rb") as f:
                    readByte = f.read()
            except Exception as e:
                print("Error, incorrect file name specified!")
                continue

            crsr.execute(f"INSERT INTO {tableName} VALUES (?, ?)", (fileName, readByte))

            print("Successfully completed task!")

            mainDatabase.commit()

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
