from ollama import chat

def generate_recipe(ingredients: list[str]) -> str:
    """
    주어진 식재료 목록을 바탕으로 요리 레시피를 생성합니다.
    
    Args:
        ingredients (list[str]): VLM이 인식한 식재료 이름 목록
        
    Returns:
        str: 생성된 레시피 텍스트
    """
    # 식재료 목록을 문자열로 변환
    ingredients_text = ", ".join(ingredients)
    
    # 레시피 생성을 위한 프롬프트 구성
    prompt = f"""
    냉장고에 있는 재료: {ingredients_text}
    
    위 재료들로 만들 수 있는 요리를 한 가지 추천해주세요.
    결과는 반드시 다음 형식으로 보여주세요:
    
    [요리명]
    (요리 이름을 한글로 작성)
    
    [필요한 추가 재료]
    - 현재 없는 재료 중 요리에 필요한 것들을 나열
    - 없다면 "추가 재료 필요 없음"이라고 표시
    
    [예상 조리 시간]
    준비 시간과 조리 시간을 포함한 총 소요 시간
    
    [조리 순서]
    1. 첫 번째 단계
    2. 두 번째 단계
    ...
    
    [조리 팁]
    이 요리를 맛있게 만들기 위한 중요한 팁이나 조언
    """
    
    try:
        # Ollama API를 통해 레시피 생성 요청
        response = chat(
            model="gemma3:4b",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            options={"temperature": 0.7}  # 약간의 창의성 허용
        )
        
        # 응답에서 레시피 텍스트 추출
        recipe_text = response['message']['content'].strip()
        return recipe_text
        
    except Exception as e:
        print(f"레시피 생성 중 오류 발생: {e}")
        return f"레시피를 생성하는 중 오류가 발생했습니다: {str(e)}"