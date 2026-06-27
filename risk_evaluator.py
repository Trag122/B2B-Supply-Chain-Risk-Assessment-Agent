from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from src.state import AgentState

# 1. Enforce strict output schema
class RiskAssessmentOutput(BaseModel):
    market_sentiment: Literal["NEGATIVE", "WATCHLIST", "STABLE", "POSITIVE"] = Field(
        description="Analyze the true sentiment of the news. If the news is a correction, denial of rumors, or indicates safety, select STABLE/POSITIVE."
    )
    risk_level: Literal["HIGH", "MEDIUM", "LOW"] = Field(
        description="The contagion credit risk level."
    )
    risk_reasoning: str = Field(
        description="Detailed reasoning: Explain why this risk level was chosen based on the news context and the dependency ratio."
    )
    recommendation: Literal["REJECT_OR_ESCALATE", "ESCALATE_FOR_MANUAL_REVIEW", "PROCEED_TO_STANDARD_CREDIT_SCORING"] = Field(
        description="Actionable recommendation for the Credit Officer."
    )

def risk_evaluator(state: AgentState) -> dict:
    print("--- NODE 6: AI RISK EVALUATOR (POWERED BY GEMINI) ---")
    
    # ✅ Sửa lại thành tên model mới (Gemini 2.5 Flash):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    structured_llm = llm.with_structured_output(RiskAssessmentOutput)
    
    # 2. Process input data for the LLM
    dependency_ratio = state.get("dependency_ratio", 0)
    dependency_pct = f"{dependency_ratio:.0%}"
    
    market_news = state.get("market_news", [])
    if market_news:
        news_text = "\n".join([f"- {article.get('title')}: {article.get('content')}" for article in market_news])
    else:
        news_text = "No notable market news available."

    # 3. Define the Expert Persona Prompt
    prompt = PromptTemplate(
        template="""You are a Senior B2B Credit Risk Underwriter.
        Your task is to evaluate the contagion risk of an Accounts Receivable Factoring application based on the Borrower's dependency on their Counterparty (Buyer).
        
        SYSTEM INFORMATION:
        - Borrower (Seller): {seller_name}
        - Counterparty (Buyer): {buyer_name}
        - Cash Flow Dependency Ratio: {dependency_pct} (A ratio >50% is a concern, >70% indicates high concentration risk).
        
        MARKET NEWS REGARDING THE COUNTERPARTY:
        {news_text}
        
        ANALYSIS RULES:
        1. Read the news context CAREFULLY. If the media mentions "bankruptcy" or "debt" but it is a denial, a resolved issue, or a false rumor, the sentiment is NOT NEGATIVE.
        2. If the Counterparty is genuinely facing a liquidity crisis AND the Borrower is heavily dependent on them (>50%), the risk MUST be categorized as HIGH or MEDIUM.
        
        Reason carefully and return the structured assessment output.
        """,
        input_variables=["seller_name", "buyer_name", "dependency_pct", "news_text"]
    )
    
    final_prompt = prompt.format(
        seller_name=state.get("seller_name", "Unknown Seller"),
        buyer_name=state.get("buyer_name", "Unknown Buyer"),
        dependency_pct=dependency_pct,
        news_text=news_text
    )
    
    print("Calling Gemini to evaluate contextual risk...")
    
    # 4. Invoke LLM and retrieve structured output
    result = structured_llm.invoke(final_prompt)
    
    # 5. Update State
    return {
        "market_sentiment": result.market_sentiment,
        "risk_level": result.risk_level,
        "risk_reasoning": result.risk_reasoning,
        "recommendation": result.recommendation,
    }