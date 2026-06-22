import os
import re
import sys
import time
import json
import requests

LEETCODE_SESSION = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfYXV0aF91c2VyX2lkIjoiMjIzMDMzOTEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYTI2ZGYxNDkyNzFkOGM5MzQxZWIxNWRhMDVhYjNhNmUzOTU3MzQyOTE3OTI0Mjk1MzczZTc2NWY4YzQ2ODIyIiwic2Vzc2lvbl91dWlkIjoiYTc1ZDg4ZDkiLCJpZCI6MjIzMDMzOTEsImVtYWlsIjoiYWxhZ2lyaXByYXZlZW5AZ21haWwuY29tIiwidXNlcm5hbWUiOiJQcmF2ZWVua3VtYXIzNzMiLCJ1c2VyX3NsdWciOiJQcmF2ZWVua3VtYXIzNzMiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzgyMTQyMDU4LCJpcCI6IjE1Ny41MS43OS41MCIsImlkZW50aXR5IjoiMTZmZWUzNzU1OWRiZDQyYjQ0ODIwNDQ0NmQwMjA4OWYiLCJkZXZpY2Vfd2l0aF9pcCI6WyIzZTJmN2RjOTY2OGI1OTA1MDViYjcwNGMwNzA0Y2FkNyIsIjE1Ny41MS43OS41MCJdLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.D12_A37PvbYSim5oh7XVFv9TQf4Jak20lXbM2Fyz6-w"
CSRF_TOKEN = "aYc0qhko3SX4OIhTaxfC7LZZ9v548f3U"

if not LEETCODE_SESSION or not CSRF_TOKEN:
    print("Missing environment variables.")
    print("Set them like this before running:")
    print('  export LEETCODE_SESSION="paste_value_here"')
    print('  export LEETCODE_CSRF="paste_value_here"')
    sys.exit(1)

BASE_URL = "https://leetcode.com"
GRAPHQL_URL = f"{BASE_URL}/graphql"
OUTPUT_DIR = "LeetCode"
PROGRESS_FILE = ".export_progress.json"
DELAY_SECONDS = 1.5

EXT_MAP = {
    "python3": "py",
    "python": "py",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "csharp": "cs",
    "javascript": "js",
    "typescript": "ts",
    "kotlin": "kt",
    "swift": "swift",
    "golang": "go",
    "ruby": "rb",
    "scala": "scala",
    "rust": "rs",
    "php": "php",
    "racket": "rkt",
    "erlang": "erl",
    "elixir": "ex",
    "dart": "dart",
}

session = requests.Session()
session.cookies.set("LEETCODE_SESSION", LEETCODE_SESSION, domain=".leetcode.com")
session.cookies.set("csrftoken", CSRF_TOKEN, domain=".leetcode.com")
session.headers.update({
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/",
    "x-csrftoken": CSRF_TOKEN,
    "User-Agent": "Mozilla/5.0 (compatible; personal-export-script/1.0)",
})


def graphql(query, variables):
    response = session.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def get_solved_problems():
    query = """
    query userProgressQuestionList($filters: UserProgressQuestionListInput) {
      userProgressQuestionList(filters: $filters) {
        totalNum
        questions {
          frontendId
          title
          titleSlug
          difficulty
          lastSubmittedAt
          questionStatus
        }
      }
    }
    """
    all_questions = []
    skip = 0
    limit = 100
    while True:
        variables = {"filters": {"skip": skip, "limit": limit, "questionStatus": "SOLVED"}}
        data = graphql(query, variables)
        chunk = data["userProgressQuestionList"]["questions"]
        if not chunk:
            break
        all_questions.extend(chunk)
        skip += limit
        if len(chunk) < limit:
            break
        time.sleep(0.5)
    return all_questions


def get_latest_accepted_submission_code(title_slug):
    query = """
    query submissionList($questionSlug: String!) {
      questionSubmissionList(questionSlug: $questionSlug, offset: 0, limit: 20) {
        submissions {
          id
          statusDisplay
          lang
          timestamp
        }
      }
    }
    """
    data = graphql(query, {"questionSlug": title_slug})
    submissions = data["questionSubmissionList"]["submissions"]
    accepted = [s for s in submissions if s["statusDisplay"] == "Accepted"]
    if not accepted:
        return None, None
    latest = max(accepted, key=lambda s: int(s["timestamp"]))
    code = get_submission_code(latest["id"])
    return code, latest["lang"]


def get_submission_code(submission_id):
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
      }
    }
    """
    data = graphql(query, {"submissionId": int(submission_id)})
    details = data.get("submissionDetails")
    if not details:
        return None
    return details["code"]


def safe_filename(name):
    name = re.sub(r"[\\/:\"*?<>|]+", "", name)
    return name.strip()


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"done_slugs": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def main():
    for difficulty in ["Easy", "Medium", "Hard"]:
        os.makedirs(os.path.join(OUTPUT_DIR, difficulty), exist_ok=True)

    print("Fetching list of solved problems...")
    problems = get_solved_problems()
    print(f"Found {len(problems)} solved problems.")

    progress = load_progress()
    done_slugs = set(progress["done_slugs"])

    for i, problem in enumerate(problems, 1):
        slug = problem["titleSlug"]
        title = problem["title"]
        frontend_id = problem["frontendId"]
        difficulty = problem["difficulty"].capitalize()

        if slug in done_slugs:
            print(f"[{i}/{len(problems)}] Skipping (already done): {title}")
            continue

        print(f"[{i}/{len(problems)}] Fetching: {frontend_id}. {title} ({difficulty})")

        try:
            code, lang = get_latest_accepted_submission_code(slug)
        except Exception as e:
            print(f"  Failed to fetch submission for {title}: {e}")
            time.sleep(DELAY_SECONDS)
            continue

        if not code:
            print(f"  No accepted submission found for {title}, skipping.")
            done_slugs.add(slug)
            progress["done_slugs"] = list(done_slugs)
            save_progress(progress)
            continue

        ext = EXT_MAP.get(lang, "txt")
        filename = f"{frontend_id}. {safe_filename(title)}.{ext}"
        filepath = os.path.join(OUTPUT_DIR, difficulty, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        done_slugs.add(slug)
        progress["done_slugs"] = list(done_slugs)
        save_progress(progress)

        time.sleep(DELAY_SECONDS)

    print("\nDone. Solutions saved under the 'LeetCode' folder.")
    print("You can now run the git init / push steps.")


if __name__ == "__main__":
    main()