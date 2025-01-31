from typing import List, Dict, Literal
import random

Decision = Literal['C', 'D']

def giveDecision(history: List[Dict[str, tuple[Decision, int]]]) -> Decision:
    """
    Bot mẫu đưa ra quyết định ngẫu nhiên giữa Cooperate ('C') và Defect ('D').
    
    Args:
        history: List[Dict[str, tuple[Decision, int]]]
            Lịch sử các lượt đấu
    
    Returns:
        Decision: Ngẫu nhiên 'C' hoặc 'D'
    """
    return random.choice(['C', 'D'])
