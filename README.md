# RepoLens

> **AI-powered GitHub portfolio analysis for developers, recruiters, and hiring managers.**

Analyze GitHub profiles by combining profile information and repository README files to generate executive-level reviews from both Product Manager and Software Developer perspectives.

🌐 **Live Demo**

https://repolens.streamlit.app/

---

| Section                         | Description                                                                  |
| :------------------------------ | :--------------------------------------------------------------------------- |
| [**✨ Features**](#0)               | Overview of RepoLens capabilities and supported AI providers.                |
| [**⚙️ How RepoLens Works**](#1)       | Learn how RepoLens crawls GitHub profiles and generates AI-powered reports.  |
| [**🚀 Using the Online Version**](#2) | Quick start guide for using the hosted Streamlit application.                |
| [**🔑 Google Gemini Setup**](#3)      | Step-by-step *guide* to obtaining a free Google AI Studio API key.             |
| [**🖥️ Ollama Support**](#4)          | Information for developers who prefer running RepoLens locally using Ollama. |
| [**🏗️ Code Architecture**](#5)       | Overview of the crawler, prompt builder, AI layer, and Streamlit interface.  |
| [**💻 Run Locally**](#6)              | Local installation and execution instructions.                               |
| [**🛠️ Technologies**](#7)            | Libraries, frameworks, and APIs used in the project.                         |
| [**📄 License**](#8)                  | Apache License 2.0 information.                                              |

---

<h2 id="0"> ✨ Features </h2>

* GitHub Profile Crawling
* Profile README Analysis
* Repository README Analysis
* Product Manager Perspective
* Developer Perspective
* Repository-by-Repository Evaluation
* LinkedIn Post Draft Generation
* Multi-language Output
* Gemini & Ollama Support

---

<h2 id="1"> ⚙️ How RepoLens Works </h2>

RepoLens automatically performs the following steps:

1. Receives a GitHub username or profile URL.
2. Crawls the user's public GitHub profile.
3. Extracts:

   * GitHub Bio
   * Profile README
   * Public repositories
4. Downloads README files from the user's most recently updated public repositories.
5. Builds a structured prompt from the collected information.
6. Sends the prompt to the selected AI model (Gemini or Ollama).
7. Generates a professional report including:

   * Product Manager evaluation
   * Developer evaluation
   * Repository-by-repository analysis
   * Strengths
   * Areas for improvement
   * A LinkedIn-ready post draft

> **Only publicly available GitHub information is analyzed.**

---

<h2 id="2"> 🚀 Using the Online Version </h2>

The easiest way to use RepoLens is through the hosted Streamlit application.

🌐 **Live Demo**

https://repolens.streamlit.app/

No installation is required.

Simply:

1. Open the website.
2. Select **Gemini (Google AI Studio)**.
3. Enter your Gemini API key.
4. Enter a GitHub username or profile URL.
5. Click **Run Deep Audit**.

---

<h2 id="3"> 🔑 Google Gemini Setup (Recommended) </h2>

The online demo uses **Google Gemini**.

For security reasons, **no API key is embedded in the application or source code**.

Instead, every user provides their own API key.

This prevents accidental exposure of API credentials while allowing users to maintain full control over their own API usage.

The good news is that **Google AI Studio provides a generous free API tier**, allowing most users to use RepoLens without any additional cost.

---

## Step 1 — Open Google AI Studio

<img src="https://github.com/ulsidae/RepoLens/blob/main/img/1.png" height="400"/>

Visit:

https://aistudio.google.com/

Sign in with your Google account.

---

## Step 2 — Create an API Key

<img src="https://github.com/ulsidae/RepoLens/blob/main/img/2.png" height="400"/>

Open the **API Keys** page:

https://aistudio.google.com/app/apikey

Click **Create API Key**.

If this is your first time using Google AI Studio, you may be asked to create or select a Google Cloud project before generating your API key.

---

## Step 3 — Copy Your API Key

<img src="https://github.com/ulsidae/RepoLens/blob/main/img/3.png" height="400"/>

After the key has been generated, copy it.

Keep your API key private.

---

## Step 4 — Paste It into RepoLens

<img src="https://github.com/ulsidae/RepoLens/blob/main/img/4.png" height="400"/>

Return to RepoLens.

In the left sidebar, paste your key into the following field:

```text
Gemini API Key
```

---

## Step 5 — Select a Gemini Model

Select one of the available Gemini models.

For example:

* gemini-3.5-flash
* gemini-3.1-flash-lite
* gemini-3.1-pro-preview

Then click **Run Deep Audit**.

<img src="https://github.com/ulsidae/RepoLens/blob/main/img/5.png" height="400"/>

---

## Free Tier

RepoLens is fully compatible with the **free Google AI Studio API tier**.

A paid Google Cloud account is **not required** for normal usage.

---

<h2 id="4"> 🖥️ Ollama Support </h2>

RepoLens also supports **Ollama**.

Unlike the hosted Streamlit demo, **Ollama support is primarily intended for developers who prefer running RepoLens entirely on their own machines.**

If you would rather perform AI inference locally without sending prompts to Google's servers:

1. Install Ollama.
2. Download your preferred language model (e.g. `llama3`).
3. Select **Ollama (Local)** in the sidebar.
4. Enter the model name.
5. Enter the Ollama API URL.

Example configuration:

**Model**

```text
llama3
```

**API URL**

```text
http://localhost:11434/api/generate
```

When using Ollama, all AI inference is performed locally.

No Google API key or external cloud service is required.

---

<h2 id="5"> 🏗️ Code Architecture </h2>

The application is organized into several logical components.

## GitHub Crawler

Responsible for collecting public GitHub information.

Main functions:

```python
crawl_github_comprehensive()

get_public_repositories()

get_repo_readme()
```

Responsibilities:

* Crawl GitHub profiles
* Read profile README files
* Retrieve public repositories
* Download repository README files

---

## Prompt Builder

After crawling, RepoLens combines the collected GitHub information into a structured prompt.

The prompt instructs the AI to generate:

* Product Manager Perspective
* Developer Perspective
* Repository-by-Repository Evaluation
* LinkedIn Post Draft

The output language is dynamically selected based on the user's preferences.

---

## AI Layer

RepoLens supports two AI backends.

### Google Gemini

Uses Google's official Gemini REST API.

```http
POST https://generativelanguage.googleapis.com/
```

Authentication is handled using the API key entered by the user.

---

### Ollama

Uses the local Ollama REST API.

```http
POST http://localhost:11434/api/generate
```

Once a local model has been installed, no cloud service or internet connection is required for AI inference.

---

## Streamlit Interface

The Streamlit frontend provides:

* AI Provider Selection
* Output Language Selection
* Gemini Model Selection
* GitHub Username Input
* Deep Audit Button
* Markdown Report Viewer

Additionally, the application includes a small startup helper that automatically launches Streamlit when `main.py` is executed directly, eliminating the need to manually run:

```bash
streamlit run main.py
```

each time.

---

<h2 id="6"> 💻 Run Locally </h2>

Clone the repository:

```bash
git clone https://github.com/ulsidae/RepoLens.git
cd RepoLens
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run main.py
```

Then open the local URL displayed in your terminal.

---

<h2 id="7"> Technologies </h2>

* Python
* Streamlit
* Requests
* BeautifulSoup4
* GitHub REST API
* Google Gemini API
* Ollama

---

<h2 id="8"> 📄 License </h2>

This project is licensed under the **Apache License 2.0**.

See the `LICENSE` file for details.
