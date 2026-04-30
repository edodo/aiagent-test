import sys
import os
import subprocess

def test_environment():
    print("="*60)
    print(" [ AI 표준 환경 및 실습 준비 검증 ]")
    print(f" Python Version: {sys.version.split()[0]}")
    print(f" Current Path: {os.getcwd()}")
    print("="*60)

    # 1. 필수 라이브러리 체크 (기존 기능 유지)
    modules = [
        ("langchain", "RAG 프레임워크"),
        ("langchain_google_genai", "Gemini 연동 모듈"),
        ("google.genai", "구글 차세대 AI SDK"), # 추가된 SDK
        ("chromadb", "벡터 데이터베이스"),
        ("fastapi", "API 서버"),
        ("dotenv", "환경변수 관리")
    ]

    success_count = 0
    missing_modules = []

    for mod_name, description in modules:
        try:
            __import__(mod_name)
            print(f" [+] {mod_name:<25} : 로드 성공")
            success_count += 1
        except ImportError:
            print(f" [X] {mod_name:<25} : 로드 실패 !!!")
            missing_modules.append(mod_name)

    # 2. 핵심 의존성 충돌(Protobuf) 정밀 테스트
    print("-" * 60)
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        # 실제 객체 생성 시도 (Protobuf 버전 충돌 여부 확인)
        test_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="TEMP")
        print(" [+] Protobuf 의존성 체크      : 정상 (충돌 없음)")
    except Exception as e:
        print(f" [X] Protobuf 의존성 체크      : 오류 발생 (교정 필요)")
        print(f"     -> 조치: pip install protobuf==4.25.3 --force-reinstall")

    # 3. .env 파일 및 API 키 설정 체크
    print("-" * 60)
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "GEMINI_API_KEY" in content and "AIza" in content:
                print(" [+] .env 설정 체크           : 정상 (API 키 탐지됨)")
            else:
                print(" [!] .env 설정 체크           : 키 값이 비어있거나 형식이 틀림")
    else:
        print(" [X] .env 파일 없음           : 03_01 실행 전 반드시 생성이 필요합니다.")

    # 4. 실습 파일 존재 여부 체크
    print("-" * 60)
    practice_files = ["03_01_genaiPredict.py", "03_02_genai_embedding.py"]
    for pf in practice_files:
        if os.path.exists(pf):
            print(f" [+] 실습 파일 확인           : {pf} (준비완료)")
        else:
            print(f" [X] 실습 파일 누락           : {pf} 파일을 찾을 수 없습니다.")

    print("="*60)
    if success_count == len(modules):
        print(" >>> [결과] 모든 라이브러리 설치가 확인되었습니다. 실습을 진행하세요!")
    else:
        print(f" >>> [결과] {len(missing_modules)}개의 모듈이 누락되었습니다. 설치가 필요합니다.")

if __name__ == "__main__":
    test_environment()