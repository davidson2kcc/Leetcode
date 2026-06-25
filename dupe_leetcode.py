import os
import re
import sys
import time
import json
import requests

LEETCODE_SESSION = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfYXV0aF91c2VyX2lkIjoiMjIzMDMzOTEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyYTI2ZGYxNDkyNzFkOGM5MzQxZWIxNWRhMDVhYjNhNmUzOTU3MzQyOTE3OTI0Mjk1MzczZTc2NWY4YzQ2ODIyIiwic2Vzc2lvbl91dWlkIjoiYzgzMDc1ZDUiLCJpZCI6MjIzMDMzOTEsImVtYWlsIjoiYWxhZ2lyaXByYXZlZW5AZ21haWwuY29tIiwidXNlcm5hbWUiOiJQcmF2ZWVua3VtYXIzNzMiLCJ1c2VyX3NsdWciOiJQcmF2ZWVua3VtYXIzNzMiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzgyMzQ5MTY5LCJpcCI6IjE1Ny41MS43OS4yMiIsImlkZW50aXR5IjoiNmIyMjFhZDFhOGIwYzYwZGYxOGY4Njg2YjQ4NzY4NzgiLCJkZXZpY2Vfd2l0aF9pcCI6WyI4NzZmZTBkOGUzMWExYzRiZWE2ODg3YzQ3MGI1NGYwNyIsIjE1Ny41MS43OS4yMiJdLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.88EmOkOFyEti1a4fuz5ByN6Rq20DzflH8yQAzw3UkI0"
CSRF_TOKEN = "5eZeVATkHsq2cp9WBHrnRo4Tme5bs2GH"

if not LEETCODE_SESSION or not CSRF_TOKEN:
    print("Missing environment variables.")
    print("Set them like this before running:")
    print('  export LEETCODE_SESSION="paste_value_here"')
    print('  export LEETCODE_CSRF="paste_value_here"')
    sys.exit(1)

BASE_URL = "https://leetcode.com"
GRAPHQL_URL = f"{BASE_URL}/graphql"
OUTPUT_DIR = "."
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


def get_question_details(title_slug):
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        difficulty
        content
        topicTags {
          name
        }
      }
    }
    """
    data = graphql(query, {"titleSlug": title_slug})
    return data["question"]


def get_latest_accepted_submission(title_slug):
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
        return None
    return max(accepted, key=lambda s: int(s["timestamp"]))


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


def html_to_text(html_content):
    text = re.sub(r"<br\s*/?>", "\n", html_content)
    text = re.sub(r"</p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_readme(question, problem_url, folder_topic):
    title = question["title"]
    difficulty = question["difficulty"]
    content_html = question["content"] or ""
    content_text = html_to_text(content_html)
    all_tags = [tag["name"] for tag in question.get("topicTags", [])]
    all_tags_line = ", ".join(all_tags) if all_tags else "Uncategorized"

    readme = f"# {question['questionId']}. {title}\n\n"
    readme += f"**Difficulty:** {difficulty}\n\n"
    readme += f"**Folder Topic:** {folder_topic}\n\n"
    readme += f"**All Topics:** {all_tags_line}\n\n"
    readme += f"**Link:** {problem_url}\n\n"
    readme += "---\n\n"
    readme += content_text + "\n"
    return readme


def safe_folder_name(name):
    name = re.sub(r"[\\/:\"*?<>|]+", "", name)
    return name.strip()


def safe_file_name(name):
    name = re.sub(r"[\\/:\"*?<>|]+", "", name)
    return name.strip()


TOPIC_PRIORITY = [
    "Trie",
    "Union Find",
    "Segment Tree",
    "Binary Indexed Tree",
    "Topological Sort",
    "Minimum Spanning Tree",
    "Shortest Path",
    "Strongly Connected Component",
    "Eulerian Circuit",
    "Biconnected Component",
    "Monotonic Stack",
    "Monotonic Deque",
    "Sliding Window",
    "Two Pointers",
    "Binary Search",
    "Backtracking",
    "Dynamic Programming",
    "Greedy",
    "Divide and Conquer",
    "Bit Manipulation",
    "Bitmask",
    "Recursion",
    "Memoization",
    "Graph",
    "Tree",
    "Binary Tree",
    "Binary Search Tree",
    "Depth-First Search",
    "Breadth-First Search",
    "Heap (Priority Queue)",
    "Hash Table",
    "Hash Function",
    "Linked List",
    "Stack",
    "Queue",
    "Counting",
    "Prefix Sum",
    "Sorting",
    "String Matching",
    "Rolling Hash",
    "Game Theory",
    "Geometry",
    "Combinatorics",
    "Number Theory",
    "Randomized",
    "Probability and Statistics",
    "Concurrency",
    "Design",
    "Simulation",
    "Interactive",
    "Data Stream",
    "Iterator",
    "Database",
    "Shell",
    "String",
    "Array",
    "Matrix",
    "Math",
    "Brainteaser",
]


def get_best_topic(question):
    tags = question.get("topicTags", [])
    names = [tag["name"] for tag in tags]
    if not names:
        return "Uncategorized"
    for priority_name in TOPIC_PRIORITY:
        if priority_name in names:
            return priority_name
    return names[0]


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"done_slugs": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def write_problem_files(topic_folder, frontend_id, title, code, ext, readme_content):
    topic_path = os.path.join(OUTPUT_DIR, safe_folder_name(topic_folder))
    base_name = f"{frontend_id}. {safe_folder_name(title)}"
    problem_path = os.path.join(topic_path, base_name)
    os.makedirs(problem_path, exist_ok=True)

    code_path = os.path.join(problem_path, f"{base_name}.{ext}")
    readme_path = os.path.join(problem_path, f"{base_name}.md")

    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)


def main():
    print("Fetching list of solved problems...")
    problems = get_solved_problems()
    print(f"Found {len(problems)} solved problems.")

    progress = load_progress()
    done_slugs = set(progress["done_slugs"])

    for i, problem in enumerate(problems, 1):
        slug = problem["titleSlug"]
        title = problem["title"]
        frontend_id = problem["frontendId"]

        if slug in done_slugs:
            print(f"[{i}/{len(problems)}] Skipping (already done): {title}")
            continue

        print(f"[{i}/{len(problems)}] Fetching: {frontend_id}. {title}")

        try:
            submission = get_latest_accepted_submission(slug)
            if not submission:
                print(f"  No accepted submission found for {title}, skipping.")
                done_slugs.add(slug)
                progress["done_slugs"] = list(done_slugs)
                save_progress(progress)
                continue

            code = get_submission_code(submission["id"])
            time.sleep(DELAY_SECONDS)

            question = get_question_details(slug)
            time.sleep(DELAY_SECONDS)
        except Exception as e:
            print(f"  Failed to fetch data for {title}: {e}")
            time.sleep(DELAY_SECONDS)
            continue

        if not code:
            print(f"  Could not retrieve code for {title}, skipping.")
            continue

        lang = submission["lang"]
        ext = EXT_MAP.get(lang, "txt")

        best_topic = get_best_topic(question)
        problem_url = f"{BASE_URL}/problems/{slug}/"
        readme_content = build_readme(question, problem_url, best_topic)

        write_problem_files(best_topic, frontend_id, title, code, ext, readme_content)

        print(f"  Saved to: {best_topic}")

        done_slugs.add(slug)
        progress["done_slugs"] = list(done_slugs)
        save_progress(progress)

    print("\nDone. Solutions saved into topic-based folders.")


if __name__ == "__main__":
    main()