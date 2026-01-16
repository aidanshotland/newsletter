import sqlite3
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "articles.db")
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_articles():
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: {DB_PATH} not found!")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # FILTER: Only articles created today
    # FREQUENCY: Only counting other articles from today to find "Trending" topics
    query = """
    SELECT a.*, 
           (SELECT COUNT(*) FROM articles b 
            WHERE b.title LIKE '%' || SUBSTR(a.title, 1, 15) || '%' 
            AND date(b.created_at) = date('now')) as frequency
    FROM articles a 
    WHERE date(a.created_at) = date('now')
    ORDER BY frequency DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_newsletter(articles):
    if not articles:
        return "No new articles found."

    total_count = len(articles)
    unique_sources = len(set([a['source'] for a in articles]))

    context = "\n".join([
        f"ID: {a['id']} | Freq: {a['frequency']} | Source: {a['source']}\nTitle: {a['title']}\nLink: {a['link']}\nSummary: {a['summary']}\n---" 
        for a in articles
    ])

    # Reverting to your preferred high-density editor instruction
    config = types.GenerateContentConfig(
        system_instruction="""You are a Technical Strategist and Lead Editor. Mission: Synthesize raw tech news into a high-density 5-minute briefing (600-900 words). 

         PRIORITY MATRIX (Selection Criteria): 
    1. 🚨 TOP TRENDS: Include if: Freq >= 2 OR it's a major release from 'Anchor' projects (Meta, OpenAI, Python, Rust, Linux, etc.) OR it's a critical 'Breaking' security vulnerability. 
    2. 🤖 AI INNOVATION: Focus on autonomous agents, local-first LLM execution, inference speed breakthroughs, and agentic frameworks. 
    3. 🛡️ DEV & SECURITY: Focus on tools solving developer pain points, performance benchmarks (Rust/Mojo), and research into new attack surfaces. 
    4. REJECT: Marketing fluff, funding news, opinion pieces without code/data, and generic "Top 10" lists. 

    OUTPUT CONSTRAINTS: 
    - 11-13 items total. 
    - Each item must start with the article title as a ### heading (e.g., ### Article Title Here)
    - 60-80 words per item (3 tight sentences). 
    - Sentence 1: The Fact (What happened?). 
    - Sentence 2: The Technical Detail (How does it work/Key spec?). 
    - Sentence 3: The Actionable Insight (Why should a dev care today?).
    - SOURCING: Every item MUST end with a Markdown link using the exact URL provided: [Read the source](URL).

        STRUCTURE: 
        ## 🚨 TOP TRENDS 
        (3-5 items based on Matrix Rule 1) 

        ## 🤖 AI INNOVATION 
        (4-6 items based on Matrix Rule 2) 

        ## 🛡️ DEV & SECURITY 
        (3-5 items based on Matrix Rule 3)""", 
        # Enabling adaptive thinking with your requested budget
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=2048) 
    )

    prompt = f""" 
    Analyze these {total_count} items. Using the Priority Matrix, select the 12 most consequential stories.  
    Ensure the 'TOP TRENDS' section prioritizes high-frequency items but doesn't ignore major 'Anchor' releases. 
      
    ARTICLES: 
    {context} 

    Final Instruction: End the report with exactly this text: 
    'Generated from {total_count} articles across {unique_sources} sources.'
    """

    print(f"🧠 Gemini is analyzing {total_count} articles...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt,
        config=config
    )
    
    return response.text

if __name__ == "__main__":
    raw_data = get_articles()
    if raw_data:
        report = generate_newsletter(raw_data)
        print("\n" + "="*30 + "\nDAILY NEWSLETTER\n" + "="*30)
        print(report)

        newsletters_dir = os.path.join(BASE_DIR, 'newsletters')
        os.makedirs(newsletters_dir, exist_ok=True)

        today = datetime.now().strftime('%B-%d-%Y') 
        report_path = os.path.join(newsletters_dir, f"{today}.md")
        
        with open(report_path, "w") as f:
            f.write(report)
        
        print(f"\n✅ Newsletter saved to: {report_path}")
    else:
        print("Nothing new to report!")