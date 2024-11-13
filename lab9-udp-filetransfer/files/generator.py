from PIL import Image, ImageDraw, ImageFont
import csv

def create_image_with_student_id(student_id):
    # 이미지 크기 및 배경 색상 설정
    width = 1280  # 이미지 가로 크기
    height = 720  # 이미지 세로 크기
    background_color = (255, 255, 255)  # 배경색 (흰색)

    # 이미지 생성
    image = Image.new('RGB', (width, height), background_color)

    # 텍스트 삽입
    #student_id = "Welcome ! " + student_id
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/open-sans/OpenSans-Light.ttf', size=30)  # 폰트와 크기 설정
    font = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', size=30)  # 폰트와 크기 설정
    text_width, text_height = draw.textsize("Welcome ! " + student_id, font=font)  # 텍스트 크기 계산
    text_position = ((width - text_width) // 2, (height - text_height) // 2)  # 중앙에 텍스트 위치 계산
    draw.text(text_position, "Welcome ! " + student_id, font=font, fill=(0, 0, 0))  # 텍스트 삽입 (검은색)

    # 이미지 저장
    image_path = f'{student_id}.jpg'
    image.save(image_path)
    print(f'이미지 생성 완료: {image_path}')

# CSV 파일 경로
csv_file_path = './student_ids.csv'

# CSV 파일 읽기
with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # 헤더 행 스킵
    for row in reader:
        student_id = row[0]  # 학번 추출
        create_image_with_student_id(student_id)