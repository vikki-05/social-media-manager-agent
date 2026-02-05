import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SocialMediaAgent:
    def __init__(self, data_path: str):
        self.data = pd.read_csv(data_path)

    # -------------------------
    # STEP 1: Observe & Analyze
    # -------------------------
    def analyze_engagement(self):
        self.data["engagement"] = (
            self.data["likes"]
            + self.data["comments"]
            + self.data["shares"]
        )
        return self.data.groupby("content_type")["engagement"].mean()

    # -------------------------
    # STEP 2: Decide Strategy
    # -------------------------
    def decide_strategy(self):
        engagement_stats = self.analyze_engagement()

        best_content_type = engagement_stats.idxmax()
        best_score = engagement_stats.max()

        best_time = (
            self.data.groupby("posted_time")["likes"]
            .mean()
            .idxmax()
        )

        return best_content_type, best_score, best_time

    # -------------------------
    # STEP 3: Act (ScaleDown AI)
    # -------------------------
    def generate_post_with_ai(self, content_type, post_time):
        api_key = os.getenv("SCALEDOWN_API_KEY")

        if not api_key:
            raise ValueError("SCALEDOWN_API_KEY not found in .env file")

        url = "https://api.scaledown.xyz/compress/raw/"

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

        prompt = f"""
You are a professional social media manager.

Insights:
- Best content type: {content_type}
- Best posting time: {post_time}:00 hrs

Generate ONE short, engaging social media caption with hashtags.
"""

        payload = {
            "prompt": prompt,
            "max_tokens": 120
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        # -------- SAFE RESPONSE HANDLING --------
        if isinstance(data, dict):
            if "compressed_text" in data:
                return data["compressed_text"]

            if "output" in data:
                return data["output"]

            if "data" in data and isinstance(data["data"], dict):
                if "text" in data["data"]:
                    return data["data"]["text"]

            if "choices" in data:
                return data["choices"][0]["message"]["content"]

        # -------- FALLBACK (never crash) --------
        return (
            f"🔥 {content_type} content performs best! "
            f"Post around {post_time}:00 to maximize engagement. "
            f"#SocialMedia #AI #Growth"
        )

    # -------------------------
    # STEP 4: MEMORY (NEW FEATURE)
    # -------------------------
    def save_decision(self, content_type, post_time, score, caption):
        os.makedirs("memory", exist_ok=True)

        with open("memory/decision_log.txt", "a", encoding="utf-8") as f:
            f.write("----- AGENT DECISION -----\n")
            f.write(f"Best Content Type : {content_type}\n")
            f.write(f"Best Time         : {post_time}:00 hrs\n")
            f.write(f"Engagement Score  : {score:.2f}\n")
            f.write("Generated Caption:\n")
            f.write(caption + "\n")
            f.write("--------------------------\n\n")

    # -------------------------
    # STEP 5: Agent Loop
    # -------------------------
    def run(self):
        content_type, score, post_time = self.decide_strategy()
        caption = self.generate_post_with_ai(content_type, post_time)

        print("\n🤖 SOCIAL MEDIA MANAGER AGENT (CLI)")
        print("=" * 50)
        print(f"📊 Best Content Type : {content_type}")
        print(f"📈 Avg Engagement   : {score:.2f}")
        print(f"⏰ Best Time        : {post_time}:00 hrs")

        print("\n📝 Generated Caption:")
        print("-" * 50)
        print(caption)

        print("\n🧠 Agent Reasoning:")
        print("-" * 50)
        print(
            f"{content_type} posts historically achieved the highest engagement.\n"
            f"Audience activity peaks around {post_time}:00 hrs.\n"
            f"The agent used these insights to generate optimized content."
        )
        print("=" * 50)

        # Save decision to memory
        self.save_decision(content_type, post_time, score, caption)


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    agent = SocialMediaAgent("data/posts.csv")
    agent.run()
