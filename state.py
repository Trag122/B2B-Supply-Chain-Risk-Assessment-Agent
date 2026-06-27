from typing import Dict, List, Optional, TypedDict


class AgentState(TypedDict, total=False):
#Step 3 (Data Extractor)
#Agent kéo từ Mock Database (Core Banking) ra và điền vào hồ sơ   
    application_id: str
    seller_id: str
    seller_name: str
    seller_credit_score: int
    seller_industry: str
#(Từ application > seller_industry: Thông tin xưởng EcoCarton (Khách vay).)
    buyer_id: str
    buyer_name: str
    buyer_industry: str
    market_watch_keywords: str
#Thông tin Siêu thị GreenSupermarket (Đối tác).
    invoice_id: str
    invoice_amount_vnd: int
    advance_rate: float
    requested_advance_amount_vnd: int
    payment_term_days: int
    issue_date: str
    due_date: str
    status: str
#Chi tiết khoản vay cầm cố hóa đơn.
    transactions: List[Dict]
#Lịch sử giao dịch 6 tháng qua.
#Step 4 (Dependency Analyzer)
#Dựa vào transactions ở trên
# hệ thống tính toán bằng toán học (Python) và trả ra kết quả
    buyer_concentration: List[Dict] 
#Danh sách liệt kê EcoCarton đang thu tiền từ những ai.
    dependency_ratio: float #85%
    dependency_summary: str #text tóm tắt mức độ phụ thuộc
#Step 5 (Market Researcher)
#Agent tự động lên mạng gõ phím và chép kết quả mang về:
    search_queries: List[str]
    market_news: List[Dict]
# Step 6: Risk Evaluation
    market_sentiment: str
    risk_level: str
    risk_reasoning: str
    recommendation: str
# Step 8: Human in the loop
    human_decision: Optional[str]
