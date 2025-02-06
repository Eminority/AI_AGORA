
"""
토론 생성
create_debate(topic,participants)
    토론 주제와 참여자를 받아와서 db에 등록


토론 시작
start_debate(debate_id)
    토론 시작


토론 진행
진행중일때:
    발언 순서 관리
    debate_turn_manager(debate_id)
        현재 진행도? 확인(서론, 본론, 결론)
        if 유저의 차례:
            발언 입력 받기.
        
        
        else if AI의 차례:
            ai 발언 생성.
            generate_ai_response(debate_id, object_id)

        발언 기록
        log_speech(debate_id, speeker, message)


if 토론 종료:
    end_debate(debate_id)
    status를 end로 변경, end_time 기록.

    토론 판결
    evaluate_debate(debate_id)

    토론 요약
    summarize_debate(debate_id)
"""