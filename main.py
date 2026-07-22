import os
import sys
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Trick to automatically run the browser-based app without manually typing 'streamlit run main.py' in the terminal
if __name__ == "__main__" and not os.environ.get("STREAMLIT_RUN_GUARD"):
    os.environ["STREAMLIT_RUN_GUARD"] = "true"
    sys.argv = ["streamlit", "run", sys.argv[0]]
    from streamlit.web.cli import main

    sys.exit(main())

# Web page configuration
st.set_page_config(
    page_title="GitHub Advanced AI Evaluator",
    page_icon="🚀",
    layout="wide"
)

# Sidebar - AI Configuration
st.sidebar.title("⚙️ AI Engine Settings")
ai_provider = st.sidebar.radio("Select AI Provider", ["Gemini (Google AI Studio)", "Ollama (Local)"])

# Language selection feature for Gemini API output (Preset + Custom Input)
language_option = st.sidebar.selectbox(
    "Output Language Preset",
    ["English", "French", "Japanese", "Korean", "Custom Input"],
    index=0,
    help="Select a preset language or choose 'Custom Input' to specify your own."
)

if language_option == "Custom Input":
    target_language = st.sidebar.text_input("Enter Custom Output Language", value="Spanish",
                                            help="Type any language you want the AI to output.")
else:
    target_language = language_option

