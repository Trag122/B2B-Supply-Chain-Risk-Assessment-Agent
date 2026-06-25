# 🚀 PoC: B2B Supply Chain Risk Assessment Agent

**An Autonomous AI Agent for SME Supply Chain Credit Risk Assessment**

## 📖 Project Overview

In traditional B2B credit approval processes, financial institutions typically evaluate risk based on static, historical financial statements. This creates a significant "blind spot": an SME could face a chain default if its largest supply chain partner encounters a sudden crisis.

This **Proof of Concept (PoC)** applies an **Agentic Workflow** architecture to build an autonomous AI Agent designed to:

1. Analyze the Transaction Graph to identify heavily dependent supply chain partners.
2. Proactively trigger search tools to retrieve real-time market news and sentiment regarding those partners.
3. Evaluate contagion risk and recommend a data-driven credit decision.

## 🎯 Scope & Synthetic Data

This project is developed within a Sandbox environment, blending simulated operational data with real-world market intelligence:

* **Internal Data (Synthetic):** A simulated Core Banking SQLite database containing historical transaction logs, establishing relationships like "Company A (Borrower) frequently transacts with Company B (Key Supplier/Buyer)".
* **External Data (Real-time):** Utilizing Search APIs to fetch actual, real-time internet news regarding "Company B" (e.g., reports of unpaid wages, bond defaults, or legal disputes).

## 🧠 System Architecture

The system is orchestrated using **LangGraph** to strictly govern the reasoning flow (State Graph), ensuring deterministic and reliable AI behavior suited for financial operations.

* **Memory (State):** Context is managed via `SqliteSaver` (Persistence) and isolated by `thread_id` to handle individual credit review sessions seamlessly.
* **Nodes (Execution Units):**
* `Data_Extractor`: Retrieves internal transaction data from the database.
* `Market_Researcher`: Triggers the Search Tool to gather external news about identified partners.
* `Risk_Evaluator`: Synthesizes data to assess the level of contagion risk.
* `Human_in_the_Loop`: An interrupt mechanism that pauses the system, awaiting final Approve/Reject authorization from a human Credit Officer.


* **Edges (Routing):** Conditional branching based on logic (e.g., If market news is safe -> Proceed to standard credit scoring. If negative news is detected -> Trigger immediate high-risk alert).

## 🛠 Tech Stack

* **Orchestration:** LangGraph
* **Core Model (LLM):** OpenAI (GPT-4o / GPT-3.5)
* **Search Tools:** Tavily Search API / DuckDuckGo
* **Database:** SQLite (Local Sandbox)
* **Language:** Python

## 📈 Project Roadmap

*Tracking the development lifecycle of the PoC.*

* [x] **Phase 1: Ideation & System Design**
* Define the business case and pain points.
* Draft README to outline the PoC scope and architecture.


* [ ] **Phase 2: Synthetic Data Preparation**
* Build a mock SQLite database for SME transaction histories.
* Create company profiles (mapping synthetic borrowers to real-world companies currently facing market risks).


* [ ] **Phase 3: LangGraph Core Development**
* Define the `AgentState` and core `Nodes`.
* Integrate the external Search Tool (Tavily).
* Engineer specialized prompts for research and risk evaluation tasks.


* [ ] **Phase 4: Advanced Features (UX & Risk Management)**
* Implement memory persistence with SQLite.
* Build the `Human-in-the-Loop` interrupt mechanism for manual review.


* [ ] **Phase 5: Testing & Documentation**
* Run case studies (Safe Scenario vs. High-Risk Scenario).
* Extract the Agent's reasoning logs and visualize the execution graph.



## 💡 Business Value (Product Perspective)

This PoC demonstrates the paradigm shift from "static data analysis" to "dynamic, automated decision-making workflows." Applying Agentic Workflows to B2B lending allows financial institutions to drastically reduce underwriting time, detect real-time market risks before they appear on balance sheets, and ensure compliance by keeping the final decision authority in human hands (Human-in-the-Loop).

---

*Status: Work in Progress. The project may change overtime*
