# vlm_processor_test.py
#
# 이 파일은 '냉장고 사진 기반 레시피 추천 및 조리 보조 시스템' 프로젝트의
# VLM (Vision Language Model) 모듈의 핵심 기능을 테스트하고 시연하는 스크립트입니다.
#
# 주요 기능:
# 1. 사용자로부터 이미지 파일 경로를 입력받습니다.
# 2. Ollama에 호스팅된 Gemma 3 멀티모달 모델을 사용하여 이미지 속 식재료를 인식합니다.
# 3. 인식된 식재료 목록을 파싱하여 파이썬 리스트(list[str]) 형태로 반환합니다.
# 4. 여러 개의 샘플 이미지에 대해 VLM 기능을 테스트하고 결과를 출력합니다.
#
# 개발 담당: 하도운

# --- VLM 모듈 실행을 위한 필수 설정 및 실행 지침 ---
# 다른 팀원들 (특히 통합 담당자)이 이 모듈을 실행하기 전에 다음 사항을 확인해 주세요.
#
# 1. Ollama 파이썬 클라이언트 라이브러리 설치:
#    가상 환경 활성화 후 다음 명령어를 실행합니다.
#    pip install ollama
#
# 2. Ollama 서버 실행 필수:
#    이 코드를 실행하기 전에 별도의 터미널 창에서 Ollama 서버를 시작해야 합니다.
#    ollama serve
#    (이 터미널 창은 닫지 말고 계속 켜두세요.)
#
# 3. Gemma 3 모델 다운로드 필수:
#    Ollama 서버에 Gemma 3 모델이 설치되어 있어야 합니다.
#    ollama pull gemma3:4b
#    (Ollama 서버 시작 전에 한 번만 다운로드하면 됩니다.)

import sys # 시스템 관련 기능 (표준 에러 출력 등)
import json # JSON 데이터 처리 (Ollama API 응답 파싱용)
import re # 정규 표현식 (모델 응답 텍스트 파싱용)
from pathlib import Path # 파일 경로를 객체로 다루기 위함 (경로 존재 여부 확인 등)

# Ollama 파이썬 클라이언트 라이브러리 임포트
# 이 라이브러리는 HTTP 요청 및 Base64 인코딩을 내부적으로 처리하여
# Ollama 서버와 편리하게 통신할 수 있도록 돕습니다.
from ollama import chat 

# 스크립트 시작을 알리는 로그 출력
print("--- Script execution started: vlm_processor_test.py ---")

