import sqlite3
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. FIX PATHS: Ensure it always finds news.db in the script's folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "news.db")
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

# 2. Setup Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_articles():
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: {DB_PATH} not found!")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Using the Frequency logic to find common trends
    query = """
    SELECT a.*, 
           (SELECT COUNT(*) FROM articles b 
            WHERE b.title LIKE '%' || SUBSTR(a.title, 1, 20) || '%' 
            AND b.is_read = 0) as frequency
    FROM articles a 
    WHERE a.is_read = 0
    ORDER BY frequency DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_newsletter(articles):
    if not articles:
        return "No new articles found. Your database is up to date!"

    # Format data for Gemini, including the Frequency Score
    context = "\n".join([
        f"ID: {a['id']} | Freq: {a['frequency']} | Source: {a['source']} | Title: {a['title']}\nSummary: {a['summary']}\nLink: {a['link']}\n---" 
        for a in articles
    ])

    config = types.GenerateContentConfig(
        system_instruction="""You are a Technical Strategist and Lead Editor. Mission: Synthesize raw tech news into a high-density 5-minute briefing (600-900 words).

        PRIORITY MATRIX (Selection Criteria):
        1. 🚨 TOP TRENDS: Include if: Freq >= 2 OR it's a major release from 'Anchor' projects (Meta, OpenAI, Python, Rust, Linux, etc.) OR it's a critical 'Breaking' security vulnerability.
        2. 🤖 AI INNOVATION: Focus on autonomous agents, local-first LLM execution, inference speed breakthroughs, and agentic frameworks.
        3. 🛡️ DEV & SECURITY: Focus on tools solving developer pain points, performance benchmarks (Rust/Mojo), and research into new attack surfaces.
        4. REJECT: Marketing fluff, funding news, opinion pieces without code/data, and generic "Top 10" lists.

        OUTPUT CONSTRAINTS:
        - Exactly 12 items total.
        - 60-80 words per item (3 tight sentences).
        - Sentence 1: The Fact (What happened?).
        - Sentence 2: The Technical Detail (How does it work/Key spec?).
        - Sentence 3: The Actionable Insight (Why should a dev care today?).

        STRUCTURE:
        ## 🚨 TOP TRENDS
        (3-5 items based on Matrix Rule 1)

        ## 🤖 AI INNOVATION
        (4-6 items based on Matrix Rule 2)

        ## 🛡️ DEV & SECURITY
        (3-5 items based on Matrix Rule 3)

        End with: 'Generated from {N} articles across {M} sources.'""",
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=2048)
    )

    # Calculate meta-stats for the footer
    unique_sources = len(set([a['source'] for a in articles]))
    
    prompt = f"""
    Analyze these {len(articles)} items. 
    Using the Priority Matrix, select the 12 most consequential stories. 
    Ensure the 'TOP TRENDS' section prioritizes high-frequency (Freq >= 2) items but doesn't ignore major 'Anchor' releases.
    
    ARTICLES:
    {context}
    """

    print(f"🧠 Gemini is analyzing {len(articles)} articles through the Priority Matrix...")
    
    response = client.models.generate_content(
        model='gemini-2.0-flash', # Or your preferred 2026 model variant
        contents=prompt,
        config=config
    )
    
    return response.text

def mark_as_read():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE articles SET is_read = 1 WHERE is_read = 0")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    raw_data = get_articles()
    
    if raw_data:
        report = generate_newsletter(raw_data)
        print("\n" + "="*30 + "\nDAILY NEWSLETTER\n" + "="*30)
        print(report)
        
        with open(os.path.join(BASE_DIR, "report.md"), "w") as f:
            f.write(report)
        
        # Uncomment this once you are happy with the output!
        # mark_as_read()
    else:
        print("Nothing new to report!")