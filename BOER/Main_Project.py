import os
import Box_Detection
import FTP_Dinleyici
from datetime import datetime
import time

Local_Path = "C:\\Users\\Kerem\\Desktop\\VSC\\Python\\BOER\\Depo\\" # Local path to download Images
Model_Path = "C:\\Users\\Kerem\\Desktop\\VSC\\my_model\\my_model.pt" #YOLO model path
confidence_threshold = 0.5 # Confidence threshold for object detection

FTP_Address = "192.168.0.12"
FTP_Username = "stajyer"
FTP_Password = "Boer2637#"

Box_Detection.set_model_path(Model_Path)
Box_Detection.set_confidence_threshold(confidence_threshold)

def Update_Filename(filename):
    name_parts = filename.split(".")
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    new_filename = f"{name_parts[0]}_islendi_{date_str}.{name_parts[1]}"
    return new_filename

def main():
    FTP_Dinleyici.FTP_Login(FTP_Address, FTP_Username, FTP_Password)

    # Loop start
    while True:
        new_files = FTP_Dinleyici.check_files(FTP_Dinleyici.ftp)
        if new_files:
            for filename in new_files:
                while not FTP_Dinleyici.size_check(filename):
                    time.sleep(0.1)
                    # FTP_Dinleyici.print_size(filename)
                FTP_Dinleyici.download_file(Local_Path , filename)
            for filename in new_files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Check if file is an image
                    frame = Box_Detection.Open_Image(Local_Path + filename)
                    box_coordinates, box_names, box_confidence = Box_Detection.Detect_Boxes(frame)
                    new_filename = Update_Filename(filename)
                    processed_frame = Box_Detection.Draw_Boxes(frame, box_coordinates, box_names, box_confidence)
                    Box_Detection.Save_Image(processed_frame, Local_Path + new_filename)
                    FTP_Dinleyici.upload_file(Local_Path, new_filename)
                    new_filename = os.path.splitext(new_filename)[0] + ".txt"
                    Box_Detection.Export_Box_Coordinates(box_coordinates, box_names, box_confidence, Local_Path + new_filename)
                    FTP_Dinleyici.upload_file(Local_Path, new_filename)

                elif filename.lower().endswith((".txt", ".csv")):
                    print(f"File is a text or CSV file: {filename}")
        time.sleep(0.5)
        # print("Waiting for new files...")

if __name__ == "__main__":
    main()