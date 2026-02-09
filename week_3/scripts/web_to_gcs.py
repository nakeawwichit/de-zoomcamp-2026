import os
import requests
from google.cloud import storage

# --- ตั้งค่าส่วนตัวของคุณ ---
# แทนที่ด้วยชื่อ Bucket ที่คุณสร้างไว้
BUCKET = "taxi-data-jan-june-2024" 
# แทนที่ด้วยชื่อไฟล์ JSON ที่คุณโหลดมา
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json" 
# -----------------------

def upload_to_gcs(bucket_name, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    print(f"GCS: {object_name} uploaded.")

def load_2024_data():
    service = 'yellow'
    year = '2024'
    # โจทย์กำหนด Jan - June (1-6)
    for i in range(1, 7):
        month = f"{i:02d}"
        file_name = f"{service}_tripdata_{year}-{month}.parquet"
        
        # URL ตรงจาก NYC TLC Website
        request_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
        
        print(f"Downloading: {request_url}")
        r = requests.get(request_url)
        
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)
            
            # อัปโหลดขึ้น GCS (เก็บไว้ใน folder yellow_taxi)
            upload_to_gcs(BUCKET, f"yellow_taxi/{file_name}", file_name)
            
            # ลบไฟล์ในเครื่องทิ้งเพื่อความสะอาด
            os.remove(file_name)
        else:
            print(f"Error downloading {file_name}: Status {r.status_code}")

if __name__ == "__main__":
    load_2024_data()