import sys
sys.dont_write_bytecode = True
import os
import re
import shutil
import json
import urllib.request
import urllib.error


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = "."

TOPIC_FOLDERS = [
    "Arrays",
    "Strings",
    "HashMap",
    "Two-Pointers",
    "Sliding-Window",
    "Stack",
    "Queue",
    "LinkedList",
    "Binary-Search",
    "Sorting",
    "Trees",
    "Heap",
    "Graphs",
    "Greedy",
    "Backtracking",
    "Dynamic-Programming",
    "Math",
    "Bit-Manipulation",
    "Matrix",
    "MySQL",
    "Other",
]


# ============================================================
# TOPIC PRIORITY RANKING
# Specialized data structures & algorithmic paradigms take
# precedence over broad container tags like Array, Math, String.
# ============================================================

TOPIC_PRIORITY = {
    "Dynamic-Programming": 100,
    "Backtracking": 95,
    "Graphs": 90,
    "Trees": 85,
    "Heap": 80,
    "Sliding-Window": 75,
    "Stack": 70,
    "Queue": 65,
    "LinkedList": 60,
    "Binary-Search": 55,
    "Bit-Manipulation": 50,
    "Matrix": 45,
    "MySQL": 40,
    "Two-Pointers": 30,
    "Greedy": 25,
    "HashMap": 20,
    "Sorting": 15,
    "Math": 10,
    "Strings": 8,
    "Arrays": 5,
    "Other": 1,
}


# ============================================================
# LEETCODE TOPIC MAPPING
# ============================================================

TAG_MAPPING = {
    "array": "Arrays",
    "string": "Strings",
    "string matching": "Strings",
    "hash table": "HashMap",
    "two pointers": "Two-Pointers",
    "sliding window": "Sliding-Window",
    "stack": "Stack",
    "monotonic stack": "Stack",
    "queue": "Queue",
    "monotonic queue": "Queue",
    "linked list": "LinkedList",
    "binary search": "Binary-Search",
    "sorting": "Sorting",
    "counting sort": "Sorting",
    "tree": "Trees",
    "binary tree": "Trees",
    "binary search tree": "Trees",
    "trie": "Trees",
    "heap": "Heap",
    "priority queue": "Heap",
    "graph": "Graphs",
    "breadth-first search": "Graphs",
    "depth-first search": "Graphs",
    "union find": "Graphs",
    "greedy": "Greedy",
    "backtracking": "Backtracking",
    "dynamic programming": "Dynamic-Programming",
    "memoization": "Dynamic-Programming",
    "math": "Math",
    "number theory": "Math",
    "geometry": "Math",
    "bit manipulation": "Bit-Manipulation",
    "matrix": "Matrix",
    "database": "MySQL",
    "sql": "MySQL",
    "mysql": "MySQL",
}


# ============================================================
# KEYWORD FALLBACK
# ============================================================

KEYWORD_MAPPING = {
    "parentheses": "Stack",
    "bracket": "Stack",
    "palindrome": "Strings",
    "anagram": "Strings",
    "substring": "Strings",
    "subsequence": "Strings",
    "linkedlist": "LinkedList",
    "linked-list": "LinkedList",
    "binary-search": "Binary-Search",
    "binarysearch": "Binary-Search",
    "sliding-window": "Sliding-Window",
    "slidingwindow": "Sliding-Window",
    "two-pointer": "Two-Pointers",
    "two-pointers": "Two-Pointers",
    "backtracking": "Backtracking",
    "dynamic-programming": "Dynamic-Programming",
    "dynamicprogramming": "Dynamic-Programming",
    "graph": "Graphs",
    "dfs": "Graphs",
    "bfs": "Graphs",
    "tree": "Trees",
    "binary-tree": "Trees",
    "heap": "Heap",
    "priorityqueue": "Heap",
    "matrix": "Matrix",
    "greedy": "Greedy",
    "bit-manipulation": "Bit-Manipulation",
    "sorting": "Sorting",
    "hashmap": "HashMap",
    "hash-map": "HashMap",
    "array": "Arrays",
    "string": "Strings",
}


# ============================================================
# IGNORE DIRECTORIES
# ============================================================

IGNORE_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
}

