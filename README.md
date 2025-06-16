소프트웨어공학 6팀
20200679 하도윤
20210866 임원석
20210868 장세준
20210881 하승훈
20210988 설동화
20220280 한창하

# 냉장고 사진 기반 레시피 추천 및 조리 보조 시스템


## 시스템 요구사항

1. Python 3.8 이상
2. NVIDIA GPU (CUDA 지원)
3. [Ollama](https://ollama.com/download) 설치

## 설치 방법

1. Ollama 설치 및 설정
   ```bash
   # 1. Ollama 다운로드 및 설치
   # Windows: https://ollama.com/download/windows
   # 설치 후 재부팅 권장

   # 2. Gemma 3 모델 다운로드
   ollama pull gemma3:4b
   ```

2. Python 패키지 설치
   ```bash
   pip install ollama
   ```

## 실행 방법

1. Ollama 서버 실행
   ```bash
   # 별도의 터미널 창에서 실행 (이 창은 계속 열어두어야 함)
   ollama serve
   ```

2. 프로그램 실행
   ```bash
   python main.py
   ```

## 사용 방법

1. 프로그램이 시작되면 냉장고/식재료 이미지의 경로를 입력합니다.
   - 예: `sample_image/sample_image.png`
   - 지원 이미지 형식: PNG, JPG, JPEG

2. VLM이 이미지에서 식재료를 인식하고 목록을 출력합니다.

3. 인식된 식재료를 바탕으로 레시피가 자동 생성됩니다.
   - 요리명
   - 필요한 추가 재료
   - 예상 조리 시간
   - 조리 순서
   - 조리 팁

4. 생성된 레시피에 대해 질문을 할 수 있습니다.
   - 예: "양파는 어떻게 써나요?"
   - 예: "조리 시간은 얼마나 걸리나요?"
   - 종료하려면 엔터키만 입력

## 주의사항

1. GPU 메모리 요구사항
   - 최소 4GB VRAM 필요
   - GTX 1650 이상 권장

2. 이미지 관련
   - 이미지는 선명하고 잘 보이는 것을 사용
   - 너무 많은 물체가 있는 복잡한 이미지는 인식률이 떨어질 수 있음

3. 실행 시 주의사항
   - Ollama 서버가 반드시 실행 중이어야 함
   - 첫 실행 시 모델 로딩에 시간이 걸릴 수 있음

## 문제 해결

1. "Failed to connect to Ollama" 에러
   - Ollama 서버가 실행 중인지 확인
   - 포트 11434가 사용 가능한지 확인

2. "image: unknown format" 에러
   - 이미지 파일 형식 확인 (PNG, JPG, JPEG만 지원)
   - 이미지 파일이 손상되지 않았는지 확인

3. GPU 관련 에러
   - NVIDIA 드라이버 업데이트 필요 여부 확인
   - CUDA 설치 상태 확인

## 기술 스택

- VLM (Vision Language Model): Gemma 3
- LLM (Language Model): Gemma 3
- 이미지 처리: Ollama API
- 프로그래밍 언어: Python 3 
