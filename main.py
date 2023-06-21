from fastapi import FastAPI, UploadFile, File
from PIL import Image
from fastapi.responses import FileResponse
import shutil
import os
import time

from datetime import datetime

app = FastAPI()
fileName = "dummy.txt"

@app.get("/test")
def cat():
    return FileResponse("myfont/32.png")


@app.post('/read_txt_file')
async def upload_file_and_read(
        file: UploadFile = File(...),
):
    if file.content_type.startswith("text"):
        text_binary = await readTxt(file) # call `await`
        text = text_binary.decode("utf-8")
        response = await file.read()
        BG=Image.open("myfont/bg.png") #path of page(background)photo (I have used blank page)
        sheet_width=BG.width
        gap, ht = 0, 0
        print(str(text_binary.decode()))
        print(await file.read())
        for i in text.replace("\n",""):
            cases = Image.open("myfont/{}.png".format(str(ord(i))))
            BG.paste(cases, (gap, ht))
            size = cases.width
            height=cases.height
            #print(size)
            print("Running...........")
            gap+=size
            if sheet_width < gap or len(i)*115 >(sheet_width-gap):
                gap,ht=0,ht+140
            print(gap)
            print(sheet_width)
            path="generated/" + file.filename + datetime.now().strftime("%m-%d-%Y, %H:%M:%S") + ".png"
            image_path = f"{path}"
        
        BG.save(image_path)
        return FileResponse(image_path)
    else:
        # do something
        response = file.filename
        return response


    

def readTxt(file):
    return file.read()

@app.post("/upload-image")
async def upload_image(image: UploadFile = File(...)):
    # Save the uploaded image to a temporary file
    temp_file = f"temp/{image.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Return the uploaded image as a response
    return FileResponse(temp_file, media_type="image/jpeg")

# Create the temporary directory if it doesn't exist
os.makedirs("generated", exist_ok=True)