CODE_EXTENSIONS = (
    ".java",
    ".cpp",
    ".py",
    ".js",
    ".ts",
    ".c",
    ".cs",
    ".go",
    ".rs",
    ".kt",
    ".sql",
)


# ============================================================
# CREATE TOPIC FOLDERS
# ============================================================

def create_topic_folders():
    for topic in TOPIC_FOLDERS:
        path = os.path.join(ROOT, topic)
        os.makedirs(path, exist_ok=True)


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================================================
# GET PROBLEM SLUG
# ============================================================

def get_problem_slug(path):
    name = os.path.basename(path)
    name = os.path.splitext(name)[0]
    # Remove LeetHub problem number prefix (e.g. 0001-two-sum, 1-two-sum)
    name = re.sub(r"^\d+[-_\s]+", "", name)
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


# ============================================================
# PARSE LOCAL README.MD TAGS (FAST FALLBACK)
# ============================================================

_README_TAGS_CACHE = None

def get_readme_tags_map():
    global _README_TAGS_CACHE
    if _README_TAGS_CACHE is not None:
        return _README_TAGS_CACHE

    _README_TAGS_CACHE = {}
    readme_path = os.path.join(ROOT, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            sections = re.findall(
                r"## ([^\n]+)\n\|[^\n]+\n\|[^\n]+\n(.*?)(?=\n## |\n<!--|\Z)",
                content,
                re.DOTALL
            )
            for section_title, table in sections:
                tag_name = section_title.strip().lower()
                problem_names = re.findall(r"\[([0-9]+-[^\]]+)\]", table)
                for p in problem_names:
                    slug = get_problem_slug(p)
                    _README_TAGS_CACHE.setdefault(slug, []).append(tag_name)
                    _README_TAGS_CACHE.setdefault(p, []).append(tag_name)
        except Exception as e:
            print(f"Could not parse local README tags: {e}")

    return _README_TAGS_CACHE


# ============================================================
# GET LEETCODE TOPICS (GRAPHQL WITH TIMEOUT + LOCAL CACHE)
# ============================================================

def get_leetcode_topics(slug):
    if not slug:
        return []

    # 1. First attempt: Local tags extracted from root README.md (instant & rate-limit proof)
    local_tags = get_readme_tags_map().get(slug, [])
    if local_tags:
        return [t.lower() for t in local_tags]

    # 2. Second attempt: LeetCode GraphQL (for newly submitted problems)
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            topicTags {
                name
            }
        }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "titleSlug": slug
        }
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            result = json.loads(response.read().decode("utf-8"))
        question = result.get("data", {}).get("question")
        if question and question.get("topicTags"):
            return [t["name"].lower() for t in question["topicTags"]]
    except Exception:
        pass

    return []


# ============================================================
# DETERMINE TOPIC
# ============================================================

