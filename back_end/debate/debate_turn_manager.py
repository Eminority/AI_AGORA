"""
발언 순서 관리
    debate_turn_manager(debate_id)
        if 끝 : 
            break
        if 유저의 차례:
            발언 입력 받기.
        
        
        else if AI의 차례:
            ai 발언 생성.
            generate_ai_response(debate_id, object_id)

        발언 기록
        log_speech(debate_id, speeker, message)
"""

