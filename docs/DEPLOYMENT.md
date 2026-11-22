# Deploy the Streamlit prototype

This repository can be deployed to Streamlit Community Cloud. Deployment is a separate manual step; passing GitHub Actions tests does not publish the app.

## Before you deploy

- Confirm the repository is public or otherwise accessible to your Streamlit account.
- Confirm the default branch is `main`.
- Confirm `app.py`, `recommendations.py`, `requirements.txt`, and `data/products.json` are committed.
- This prototype uses synthetic sample products only. It does not require API keys or secrets.

## Deployment steps

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
2. Select **Create app**.
3. Choose repository: `AakankshLabs/ai-deal-agent`.
4. Choose branch: `main`.
5. Set the main file path to `app.py`.
6. Open **Advanced settings** only if you need to select a Python version. Use Python 3.11 to match the GitHub Actions workflow.
7. Select **Deploy** and wait for the build to finish.
8. Open the generated app URL and test at least:
   - a search such as `headphones`;
   - a low budget and a higher budget;
   - each persona;
   - the score breakdown expander;
   - relevant / not relevant feedback;
   - the session analytics CSV download.

## After deployment

- Add the hosted URL to the repository README and portfolio only after you have verified it works.
- Check the Streamlit app logs if startup fails.
- When code changes are pushed to `main`, Streamlit Community Cloud can rebuild the app.
- Do not add passwords, API keys, or personal data to the repository.

## Important product limitations

- Search analytics and feedback are stored only in the active Streamlit session. They are not persisted to a database or available as cross-user analytics.
- Product records, prices, discounts, and sellers are synthetic sample data.
- Recommendation ranking is deterministic and heuristic; it is not an LLM or trained model.
- The hand-labelled 30-query benchmark is a regression check, not a real-world recommendation quality study.