def determine_topic(path, current_topic=None):
    filename = os.path.basename(path)
    slug = get_problem_slug(path)

    # 1. Check tags from LeetCode / README
    tags = get_leetcode_topics(slug)

    if tags:
        candidate_topics = [TAG_MAPPING[t] for t in tags if t in TAG_MAPPING]

        if candidate_topics:
            # Check if there are specialized structural/algorithmic topics (priority >= 45)
            # such as Matrix, Dynamic-Programming, Stack, Binary-Search, Bit-Manipulation, etc.
            has_specialized = any(TOPIC_PRIORITY.get(c, 0) >= 45 for c in candidate_topics)

            # If currently in a generic folder (Arrays, Math, etc.) and a specialized topic exists:
            if has_specialized and current_topic and TOPIC_PRIORITY.get(current_topic, 0) < 45:
                best_topic = max(candidate_topics, key=lambda x: TOPIC_PRIORITY.get(x, 0))
                print(f"Selecting specialized topic '{best_topic}' over generic '{current_topic}' for {filename}")
                return best_topic

            # If current topic is already among the valid candidate topics, keep it
            if current_topic and current_topic in candidate_topics:
                return current_topic

            # Otherwise, pick candidate with highest priority
            best_topic = max(candidate_topics, key=lambda x: TOPIC_PRIORITY.get(x, 0))
            return best_topic

    # 2. Check title/slug keywords
    text = clean_text(filename + " " + slug)
    for keyword, topic in KEYWORD_MAPPING.items():
        if keyword in text:
            return topic

    # 3. Analyze file / directory code contents
    code_content = ""
    readme_content = ""
    files_to_check = []
    if os.path.isfile(path):
        files_to_check.append(path)
    elif os.path.isdir(path):
        for root_dir, _, files in os.walk(path):
            for file in files:
                files_to_check.append(os.path.join(root_dir, file))

    for file_path in files_to_check:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if file_path.endswith("README.md"):
                    readme_content += " " + content.lower()
                else:
                    code_content += " " + content
        except Exception:
            pass

    code_lower = code_content.lower()
    if any(file_path.endswith(".sql") for file_path in files_to_check):
        return "MySQL"
    if "treenode" in code_lower or "root.left" in code_lower or "root.right" in code_lower:
        return "Trees"
    if "listnode" in code_lower or ".next" in code_lower:
        return "LinkedList"
    if "priorityqueue" in code_lower:
        return "Heap"
    if "matrix" in text or "[][]" in code_content or "grid[" in code_lower:
        return "Matrix"
    if "stack<" in code_lower:
        return "Stack"
    if "hashmap" in code_lower or "hashset" in code_lower:
        return "HashMap"

    for keyword, topic in KEYWORD_MAPPING.items():
        if keyword in code_lower:
            return topic
    for keyword, topic in KEYWORD_MAPPING.items():
        if keyword in readme_content:
            return topic

    # If already in a valid topic folder and nothing better was found, stay there
    if current_topic and current_topic in TOPIC_FOLDERS:
        return current_topic

    return "Other"


# ============================================================
# CHECK WHETHER DIRECTORY IS A LEETCODE PROBLEM
# ============================================================

def is_leetcode_problem_directory(path):
    if not os.path.isdir(path):
        return False

    try:
        files = os.listdir(path)
    except Exception:
        return False

    has_code = any(file.endswith(CODE_EXTENSIONS) for file in files)

    # Standard LeetHub directory contains README.md and solution file
    if "README.md" in files and has_code:
        return True

    # Problem directory formatted as [number]-[slug] with code inside
    dirname = os.path.basename(path)
    if re.match(r"^\d+[-_]", dirname) and has_code:
        return True

    return False


# ============================================================
# FIND UNORGANIZED LEETCODE DIRECTORIES
# ============================================================

def find_problem_directories():
    directories = []

    for root, dirs, files in os.walk(ROOT):
        # Exclude ignored directories and existing topic folders
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRECTORIES
            and d not in TOPIC_FOLDERS
        ]

        for directory in dirs:
            full_path = os.path.join(root, directory)
            if is_leetcode_problem_directory(full_path):
                directories.append(full_path)

    return directories


# ============================================================
# FIND STANDALONE SOLUTION FILES
# ============================================================

def find_solution_files():
    solution_files = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRECTORIES
            and d not in TOPIC_FOLDERS
        ]

        for file in files:
            if not file.endswith(CODE_EXTENSIONS):
                continue

            path = os.path.join(root, file)
            solution_files.append(path)

    return solution_files


# ============================================================
# MOVE LEETCODE DIRECTORY
# ============================================================

def move_problem_directory(path, current_topic=None):
    topic = determine_topic(path, current_topic=current_topic)
    destination_folder = os.path.join(ROOT, topic)
    os.makedirs(destination_folder, exist_ok=True)

    directory_name = os.path.basename(path)
    destination = os.path.join(destination_folder, directory_name)

    if os.path.abspath(path) == os.path.abspath(destination):
        return destination

    if os.path.exists(destination):
        print(f"Destination already exists: {destination}. Merging files...")
        try:
            for f in os.listdir(path):
                src_file = os.path.join(path, f)
                dst_file = os.path.join(destination, f)
                if not os.path.exists(dst_file) and os.path.isfile(src_file):
                    shutil.copy2(src_file, dst_file)
            shutil.rmtree(path)
            print(f"Cleaned up duplicate source: {path}")
        except Exception as e:
            print(f"Could not merge duplicate {path}: {e}")
        return destination

    print(f"MOVING DIRECTORY: {path} -> {destination}")
    shutil.move(path, destination)
    return destination


# ============================================================
# MOVE STANDALONE FILE
# ============================================================

