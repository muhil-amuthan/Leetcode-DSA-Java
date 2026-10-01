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
    "Other",
]


# ============================================================
# LEETCODE TOPIC MAPPING
# ============================================================

TAG_MAPPING = {
    "array": "Arrays",
    "string": "Strings",
    "hash table": "HashMap",
    "two pointers": "Two-Pointers",
    "sliding window": "Sliding-Window",
    "stack": "Stack",
    "queue": "Queue",
    "monotonic queue": "Queue",
    "linked list": "LinkedList",
    "binary search": "Binary-Search",
    "sorting": "Sorting",
    "tree": "Trees",
    "binary tree": "Trees",
    "binary search tree": "Trees",
    "heap": "Heap",
    "priority queue": "Heap",
    "graph": "Graphs",
    "breadth-first search": "Graphs",
    "depth-first search": "Graphs",
    "greedy": "Greedy",
    "backtracking": "Backtracking",
    "dynamic programming": "Dynamic-Programming",
    "math": "Math",
    "number theory": "Math",
    "bit manipulation": "Bit-Manipulation",
    "matrix": "Matrix",
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
    text = re.sub(
        r"[^a-z0-9\s\-]",
        " ",
        text
    )
    text = re.sub(
        r"\s+",
        " ",
        text
    )
    return text.strip()


# ============================================================
# GET POSSIBLE LEETCODE SLUG
# ============================================================

def get_problem_slug(path):
    name = os.path.basename(path)

    # Remove extension
    name = os.path.splitext(name)[0]

    # Remove LeetHub problem number (e.g. 1-two-sum, 0001-two-sum)
    name = re.sub(
        r"^\d+[-_\s]+",
        "",
        name
    )

    # Convert to LeetCode slug
    name = name.lower()
    name = re.sub(
        r"[^a-z0-9]+",
        "-",
        name
    )
    name = name.strip("-")

    return name


# ============================================================
# GET LEETCODE TOPICS
# ============================================================

def get_leetcode_topics(slug):
    if not slug:
        return []

    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            title
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
        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        question = (
            result
            .get("data", {})
            .get("question")
        )

        if not question:
            return []

        tags = question.get(
            "topicTags",
            []
        )

        return [
            tag["name"].lower()
            for tag in tags
        ]

    except Exception as error:
        print(
            f"Could not fetch LeetCode topics "
            f"for '{slug}': {error}"
        )
        return []


# ============================================================
# DETERMINE TOPIC
# ============================================================

def determine_topic(path):
    filename = os.path.basename(path)
    slug = get_problem_slug(path)

    print(f"\nChecking: {filename}")
    print(f"Problem slug: {slug}")

    # --------------------------------------------------------
    # Try official LeetCode tags
    # --------------------------------------------------------
    tags = get_leetcode_topics(slug)

    if tags:
        print("LeetCode tags:", ", ".join(tags))
        for tag in tags:
            if tag in TAG_MAPPING:
                topic = TAG_MAPPING[tag]
                print(f"Topic selected: {topic}")
                return topic

    # --------------------------------------------------------
    # Keyword fallback
    # --------------------------------------------------------
    text = clean_text(filename + " " + slug)

    for keyword, topic in KEYWORD_MAPPING.items():
        if keyword in text:
            print(f"Fallback topic: {topic}")
            return topic

    # --------------------------------------------------------
    # Analyze file / directory contents (Code inspection)
    # --------------------------------------------------------
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

    # High-confidence code structure detection
    code_lower = code_content.lower()
    if "treenode" in code_lower or "root.left" in code_lower or "root.right" in code_lower:
        print("Code-based topic: Trees")
        return "Trees"
    if "listnode" in code_lower or ".next" in code_lower:
        print("Code-based topic: LinkedList")
        return "LinkedList"
    if "priorityqueue" in code_lower:
        print("Code-based topic: Heap")
        return "Heap"
    if "matrix" in text or "[][]" in code_content or "grid[" in code_lower:
        print("Code-based topic: Matrix")
        return "Matrix"
    if "stack<" in code_lower:
        print("Code-based topic: Stack")
        return "Stack"
    if "hashmap" in code_lower or "hashset" in code_lower or "map<" in code_lower:
        print("Code-based topic: HashMap")
        return "HashMap"

    # General keywords in code
    for keyword, topic in KEYWORD_MAPPING.items():
        if keyword in code_lower:
            print(f"Code-based topic: {topic}")
            return topic

    # General keywords in README (problem description)
    for keyword, topic in KEYWORD_MAPPING.items():
        if keyword in readme_content:
            print(f"README-based topic: {topic}")
            return topic

    print("Topic: Other")
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

    code_extensions = (".java", ".cpp", ".py", ".js", ".ts", ".c", ".cs", ".go", ".rs", ".kt")
    has_code = any(file.endswith(code_extensions) for file in files)

    # Standard LeetHub directory contains README.md and solution file
    if "README.md" in files and has_code:
        return True

    # Also handle problem directory formatted as [number]-[slug] with code inside
    dirname = os.path.basename(path)
    if re.match(r"^\d+[-_]", dirname) and has_code:
        return True

    return False


# ============================================================
# FIND LEETCODE DIRECTORIES
# ============================================================

def find_problem_directories():
    directories = []

    for root, dirs, files in os.walk(ROOT):
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
    extensions = (".java", ".cpp", ".py", ".js", ".ts")

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRECTORIES
            and d not in TOPIC_FOLDERS
        ]

        for file in files:
            if not file.endswith(extensions):
                continue

            path = os.path.join(root, file)
            solution_files.append(path)

    return solution_files


