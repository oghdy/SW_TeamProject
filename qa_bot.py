from ollama import chat

def answer(question: str, recipe_context: str = "") -> str:
    """
    사용자의 요리 관련 질문에 답변합니다.
    
    Args:
        question (str): 사용자의 질문
        recipe_context (str, optional): 레시피 컨텍스트. 기본값은 빈 문자열
        
    Returns:
        str: 질문에 대한 답변
    """
    # 시스템 프롬프트 설정
    system_prompt = """당신은 유저의 요리 조리법 관련 질문에 1~2 문장으로 
    간결하고 정확하게 답변하는 전문 요리 도우미 QA 봇입니다."""
    
    # 메시지 구성
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # 레시피 컨텍스트가 있다면 추가
    if recipe_context:
        messages.append({
            "role": "system", 
            "content": f"Context:\n{recipe_context}"
        })
    
    # 사용자 질문 추가
    messages.append({
        "role": "user",
        "content": question
    })
    
    try:
        # Ollama API를 통해 답변 생성 요청
        response = chat(
            model="gemma3:4b",
            messages=messages,
            options={"temperature": 0.2}  # 낮은 temperature로 일관된 답변 유도
        )
        
        # 응답에서 답변 텍스트 추출
        answer_text = response['message']['content'].strip()
        return answer_text
        
    except Exception as e:
        print(f"답변 생성 중 오류 발생: {e}")
        return f"답변을 생성하는 중 오류가 발생했습니다: {str(e)}"