# InvestIQ Deployment Guide

## GitHub Setup
1. Initialize git in the root folder `investiq/`:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Create a new repository on GitHub.
3. Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/investiq.git
   git push -u origin main
   ```

## Streamlit Cloud Deployment
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**.
3. Select your GitHub repository (`investiq`).
4. Set the Main file path to `app.py`.
5. Click **Deploy!**

Streamlit Cloud will automatically read your `requirements.txt` and install all necessary dependencies.
