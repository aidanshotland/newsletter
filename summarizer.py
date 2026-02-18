import sqlite3
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime
from email.mime.multipart import MIMEMultipart # Added this
from email.mime.text import MIMEText          # Added this
from dotenv import load_dotenv
import markdown
import smtplib

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
            AND b.is_read = 0) as frequency
    FROM articles a 
    WHERE a.is_read = 0
    ORDER BY frequency DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_as_read(article_ids):
    """Updates the database to set is_read = 1 for the processed articles."""
    if not article_ids:
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Using 'IN' to update multiple IDs at once
    placeholders = ', '.join(['?'] * len(article_ids))
    query = f"UPDATE articles SET is_read = 1 WHERE id IN ({placeholders})"
    cursor.execute(query, article_ids)
    conn.commit()
    conn.close()
    print(f"✅ Success: {len(article_ids)} articles marked as read.")


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
        system_instruction="""You are a Technical Strategist and Lead Editor. Mission: Synthesize raw tech news into a high-density 5-minute briefing. 

    PRIORITY MATRIX (Selection Criteria): 
    1. RELEVANCE: Prioritize major releases from 'Anchor' projects (Meta, OpenAI, Python, Rust, Linux, etc.), critical security vulnerabilities, or items appearing with high frequency (>= 2). 
    2. TECHNICAL FOCUS: Cover the systems and infrastructure powering the AI race, the agent and model shifts redefining how software gets built, and the security threats that emerge when development moves this fast.
    3. REJECT: Marketing fluff, funding news, opinion pieces without code/data, and generic "Top 10" lists. 

    OUTPUT CONSTRAINTS: 
    - Exactly 10 items total in a single flat list (no category headings or intro summaries). 
    - Each item must start with a relevant emoji followed by the article title as a ### heading (e.g., ### [emoji] Article Title Here). 
    - 60-80 words per item (exactly 3 sentences). 
    - Sentence 1: The Fact (What happened?). 
    - Sentence 2: The Technical Detail (The explanation of how it works or its key specification). 
    - Sentence 3: Extended Context (Further information to round out the technical explanation or broader implications). 
    - SOURCING: Every item MUST end with a Markdown link: [Source: SourceName](URL).""", 
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=2048) 
    )

    prompt = f""" 
    Analyze these {total_count} items and select the 10 most consequential stories based on the Priority Matrix. 
    Provide a direct list of 10 items. Ensure the emoji is placed BEFORE the title in the heading.
      
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

def delete_old_articles():
    if not os.path.exists(DB_PATH):
        print("❌ Database not found. Nothing to delete.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # SQLite uses 'now' and '-3 days' to calculate the cutoff
        query = "DELETE FROM articles WHERE created_at < DATETIME('now', '-3 days')"
        cursor.execute(query)
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        if deleted_count > 0:
            print(f"🧹 Cleanup complete: {deleted_count} articles older than 3 days deleted.")
        else:
            print("✨ Database is already lean! No articles older than 3 days found.")
            
    except sqlite3.Error as e:
        print(f"❌ An error occurred: {e}")
    finally:
        conn.close()


def send_email(markdown_content):
    sender_email = os.getenv("EMAIL_ADDRESS")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    today = datetime.now().strftime('%B %d, %Y')

    # Convert the Markdown string into HTML
    html_body = markdown.markdown(markdown_content)

    # Wrap in basic styling to prevent "blob" text and improve readability
  # Wrap in styling with larger font and Dark Mode support
    styled_html = f"""
    <html>
      <head>
        <meta name="color-scheme" content="light dark">
        <meta name="supported-color-schemes" content="light dark">
        <style>
          :root {{
            color-scheme: light dark;
            supported-color-schemes: light dark;
          }}

          /* Dark Mode specific overrides */
          @media (prefers-color-scheme: dark) {{
            body {{
              background-color: #121212 !important;
              color: #eeeeee !important;
            }}
            h1, h2, h3 {{
              color: #ffffff !important;
            }}
            p, li {{
              color: #cccccc !important;
            }}
          }}

          /* General spacing for readability */
          h1, h2, h3 {{ margin-top: 24px; }}
          p, li {{ margin-bottom: 16px; }}
        </style>
      </head>
      <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                   line-height: 1.6; color: #333; background-color: #ffffff;
                   max-width: 600px; margin: auto; padding: 20px; 
                   font-size: 19px;">
        {html_body}
      </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = f"Tech Briefing <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = f"🚀 Tech Briefing: {today}"
    message.attach(MIMEText(styled_html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("📧 Email sent via Gmail (Clean links!)")
    except Exception as e:
        print(f"❌ Gmail Error: {e}")

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
        
        send_email(report)
        
        print(f"\n✅ Newsletter saved to: {report_path}")
        article_ids = [a['id'] for a in raw_data]
        mark_as_read(article_ids)
        delete_old_articles()

    else:
        print("Nothing new to report!")