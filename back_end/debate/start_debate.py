# 토론 시작 모듈

# 토론이 유효한 경우 True 반환.
def start_debate(debate_id : str):
    # 토론 주제 확인, 참가자 확인.
    
    # 토론 가져오기. 
    #debate = <debate_collection>.find_one({"id":ObjectId(debate_id)})

    # 토론 아이디가 유효한지
    if not debate:
        raise ValueError(f"토론 ID {debate_id}가 존재하지 않습니다.")
    if "start_time" in debate:
        raise ValueError(f"토론 ID {debate_id}는 이미 시작된 토론입니다.")
    
    participants = debate.get("participants", [])

    # 현재 시간 저장
    start_time = datetime.utcnow()
    
    # db에 업데이트
    try : 
        """
        <debate_collection>.update_one(
            {"_id" : ObjectId(debate_id)},
            {"$set": {
                "start_time": start_time,
                "statue":"in_progress"
            }}
        )
        """
        pass
    except Exception as e:
        return False
    
    # 토론이 유효하고 잘 시작되었을 경우
    return True
