

# 토론 요약 모듈
# summary 요소 반환
def summaraize_debate(debate_id: str):
    #db 조회해서 대화록 받아오기
    #요약 ai 호출
    summary_pro = "찬성측 주장 요약"
    summary_con = "반대측 주장 요약"
    summary_arguments = "전체 변론 요약"
    summary_verdict = "판결 요약"
    summary = {
        "summary_pro" : summary_pro,
        "summary_con" : summary_con,
        "summary_arguments": summary_arguments,
        "summary_verdict" : summary_verdict
    }
    return summary