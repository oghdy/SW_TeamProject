from vlm_processor import get_ingredients
from recipe_ai import generate_recipe
from qa_bot import answer

def run_cli():
    print(" 냉장고 AI 셰프에 오신 것을 환영합니다!")
    
    # 1. 이미지 경로 입력
    img_path = input(" 분석할 냉장고 이미지 경로를 입력하세요: ").strip()
    
    # 2. 식재료 인식
    print("\n 식재료 인식 중입니다...")
    try:
        ingredients = get_ingredients(img_path)
        if not ingredients:
            print(" 재료를 인식하지 못했습니다. 이미지를 다시 확인해주세요.")
            return
        print(" 인식된 재료:", ingredients)
    except Exception as e:
        print(" 재료 인식 실패:", e)
        return
    
    # 3. 레시피 생성
    print("\n 레시피 생성 중입니다... 잠시만 기다려주세요.")
    try:
        recipe = generate_recipe(ingredients)
        print("\n 생성된 레시피:\n")
        print(recipe)
    except Exception as e:
        print(" 레시피 생성 실패:", e)
        return
    
    # 4. 사용자 질문 → LLM 답변
    print("\n 요리에 대해 궁금한 점을 입력해보세요 (엔터만 입력 시 종료)")
    while True:
        question = input("\n 질문: ").strip()
        if question == "":
            print(" 종료합니다. 즐거운 요리 되세요!")
            break
        try:
            reply = answer(question, recipe)
            print(" 답변:", reply)
        except Exception as e:
            print(" 답변 실패:", e)
    # 5. 파일 단독 실행 코드
    
if __name__ == "__main__":
    run_cli()