# ============================================================
# MOVE LEETCODE DIRECTORY
# ============================================================

def move_problem_directory(path):
    topic = determine_topic(path)
    destination_folder = os.path.join(ROOT, topic)
    os.makedirs(destination_folder, exist_ok=True)

    directory_name = os.path.basename(path)
    destination = os.path.join(destination_folder, directory_name)

    if os.path.abspath(path) == os.path.abspath(destination):
        return

    if os.path.exists(destination):
        print(f"Already exists: {destination}")
        # Merge duplicate files if any, then remove source directory
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
        return

    print(
        f"MOVING DIRECTORY:\n"
        f"  {path}\n"
        f"  -> {destination}"
    )

    shutil.move(path, destination)


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
        return

    if os.path.exists(destination):
        print(f"Already exists: {destination}")
        return

    print(
        f"MOVING FILE:\n"
        f"  {path}\n"
        f"  -> {destination}"
    )

    shutil.move(path, destination)


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("==========================================")
    print("     LEETCODE REPOSITORY ORGANIZER")
    print("==========================================")
    print()

    # Create folders
    create_topic_folders()

    # --------------------------------------------------------
    # First handle LeetHub problem directories
    # --------------------------------------------------------
    problem_directories = find_problem_directories()
    print(f"Found {len(problem_directories)} LeetCode problem directories.")

    for directory in problem_directories:
        move_problem_directory(directory)

    # --------------------------------------------------------
    # Then handle standalone files
    # --------------------------------------------------------
    solution_files = find_solution_files()
    print(f"\nFound {len(solution_files)} standalone solution files.")

    for file in solution_files:
        move_solution_file(file)

    # --------------------------------------------------------
    # Clean up any leftover empty directories
    # --------------------------------------------------------
    for root, dirs, files in os.walk(ROOT, topdown=False):
        dir_name = os.path.basename(root)
        if dir_name not in IGNORE_DIRECTORIES and dir_name not in TOPIC_FOLDERS and root != ROOT:
            if not os.listdir(root):
                try:
                    os.rmdir(root)
                    print(f"Removed empty directory: {root}")
                except Exception:
                    pass

    print()
    print("==========================================")
    print("       ORGANIZATION COMPLETED")
    print("==========================================")


if __name__ == "__main__":
    main()
