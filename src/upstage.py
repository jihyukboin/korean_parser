import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

def submit_digitization_request():

    api_key = os.getenv("UPSTAGE_API_KEY")
    file_path = input("파일 경로를 입력하세요 :")

    url = "https://api.upstage.ai/v1/document-digitization"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"document": open(file_path, "rb")}
    data = {
        "model": "document-parse-250618",
        "merge_multipage_tables" : True,
        "ocr": "auto",
        "chart_recognition": True,
        "coordinates": True,
        "output_formats": '["html","text","markdown"]',
        "base64_encoding": '["figure","table","heading1","caption","chart","header","footer","paragraph","list","equation","index","footnote"]',
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    
    # asset/after_parsing 폴더 생성
    output_dir = "asset/after_parsing"
    os.makedirs(output_dir, exist_ok=True)
    
    # 파일명 생성 (현재 시간 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_filename = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(output_dir, f"{original_filename}_request_{timestamp}.json")
    
    # 결과를 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)
    
    print(f"요청 결과가 {output_file}에 저장되었습니다.")



def get_file_list(file_path) :
    
    file_list = os.listdir(file_path)

    return file_list



def async_api() :
    api_key = os.getenv("UPSTAGE_API_KEY")
    filename = input("파일 경로를 입력하세요 :")

    url = "https://api.upstage.ai/v1/document-digitization/async"

    headers = {"Authorization": f"Bearer {api_key}"}

    files = {"document": open(filename, "rb")}

    data = {
    "model": "document-parse-250618",
    "merge_multipage_tables" : True,
    "ocr": "auto",
    "chart_recognition": True,
    "coordinates": True,
    "output_formats": '["html","text","markdown"]',
    "base64_encoding": '["figure","table","heading1","caption","chart","header","footer","paragraph","list","equation","index","footnote"]',
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    print(response.json())

def get_digitization_result(REQUEST_ID):
 
    
    api_key = os.getenv("UPSTAGE_API_KEY")
    
    url = f"https://api.upstage.ai/v1/document-digitization/requests/{REQUEST_ID}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    resp_json = response.json()
    print(resp_json)
    

    

while True :
    
    file_path = input("파일 경로 입력 :")
    for i in  get_file_list(file_path) :
        print(i)
    

    a = int(input("1: 파싱, 2:결과받아오기, 3:종료, 4.비동기파싱: "))

    if a == 1 :
        
        submit_digitization_request()
        
        
    elif a == 2 :
        REQUEST_ID = input("request_id 입력 : ")
        get_digitization_result(REQUEST_ID)

    elif a == 4 :
        
        async_api()

    else :
        break








# asset/영어_교육과정_0_99.pdf              완료!!!!!!!
# asset/영어_교육과정_100_199.pdf           완 !!!
# asset/영어_교육과정_200_299.pdf    ########   에러 ####### (해결완)
# asset/영어_교육과정_200_299_0_9.pdf     C
# asset/영어_교육과정_200_299_10_19.pdf  C 
# asset/영어_교육과정_200_299_20_29.pdf C 
# asset/영어_교육과정_200_299_30_39.pdf C 
# asset/영어_교육과정_200_299_40_49.pdf C 
# asset/영어_교육과정_200_299_50_59.pdf  C 
# asset/영어_교육과정_200_299_60_69.pdf C
# asset/영어_교육과정_200_299_70_79.pdf C
# asset/영어_교육과정_200_299_80_89.pdf C
# asset/영어_교육과정_200_299_90_99.pdf C
# asset/영어_교육과정_300_305.pdf           완료 !!!!!!!!!!!!!!!!!!!
# asset/음악_교육과정_0_95.pdf            완         
# asset/창체_교육과정_0_22.pdf            완료!!!!!!!!!
# asset/체육_교육과정_0_99.pdf            완
# asset/체육_교육과정_100_124.pdf         완 
# asset/총론_초등_교육과정_0_99.pdf   CLAER
# asset/총론_초등_교육과정_100_199.pdf CLAER
# asset/총론_초등_교육과정_200_299.pdf CLAER 
# asset/총론_초등_교육과정_300_399.pdf C
# asset/총론_초등_교육과정_400_499.pdf  ######에러########
# asset/총론_초등_교육과정_400_499_0_49.pdf
# asset/총론_초등_교육과정_400_499_50_99.pdf
# asset/총론_초등_교육과정_500_520.pdf    C  완료 !!!!!!!!!!!!!!!!

