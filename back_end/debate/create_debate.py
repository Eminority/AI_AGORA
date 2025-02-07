from datetime import datetime

# 토론 생성 모듈
# 토론 id 반환
def create_debate(topic: str, participants: list):
    debate_data = {
        "participants": participants,   # 참가자 list
        "topic": topic,                 # 주제
        "status" : "start",             # 상태(start, in_progress, end)
        "debate_log": [],               # 초기에는 비어있을것
        "summary": {
            "summary_pro":"",
            "summary_con":"",
            "summary_arguments":"",
            "summary_verdict":""
        },                              # 내용 요약. 초기에는 비어있을 것
        "start_time": None,  # 토론 시작 시간
        "end_time": None, 
        "result": None
    }

    # MongoDB에 토론 저장
    #result = <debate collection>.insert_one(debate_data)

    return str(result.inserted_id)