# PoC: B2B Supply Chain Risk Assessment Agent

## Tác nhân AI đánh giá rủi ro chuỗi cung ứng B2B cho SME

An autonomous AI agent for SME supply chain credit risk assessment, designed for invoice financing and factoring use cases.

---

## 1. Project Overview / Tổng Quan Dự Án

### English

Traditional B2B credit approval processes often rely on static, historical financial statements. This creates a major blind spot: an SME may appear financially healthy while its largest buyer, supplier, or supply chain partner is facing a sudden liquidity crisis.

This Proof of Concept applies an agentic workflow architecture to build an autonomous AI agent that can:

- Analyze transaction relationships to identify critical supply chain dependencies.
- Trigger external search tools (DuckDuckGo) to retrieve real-time market news and sentiment about key counterparties.
- Evaluate contagion risk using Google Gemini (2.5 Flash) and generate a data-driven credit recommendation.
- Pause the workflow for human approval before any final credit decision is made.

### Tiếng Việt

Trong quy trình phê duyệt tín dụng B2B truyền thống, các tổ chức tài chính thường đánh giá rủi ro dựa trên báo cáo tài chính lịch sử. Cách tiếp cận này tạo ra một điểm mù lớn: một SME có thể trông có vẻ ổn định, nhưng khách hàng, nhà cung cấp, hoặc đối tác chuỗi cung ứng lớn nhất của doanh nghiệp đó lại đang gặp khủng hoảng thanh khoản.

PoC này áp dụng kiến trúc agentic workflow để xây dựng một tác nhân AI có khả năng:

- Phân tích quan hệ giao dịch để xác định các đối tác chuỗi cung ứng trọng yếu.
- Tự động kích hoạt công cụ tìm kiếm (DuckDuckGo) để thu thập tin tức thị trường theo thời gian thực về các đối tác này.
- Đánh giá rủi ro lây truyền bằng Google Gemini (2.5 Flash) và đưa ra khuyến nghị tín dụng dựa trên dữ liệu.
- Tạm dừng quy trình để chờ con người phê duyệt trước khi có quyết định tín dụng cuối cùng.

---

## 2. Business Problem / Bài Toán Nghiệp Vụ

In invoice financing, the repayment source depends heavily on the buyer's ability to pay the invoice on time. If the buyer experiences a liquidity shock, supplier payment delays, legal disputes, or bond default risk, the borrower may face a chain-default event even if its own historical financials look acceptable.

The goal of this PoC is to help credit officers detect supply chain contagion risk before it appears in financial statements.

---

## 3. Demo Scenario: The Contagion Use Case

EcoCarton Packaging, the Seller, applies for invoice financing using a 2 billion VND receivable from GreenSupermarket, the Buyer. The invoice has a 90-day deferred payment term and is supported by the Buyer's payment commitment.

The internal transaction database shows that 85% of EcoCarton's historical cash flow depends on this buyer. The agent then searches for recent market news about the counterparty and discovers negative signals such as liquidity stress, supplier payment delays, or legal disputes.

Based on the internal dependency concentration and external market signals, the agent raises a Red Alert and recommends rejection or manual escalation, even if the Seller's own profile appears acceptable.

---

## 4. Scope And Data

### Internal Data: Synthetic

A local SQLite database simulates core banking and transaction data:
- SME Sellers & Anchor Buyers
- Factoring invoices & Historical transaction logs

### External Data: Real-Time (Zero-Cost Setup)
- **Search Engine:** DuckDuckGo (Free, no API Key required) via `lxml`.
- **LLM Engine:** Google Gemini 2.5 Flash (High speed, strong reasoning).

---

## 5. System Architecture

The system is orchestrated with LangGraph. The workflow is modeled as a state graph where each node performs a specific task and routing logic determines the next step.

| Component | Purpose |
|---|---|
| `AgentState` | Shared state object passed between LangGraph nodes |
| `Data_Extractor` | Retrieves data from SQLite |
| `Dependency_Analyzer` | Calculates counterparty concentration and dependency ratio |
| `Market_Researcher` | Searches real-time market news (DuckDuckGo) |
| `Risk_Evaluator` | Synthesizes data into a risk level (Powered by Gemini) |
| `Human_in_the_Loop` | Pauses the workflow for Credit Officer approval |
| `SqliteSaver` | Persists workflow state by `thread_id` so interrupted flows can resume |

---

## 6. Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate

```

Install the required dependencies (Optimized for Google GenAI & DuckDuckGo):

```bash
pip install -U langgraph langchain-google-genai langchain-community langgraph-checkpoint-sqlite python-dotenv pandas duckduckgo-search lxml requests pydantic

```

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key

```

---

## 7. Execution & Actual Output

Run the Agent from the terminal:

```bash
python -m src.main FACT-2026-001

```

**Actual Terminal Output (High-Risk Contagion Scenario):**

```text
STARTING RISK ASSESSMENT FOR: FACT-2026-001
Completed Node: data_extractor
Completed Node: dependency_analyzer
Completed Node: market_researcher
--- NODE 6: AI RISK EVALUATOR (POWERED BY GEMINI) ---
Calling Gemini to evaluate contextual risk...
Completed Node: risk_evaluator
Completed Node: __interrupt__

============================================================
SYSTEM PAUSED: MANUAL CREDIT REVIEW REQUIRED
============================================================
Borrower:      EcoCarton Packaging
Counterparty:  GreenSupermarket
AI Risk Level: HIGH
Reasoning:     The Borrower, EcoCarton Packaging, exhibits an extremely high cash flow dependency ratio of 85% on its Counterparty, GreenSupermarket. This level of concentration (well above the 70% threshold for high concentration risk) makes EcoCarton Packaging exceptionally vulnerable to any financial distress or operational issues GreenSupermarket might encounter. Given this extreme structural vulnerability, the contagion credit risk is assessed as HIGH.
AI Suggests:   ESCALATE_FOR_MANUAL_REVIEW
------------------------------------------------------------

Action Required - APPROVE or REJECT? (Y/N): n

Updating state with decision: REJECTED_BY_HUMAN...
Resuming workflow...
--- NODE: HUMAN REVIEW ---
Completed Node: human_review

WORKFLOW COMPLETED. FINAL REPORT:
{
    "application_id": "FACT-2026-001",
    "seller_name": "EcoCarton Packaging",
    "dependency_ratio": 0.85,
    "ai_risk_level": "HIGH",
    "human_decision": "REJECTED_BY_HUMAN"
}

```

---

## 8. Business Value

This PoC demonstrates a shift from static credit analysis to dynamic, event-driven risk monitoring. It helps financial institutions reduce underwriting time, identify real-time market risks before they appear on balance sheets, and maintain governance by keeping final decision authority in human hands.

```

### Điểm nhấn quan trọng trong bản cập nhật này:
1. **Tech Stack đã được điều chỉnh:** Tôi đã thay toàn bộ references từ OpenAI/Tavily sang **Google Gemini 2.5 Flash** và **DuckDuckGo**, đi kèm với câu lệnh `pip install` chính xác nhất.
2. **Real Output:** Tôi đã copy đoạn log terminal chân thực nhất của bạn nhét vào phần 7. Việc show ra được quá trình Graph ngắt luồng (`__interrupt__`), lý luận sắc bén của AI, và quyết định Reject của con người là bảo chứng tuyệt đối cho độ hoàn thiện của hệ thống khi ai đó đọc GitHub của bạn.

```
