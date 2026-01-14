from google import genai
import os
from dotenv import load_dotenv
from fetch_articles import fetch_recent_articles
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def summarize_with_gemini(articles):
    """Use Gemini AI to summarize and categorize articles into a newsletter."""
    
    # Initialize Gemini client
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Prepare the articles data for Gemini
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"\n{i}. [{article['source']}] {article['title']}\n"
        articles_text += f"   Link: {article['link']}\n"
        articles_text += f"   Published: {article['published']}\n"
        articles_text += f"   Summary: {article['summary']}\n"
    
    # Create the prompt for Gemini
    prompt = f"""You are creating a daily tech newsletter. Below are {len(articles)} articles from various tech sources from the last 24 hours.

Please create a concise, engaging newsletter with the following structure:

1. **Top Stories** (3-5 most important/impactful stories)
2. **AI & Machine Learning** (if relevant articles exist)
3. **Developer Tools & GitHub** (if relevant)
4. **Security & Cloud** (if relevant)
5. **Other Notable News** (remaining interesting articles)

For each article in each section:
- Write a 2-3 sentence summary explaining what happened and why it matters
- Include the article title as a text (not a link)
- Include the link on a separate line
- Make the summary informative enough that I don't need to click through unless I want more details

Skip any sections that don't have relevant articles. Keep the total newsletter to about 5 minutes of reading time.

Here are the articles:
{articles_text}

Format the output in clean, readable markdown suitable for an email."""

    # Call Gemini API (using stable free tier model)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text


def generate_newsletter():
    """Main function to fetch articles and generate newsletter."""
    print("=" * 80)
    print(f"Generating Daily Tech Newsletter - {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 80)
    
    # Fetch articles
    print("\n📰 Fetching articles from the last 24 hours...")
    articles = fetch_recent_articles(hours=24)
    print(f"✓ Found {len(articles)} articles")
    
    # Generate summary with Gemini
    print("\n🤖 Generating AI summary with Gemini...")
    newsletter = summarize_with_gemini(articles)
    
    print("\n" + "=" * 80)
    print("NEWSLETTER PREVIEW")
    print("=" * 80 + "\n")
    print(newsletter)
    
    # Optionally save to file
    filename = f"newsletter_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w') as f:
        f.write(f"# Daily Tech Newsletter - {datetime.now().strftime('%B %d, %Y')}\n\n")
        f.write(newsletter)
    
    print(f"\n✓ Newsletter saved to {filename}")
    
    return newsletter


if __name__ == "__main__":
    # Make sure GOOGLE_API_KEY is set in your environment
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: Please set GOOGLE_API_KEY environment variable")
        print("Get your free API key at: https://aistudio.google.com/apikey")
        print("Then export it like: export GOOGLE_API_KEY='your-key-here'")
    else:
        generate_newsletter()