# --- VLM 모듈의 핵심 함수 ---
# 이 함수는 VLM 담당자가 구현하여 다른 모듈에서 호출할 최종 모듈의 인터페이스입니다.
# 즉, 이 프로젝트에서 다른 팀원(예: 레시피 생성 담당자)이 이 함수를 호출하여
# 이미지로부터 식재료 목록을 얻게 됩니다.
def get_ingredients(image_path: str) -> list[str]:
    """
    이미지 파일 경로를 입력받아 Ollama의 Gemma 3 모델을 사용하여
    이미지 속 식재료 목록을 텍스트로 추출하고, 이를 파싱하여 문자열 리스트로 반환합니다.

    Args:
        image_path (str): 분석할 이미지 파일의 절대 또는 상대 경로.

    Returns:
        list[str]: 이미지에서 인식된 식재료 이름들의 리스트.
                   오류 발생 시 빈 리스트를 반환합니다.
    """
    # 1. 이미지 파일 존재 여부 확인 로직
    # 제공된 image_path가 실제 파일인지 확인합니다.
    if not Path(image_path).is_file():
        print(f"Error: Image file not found at {image_path}", file=sys.stderr)
        return [] # 파일이 없으면 빈 리스트 반환 후 함수 종료

    try:
        # 2. Ollama chat 함수에 전달할 메시지 구성
        # Gemma 3와 같은 멀티모달 모델은 'images' 필드를 통해 이미지 입력을 받습니다.
        # 'content' 필드에는 이미지에 대한 질문(프롬프트)을 작성합니다.
        # 프롬프트는 모델이 원하는 형태로 응답하도록 유도하는 것이 중요합니다 (예: 쉼표로 구분).
        vlm_prompt_text = "What ingredients are shown in this picture? List them only, separated by commas, like 'onion, potato, carrot'."
        
        messages = [
            {"role": "user", 
             "content": vlm_prompt_text,
             "images": [image_path] # 핵심: 이미지 파일 경로를 'images' 리스트에 담아 전달
                                    # Ollama 라이브러리가 이 경로의 이미지를 읽어 Base64로 자동 인코딩합니다.
            }
        ]

        print(f"\n[VLM Module] Sending request to Ollama with image: {image_path}...")
        
        # 3. Ollama chat API 호출
        # chat() 함수를 사용하여 Ollama 서버와 통신합니다.
        # - model: 사용할 LLM/VLM 모델의 이름과 태그 (예: "gemma3:4b").
        # - messages: 대화 이력을 포함하는 메시지 리스트.
        # - options: 모델의 응답 방식 제어 (예: temperature는 창의성, 0.1은 비교적 일관된 답변 유도).
        # - stream=False: 응답을 실시간 스트리밍하지 않고, 모든 응답이 완료된 후 한 번에 받습니다.
        # (참고: ollama.chat() 함수는 timeout 인자를 직접 받지 않으므로 제거되어 있습니다.)
        response = chat(model="gemma3:4b", messages=messages, options={"temperature": 0.1}, stream=False)
        
        # Ollama 모델의 응답에서 실제 텍스트 내용만 추출하여 공백 제거
        raw_vlm_response = response['message']['content'].strip()
        print(f"[VLM Module] Raw Gemma 3 VLM Response: {raw_vlm_response}")

        # 4. 응답 텍스트에서 식재료만 파싱하는 로직
        # 이 부분은 Gemma 3의 실제 응답 패턴에 따라 가장 '효과적'이고 '견고'하게
        # 식재료만 추출하도록 다듬어야 하는 VLM 담당자의 주요 과업입니다.
        parsed_ingredients = []
        if raw_vlm_response:
            # Gemma 3의 응답에서 불필요한 서두 문구들을 정규 표현식을 사용하여 제거
            # 예: "The ingredients are", "I can see", "This image appears to contain" 등
            cleaned_response = re.sub(
                r"^(The ingredients are|The image shows|I can see|Ingredients:|This image appears to contain)\s*", 
                "", 
                raw_vlm_response, 
                flags=re.IGNORECASE # 대소문자 구분 없이 매칭
            ).strip()
            
            # 응답의 마지막에 마침표가 있다면 제거 (깔끔한 파싱을 위함)
            if cleaned_response.endswith('.'):
                cleaned_response = cleaned_response[:-1]
                
            # 쉼표(,)를 기준으로 문자열을 분리하고, 각 요소를 공백 제거 후 리스트에 추가
            # 빈 문자열은 제외합니다.
            parts = [part.strip() for part in cleaned_response.split(',') if part.strip()]
            parsed_ingredients = parts
            
        return parsed_ingredients

    # 예외 처리: Ollama 서버 통신 또는 모델 처리 중 발생할 수 있는 오류를 잡습니다.
    except Exception as e: 
        print(f"\n[VLM Module Error] An error occurred during Ollama chat: {e}", file=sys.stderr)
        
        # 오류 메시지 내용을 기반으로 사용자에게 더 구체적인 힌트를 제공합니다.
        error_message_lower = str(e).lower()
        if "model not found" in error_message_lower or "404" in error_message_lower:
            print("  Hint: Model 'gemma3:4b' not found on Ollama server. Check 'ollama list' or 'ollama pull gemma3:4b'.", file=sys.stderr)
        elif "timeout" in error_message_lower: # 라이브러리 내부에서 발생하는 타임아웃 오류
            print("  Hint: The request timed out. Model might be processing slowly due to large image or low resources. Check Ollama server logs.", file=sys.stderr)
        elif "connection refused" in error_message_lower or "connectionerror" in error_message_lower:
            print("  Hint: Could not connect to Ollama server. Is 'ollama serve' running? (It should be running in a separate terminal.)", file=sys.stderr)
        elif "jsondecodeerror" in error_message_lower:
            print("  Hint: Received an unparseable response from Ollama. Check Ollama server logs for errors or unexpected output.", file=sys.stderr)
        
        return [] # 오류 발생 시 빈 리스트 반환

# --- 메인 실행 블록 ---
# 이 부분은 VLM 모듈의 기능을 테스트하고 시연하기 위한 코드입니다.
# 실제 통합 시에는 '통합 & 발표' 담당자가 이 함수(get_ingredients)를 호출하게 됩니다.
if __name__ == "__main__":
    # 테스트할 이미지 경로들을 리스트로 정의합니다.
    # 이 경로는 실제 이미지 파일의 위치와 일치해야 합니다.
    # 각 팀원마다 테스트할 이미지 경로가 다를 수 있으므로, 자신의 환경에 맞게 수정해야 합니다.
    test_image_paths = [
        r"C:\Users\hadyo\Downloads\swg-main\swg-main\sample_image\sample_image.png",  # 첫 번째 샘플 이미지 경로
        r"C:\Users\hadyo\Downloads\swg-main\swg-main\sample_image\sample_image2.png",  # 두 번째 샘플 이미지 경로
        r"C:\Users\hadyo\Downloads\swg-main\swg-main\sample_image\sample_image3.png"   # 세 번째 샘플 이미지 경로
    ]

    print(f"--- Running VLM Module Test for Multiple Images ---")

    # 각 이미지 경로에 대해 반복하여 VLM 모듈 테스트를 실행합니다.
    for i, image_path in enumerate(test_image_paths):
        print(f"\n===== Testing Image {i+1}: {image_path} =====")
        
        # VLM 모듈의 핵심 함수 호출
        recognized_ingredients = get_ingredients(image_path)

        # 테스트 결과 출력
        if recognized_ingredients:
            print(f"\n[VLM Module Result] Recognized Ingredients: {recognized_ingredients}")
            print(f"Success! The VLM module successfully extracted ingredients for {Path(image_path).name}.")
        else:
            print(f"\n[VLM Module Result] No ingredients recognized or an error occurred for {Path(image_path).name}.")
            print(f"Please check the image, Ollama server status, and VLM parsing logic if this was unexpected.")
        
        print(f"===== Test for Image {i+1} Finished =====")