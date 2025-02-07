import summaraize_debate
from datetime import datetime
#토론 종료 모듈
def end_debate(debate_id : str):
    # debate id 불러와서 유효한지 검사
    # 유효하다면 요약
    # summarize = 
    #status를 end로 변경, end_time 기록.
    """ debate_collection.update_one({
        {"_id": ObjectId(debate_id)},
        {"$set":{
            "end_time":end_time,
            "status": "end",
            "result": evaluate_debate(debate_id),
            "summary": summarize_debate(debate_id)
            }
        }
        })
    """