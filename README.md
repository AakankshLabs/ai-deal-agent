# AI Deal Discovery & Marketing Agent

A Streamlit prototype from **AakankshLabs** that demonstrates how a shopper's product interest, audience type, and budget can be used to surface relevant offers and generate supporting marketing copy.

> **Project status:** Prototype  
> **Current implementation:** Rule-based product matching and template-based marketing content. It does not yet connect to live marketplaces, external product feeds, or a generative AI model.

## What it demonstrates

- **Audience selection:** Choose a student, gamer, or general shopper persona.
- **Budget filtering:** Set a spending limit and filter the sample catalogue.
- **Keyword matching:** Match a product query against product categories.
- **Deal presentation:** Show listed price, reference price, discount percentage, and estimated savings.
- **Marketing copy:** Generate draft Instagram, push-notification, email, and SEO snippets from the selected offer.
- **Basic marketing insight:** Display the selected audience segment alongside the recommendation.

## Tech stack

- Python
- Streamlit

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/AakankshLabs/ai-deal-agent.git
   cd ai-deal-agent
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Current limitations

- Uses a small sample product catalogue embedded in `app.py`.
- Matching is based on simple keyword checks, not semantic search.
- Prices, discounts, sellers, and images are sample data and should not be treated as live offers.
- Marketing copy is generated from templates rather than an LLM.
- No user accounts, persistent preferences, checkout, or live retailer integrations are included in this prototype.

## Roadmap

- [ ] Move the sample catalogue into a structured data source.
- [ ] Add robust text normalization and category-based matching.
- [ ] Add product-feed integrations and offer freshness checks.
- [ ] Introduce explainable ranking using relevance, price, and user preferences.
- [ ] Add an optional LLM-powered copy assistant with human review.
- [ ] Add tests, logging, and deployment documentation.

## About AakankshLabs

AakankshLabs explores practical software and AI-enabled product experiences. This project is an early prototype in deal discovery, personalization, and marketing automation.

---

*Built as an experimental portfolio project. Verify merchant, availability, and pricing details independently before making a purchase.*