if ai_provider == "Gemini (Google AI Studio)":
    google_api_key = st.sidebar.text_input("Gemini API Key", type="password",
                                           help="Enter your Google AI Studio API key")
    model_name = st.sidebar.selectbox("Gemini Model",
                                      ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"])
else:
    ollama_model = st.sidebar.text_input("Ollama Model Name", value="llama3")
    ollama_url = st.sidebar.text_input("Ollama API URL", value="http://localhost:11434/api/generate")


def get_public_repositories(username: str):
    """Retrieve public repository list of the user via GitHub API"""
    api_url = f"https://api.github.com/users/{username}/repos?per_page=15&sort=updated"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(api_url, headers=headers)
        if res.status_code == 200:
            repos = res.json()
            return [repo["name"] for repo in repos if not repo["fork"]]  # Exclude forked repositories
    except Exception:
        pass
    return []


def get_repo_readme(username: str, repo_name: str):
    """Fetch README.md content for a specific repository using GitHub API Raw URL"""
    raw_urls = [
        f"https://raw.githubusercontent.com/{username}/{repo_name}/main/README.md",
        f"https://raw.githubusercontent.com/{username}/{repo_name}/master/README.md"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in raw_urls:
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                return res.text[:2500]  # Truncate if too long to prevent token overflow
        except Exception:
            continue
    return "No README found."


def crawl_github_comprehensive(username: str):
    """Comprehensively gather profile info, profile README, and individual repository READMEs"""
    print(f"[+] Comprehensive crawling for: {username}...")
    profile_url = f"https://github.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(profile_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract Bio
    bio_elem = soup.find("div", {"data-bio-text": True})
    bio = bio_elem.text.strip() if bio_elem else "No bio provided."

    # Extract Profile README
    profile_readme = ""
    readme_elem = soup.find("article", class_="markdown-body")
    if readme_elem:
        profile_readme = readme_elem.get_text(separator="\n", strip=True)

    # Fetch public repositories and crawl their READMEs
    repo_names = get_public_repositories(username)
    repos_data = {}

    for rname in repo_names[:6]:  # Analyze up to 6 core repositories
        r_readme = get_repo_readme(username, rname)
        repos_data[rname] = r_readme

    return {
        "bio": bio,
        "profile_readme": profile_readme,
        "repos": repos_data
    }


def analyze_with_ai(data: dict):
    # Assemble comprehensive data into structured prompt format
    repos_text = ""
    for rname, rcontent in data["repos"].items():
        repos_text += f"\n--- Repository: {rname} ---\n{rcontent}\n"

    prompt = f"""
You are an elite Tech Lead, Senior Engineering Director, and Executive Product Strategist. Analyze the following comprehensive GitHub profile and repository data with uncompromising depth.

[Target Data]
- Bio: {data['bio']}
- Profile README: {data['profile_readme']}
- Individual Repositories & READMEs: {repos_text}

CRITICAL INSTRUCTION: You MUST write the entire response in **{target_language}**. 

You MUST follow this strict layout and formatting. Do not skip any section. Use polite, highly polished, sophisticated, and professional language suitable for high-end executive review and direct LinkedIn publication.

### 1. Product Manager (PM) Perspective
- **Product Vision & Market Fit**: Evaluate how the projects address real-world needs, user friction, and business/portfolio value.
- **Strengths**: Explicitly detail the core product strengths.
- **Areas for Improvement**: Constructively highlight strategic considerations or potential scope optimizations.

### 2. Developer Perspective
- **Architectural Rigor & Stack Selection**: Evaluate technical depth, stack choices, engineering discipline, and structural maturity.
- **Strengths**: Explicitly detail technical achievements, code architecture insights, and security/efficiency standards.
- **Areas for Improvement**: Constructively point out potential technical enhancements or optimization vectors.

### 3. Repository-by-Repository Evaluation
Provide a structured breakdown for the core repositories found in the data, using this exact format for each:
- **[Repository Name]**
  - **Core Value & Role**: What does it solve?
  - **Technical Merit & Stack**: How is it built?
  - **Verdict (Pros & Cons)**: Professional verdict detailing strong points and constructive recommendations.

### 4. LinkedIn Post Draft
- Write a short, powerful, highly engaging summary paragraph optimized for a professional networking post, highlighting technical grit, architectural discipline, and product mindset. Conclude with powerful tech hashtags.
"""

    if ai_provider == "Gemini (Google AI Studio)":
        if not google_api_key:
            return "ERROR: Gemini API Key is missing. Please check the sidebar."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={google_api_key}"
        headers = {"Content-Type": "application/json"}
        data_payload = {"contents": [{"parts": [{"text": prompt}]}]}

        res = requests.post(url, headers=headers, json=data_payload)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Gemini API Error: {res.text}"

    elif ai_provider == "Ollama (Local)":
        payload = {
            "model": ollama_model,
            "prompt": prompt,
            "stream": False
        }
        try:
            res = requests.post(ollama_url, json=payload)
            if res.status_code == 200:
                return res.json().get("response", "")
            else:
                return f"Ollama Error: {res.text}"
        except Exception as e:
            return f"Ollama Connection Error: {str(e)}"


# Main Screen UI
st.title("🚀 Comprehensive GitHub & Repository AI Auditor")
st.write(
    "Crawl GitHub profiles and **core repository README files** comprehensively to generate PM/Developer evaluations (strengths & improvements) and a LinkedIn-ready post draft.")

col1, col2 = st.columns([3, 1])

with col1:
    github_input = st.text_input("GitHub Username or Profile Link",
                                 placeholder="e.g., ulsidae or https://github.com/ulsidae")

with col2:
    st.write(" ")
    st.write(" ")
    analyze_btn = st.button("🔥 Run Deep Audit", use_container_width=True)

if analyze_btn:
    if not github_input:
        st.warning("Please enter a GitHub username or link.")
    else:
        target_username = github_input.rstrip("/").split("/")[
            -1] if "github.com/" in github_input else github_input.strip()

        with st.spinner(f"Scraping profile and repositories for '{target_username}'... (This may take a few seconds)"):
            crawled_data = crawl_github_comprehensive(target_username)

            if crawled_data and (crawled_data["profile_readme"] or crawled_data["repos"]):
                st.success("Crawling complete! Running multi-perspective AI evaluation...")
                result = analyze_with_ai(crawled_data)

                st.markdown("---")
                st.subheader("📊 Executive Audit Report")

                if "ERROR" in result or "Error" in result:
                    st.error(result)
                else:
                    st.markdown(result)
            else:
                st.error("Failed to retrieve profile or repositories. Check the username.")
