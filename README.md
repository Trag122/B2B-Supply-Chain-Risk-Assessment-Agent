# PoC: B2B Supply Chain Risk Assessment Agent

**An Autonomous AI Agent for SME Supply Chain Credit Risk Assessment**

## Project Overview

In traditional B2B credit approval processes, financial institutions typically evaluate risk based on static, historical financial statements. This creates a significant "blind spot": an SME could face a chain default if its largest supply chain partner encounters a sudden crisis.

This **Proof of Concept (PoC)** applies an **Agentic Workflow** architecture to build an autonomous AI Agent designed to:

1. Analyze the Transaction Graph to identify heavily dependent supply chain partners.
2. Proactively trigger search tools to retrieve real-time market news and sentiment regarding those partners.
3. Evaluate contagion risk and recommend a data-driven credit decision.

## Scope & Synthetic Data

This project is developed within a Sandbox environment, blending simulated operational data with real-world market intelligence:

* **Internal Data (Synthetic):** A simulated Core Banking SQLite database containing historical transaction logs, establishing relationships like "Company A (Borrower) frequently transacts with Company B (Key Supplier/Buyer)".
* **External Data (Real-time):** Utilizing Search APIs to fetch actual, real-time internet news regarding "Company B" (e.g., reports of unpaid wages, bond defaults, or legal disputes).

## System Architecture

The system is orchestrated using **LangGraph** to strictly govern the reasoning flow (State Graph), ensuring deterministic and reliable AI behavior suited for financial operations.

* **Memory (State):** Context is managed via `SqliteSaver` (Persistence) and isolated by `thread_id` to handle individual credit review sessions seamlessly.
* **Nodes (Execution Units):**
* `Data_Extractor`: Retrieves internal transaction data from the database.
* `Market_Researcher`: Triggers the Search Tool to gather external news about identified partners.
* `Risk_Evaluator`: Synthesizes data to assess the level of contagion risk.
* `Human_in_the_Loop`: An interrupt mechanism that pauses the system, awaiting final Approve/Reject authorization from a human Credit Officer.


* **Edges (Routing):** Conditional branching based on logic (e.g., If market news is safe -> Proceed to standard credit scoring. If negative news is detected -> Trigger immediate high-risk alert).

## Tech Stack

* **Orchestration:** LangGraph
* **Core Model (LLM):** OpenAI (GPT-4o / GPT-3.5)
* **Search Tools:** Tavily Search API / DuckDuckGo
* **Database:** SQLite (Local Sandbox)
* **Language:** Python

## Project Roadmap

*Tracking the development lifecycle of the PoC.*

| Step | Action Item | Expected Result |
| --- | --- | --- |
| **1** | **Setup project & virtual environment** | Clean Python project running successfully in VS Code. |
| **2** | **Create SQLite synthetic database** | Database populated with tables for borrower, counterparty, invoices, and transactions. |
| **3** | **Develop Data_Extractor** | System successfully retrieves EcoCarton's transactions from the database. |
| **4** | **Develop Dependency_Analyzer** | Calculate and output dependency metrics (e.g., "85% of cash flow relies on GreenSupermarket"). |
| **5** | **Integrate Tavily or DuckDuckGo** | Agent autonomously searches for real-time news regarding the counterparty. |
| **6** | **Develop Risk_Evaluator** | The LLM evaluates data and returns a specific risk level: LOW, MEDIUM, or HIGH. |
| **7** | **Implement persistence with SQLite** | Workflow state is saved and can be resumed seamlessly using `thread_id`.

 |
| **8** | **Add Human-in-the-loop** | Workflow pauses at critical points, waiting for the Credit Officer to explicitly approve/reject.

 |
| **9** | **Execute 2 demo cases** | Successfully run one safe scenario and one high-risk scenario. |
| **10** | **Export JSON/Markdown report** | Final structured report generated for PoC presentation. |


## Business Value (Product Perspective)

This PoC demonstrates the paradigm shift from "static data analysis" to "dynamic, automated decision-making workflows." Applying Agentic Workflows to B2B lending allows financial institutions to drastically reduce underwriting time, detect real-time market risks before they appear on balance sheets, and ensure compliance by keeping the final decision authority in human hands (Human-in-the-Loop).

# Business Scenario: The "Contagion" Use Case
To demonstrate the system's capabilities, this PoC follows a highly realistic Invoice Financing (Factoring) scenario:

* The Business Context: EcoCarton Packaging (Company A - Synthetic Data) recently delivered 100,000 carton boxes to a major retail supermarket, GreenSupermarket (Company B - Real Data). Company B accepted the goods and signed a VAT Invoice with a 90-day deferred payment term.

* The Problem: Facing an immediate cash flow shortage to cover factory payroll and raw materials, EcoCarton brings this 2 billion VND invoice to the bank to apply for a short-term loan. This financial operation is known as Accounts Receivable Factoring.

* The Workflow:

 1. The Credit Officer inputs EcoCarton's factoring application into the system.
 2. The Data_Extractor node scans the mock Core Banking database and discovers a critical dependency: 85% of EcoCarton's historical cash flow, along with the current 2 billion VND collateral, entirely depends on Company B's ability to pay in 90 days.
 3. The Market_Researcher node automatically triggers a Tavily search query: "Company B financial health, bankruptcy, bond default news".
 4. The Risk_Evaluator node processes recent news articles revealing that Company B is facing a severe liquidity crisis and delaying payments to suppliers.
 5. The system triggers a Human_in_the_Loop interrupt, presenting the Credit Officer with a Red Alert summary, recommending a rejection of the loan to prevent cross-default risk (since Company B is highly unlikely to pay the invoice in 90 days).
---

*Status: Work in Progress. The project may change overtime*
