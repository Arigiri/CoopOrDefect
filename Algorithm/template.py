from typing import List, Dict, Literal

Decision = Literal['C', 'D']

def giveDecision(history: List[Dict[str, tuple[Decision, int]]]) -> Decision:
    """
    Hàm đưa ra quyết định Cooperate ('C') hoặc Defect ('D') dựa trên lịch sử đấu.
    
    Args:
        history: List[Dict[str, tuple[Decision, int]]]
            Lịch sử các lượt đấu, mỗi phần tử là một dict chứa thông tin của một lượt
            Key là tên người chơi (str)
            Value là tuple gồm (quyết định, điểm hiện tại)
            Ví dụ: [{'A': ('D', 0), 'B': ('C', 0)}]
    
    Returns:
        Decision: 'C' cho Cooperate hoặc 'D' cho Defect
    
    Note:
        - Hàm này sẽ bị timeout sau 10 giây
        - Nếu trả về giá trị khác 'C' hoặc 'D', đối thủ sẽ được cộng 5 điểm
    """
    raise NotImplementedError("Implement your decision logic here")