def move_solution_file(path):
    topic = determine_topic(path)
    destination_folder = os.path.join(ROOT, topic)
    os.makedirs(destination_folder, exist_ok=True)

    filename = os.path.basename(path)
    destination = os.path.join(destination_folder, filename)

    if os.path.abspath(path) == os.path.abspath(destination):
        return destination

    if os.path.exists(destination):
        print(f"Already exists: {destination}")
        return destination

    print(f"MOVING FILE: {path} -> {destination}")
    shutil.move(path, destination)
    return destination


# ============================================================
# RE-CLASSIFY EXISTING TOPIC FOLDERS
# ============================================================

def reclassify_existing_directories():
    """
    Checks all problems currently inside TOPIC_FOLDERS to ensure
    specialized problems (e.g. Matrix, Stack, DP, Bit-Manipulation)
    are not mistakenly kept in generic folders like Arrays or Math.
    """
    print("\nChecking existing problems for optimal topic placement...")
    for topic in TOPIC_FOLDERS:
        topic_path = os.path.join(ROOT, topic)
        if not os.path.isdir(topic_path):
            continue

        for item in sorted(os.listdir(topic_path)):
            item_path = os.path.join(topic_path, item)
            if is_leetcode_problem_directory(item_path):
                move_problem_directory(item_path, current_topic=topic)


# ============================================================
# UPDATE ROOT README.MD LINKS
# Updates all problem links in README.md to ensure they point
# directly to the correct topic folder path.
# ============================================================

def update_readme_links():
    readme_path = os.path.join(ROOT, "README.md")
    if not os.path.exists(readme_path):
        return

    problem_map = {}
    for topic in TOPIC_FOLDERS:
        topic_dir = os.path.join(ROOT, topic)
        if not os.path.isdir(topic_dir):
            continue
        for item in os.listdir(topic_dir):
            item_path = os.path.join(topic_dir, item)
            if os.path.isdir(item_path):
                problem_map[item] = topic

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    def replace_link(match):
        prob_name = match.group(1)
        base_url = match.group(2)
        if prob_name in problem_map:
            topic = problem_map[prob_name]
            return f"[{prob_name}]({base_url}{topic}/{prob_name}/)"
        return match.group(0)

    pattern = r"\[([0-9]+-[^\]]+)\]\((https://github\.com/[^/]+/[^/]+/tree/[^/]+/)(?:[^/\)]+/)*[0-9]+-[^/\)]+/?\)"
    new_content = re.sub(pattern, replace_link, content)

    if new_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated README.md problem links to point to correct topic folders.")


# ============================================================
# CLEAN UP EMPTY DIRECTORIES SAFELY
# ============================================================

def cleanup_empty_directories():
    for root, dirs, files in os.walk(ROOT, topdown=False):
        parts = os.path.normpath(root).split(os.sep)
        # Never touch anything inside .git or .github or other ignored directories
        if any(part in IGNORE_DIRECTORIES for part in parts):
            continue
        # Never delete the root directory or topic folders
        if root == ROOT or any(part in TOPIC_FOLDERS for part in parts):
            continue

        if not os.listdir(root):
            try:
                os.rmdir(root)
                print(f"Removed empty directory: {root}")
            except Exception:
                pass


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("==========================================")
    print("     LEETCODE REPOSITORY ORGANIZER")
    print("==========================================")
    print()

    # 1. Create topic folders
    create_topic_folders()

    # 2. Organize any new/unorganized problem directories (e.g. from LeetHub)
    problem_directories = find_problem_directories()
    print(f"Found {len(problem_directories)} unorganized problem directories.")
    for directory in problem_directories:
        move_problem_directory(directory)

    # 3. Organize any standalone code solution files
    solution_files = find_solution_files()
    print(f"Found {len(solution_files)} standalone solution files.")
    for file in solution_files:
        move_solution_file(file)

    # 4. Check existing problem directories for optimal topic placement
    reclassify_existing_directories()

    # 5. Clean up any leftover empty directories safely
    cleanup_empty_directories()

    # 6. Update README.md links
    update_readme_links()

    print()
    print("==========================================")
    print("       ORGANIZATION COMPLETED")
    print("==========================================")


if __name__ == "__main__":
    main()
