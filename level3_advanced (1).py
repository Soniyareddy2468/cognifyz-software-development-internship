"""
Cognifyz Software Development Internship - Level 3: Advanced
Task 5: CRUD task manager with persistent storage (text file I/O)
Task 6: Interactive web scraper

Task 6 needs:  pip install requests beautifulsoup4
"""

import os

TASK_FILE = "tasks.txt"
SEP = "|"


# ---------------------------------------------------------------- Task 5
class Task:
    def __init__(self, task_id, title, description="", status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status

    def to_line(self):
        # '|' and newlines are escaped so a line always parses back correctly
        def esc(s):
            return s.replace("\\", "\\\\").replace(SEP, "\\p").replace("\n", "\\n")
        return SEP.join([str(self.task_id), esc(self.title), esc(self.description), esc(self.status)])

    @staticmethod
    def from_line(line):
        def unesc(s):
            out, i = [], 0
            while i < len(s):
                if s[i] == "\\" and i + 1 < len(s):
                    out.append({"p": SEP, "n": "\n", "\\": "\\"}.get(s[i + 1], s[i + 1]))
                    i += 2
                else:
                    out.append(s[i])
                    i += 1
            return "".join(out)

        parts = line.rstrip("\n").split(SEP)
        if len(parts) != 4:
            raise ValueError(f"Malformed line: {line!r}")
        return Task(int(parts[0]), unesc(parts[1]), unesc(parts[2]), unesc(parts[3]))

    def __str__(self):
        return f"[{self.task_id}] {self.title} | {self.status} | {self.description or '-'}"


class TaskManager:
    STATUSES = ("Pending", "In Progress", "Done")

    def __init__(self, filename=TASK_FILE):
        self.filename = filename
        self.tasks = []
        self.load()

    # ---- persistence with error handling
    def load(self):
        self.tasks = []
        if not os.path.exists(self.filename):
            return  # first run: nothing saved yet
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        self.tasks.append(Task.from_line(line))
                    except ValueError as e:
                        print(f"Warning: skipped line {n} ({e})")
        except PermissionError:
            print(f"Error: no permission to read {self.filename}.")
        except OSError as e:
            print(f"Error reading {self.filename}: {e}")

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for t in self.tasks:
                    f.write(t.to_line() + "\n")
            return True
        except PermissionError:
            print(f"Error: no permission to write {self.filename}.")
        except OSError as e:
            print(f"Error writing {self.filename}: {e}")
        return False

    # ---- CRUD
    def _next_id(self):
        return max((t.task_id for t in self.tasks), default=0) + 1

    def create(self, title, description=""):
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        t = Task(self._next_id(), title.strip(), description.strip())
        self.tasks.append(t)
        self.save()
        return t

    def find(self, task_id):
        return next((t for t in self.tasks if t.task_id == task_id), None)

    def update(self, task_id, title=None, description=None, status=None):
        t = self.find(task_id)
        if t is None:
            return False
        if title:
            t.title = title.strip()
        if description:
            t.description = description.strip()
        if status:
            t.status = status
        self.save()
        return True

    def delete(self, task_id):
        t = self.find(task_id)
        if t is None:
            return False
        self.tasks.remove(t)
        self.save()
        return True


def crud_app():
    manager = TaskManager()
    print(f"Loaded {len(manager.tasks)} task(s) from {manager.filename}.")
    while True:
        print("\n--- PERSISTENT TASK MANAGER ---")
        print("1) Add task\n2) View tasks\n3) Update task\n4) Delete task\n0) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            try:
                t = manager.create(input("Title: "), input("Description (optional): "))
                print(f"Added and saved: {t}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            if not manager.tasks:
                print("No tasks yet.")
            for t in manager.tasks:
                print(t)
        elif choice == "3":
            raw = input("Task ID to update: ").strip()
            tid = int(raw) if raw.isdigit() else None
            if tid is None or manager.find(tid) is None:
                print("Task not found.")
                continue
            title = input("New title (blank to keep): ")
            desc = input("New description (blank to keep): ")
            print("Status: 1) Pending  2) In Progress  3) Done  (blank to keep)")
            s = input("Choose: ").strip()
            status = TaskManager.STATUSES[int(s) - 1] if s in ("1", "2", "3") else None
            manager.update(tid, title, desc, status)
            print("Updated and saved.")
        elif choice == "4":
            raw = input("Task ID to delete: ").strip()
            if raw.isdigit() and manager.delete(int(raw)):
                print("Deleted and saved.")
            else:
                print("Task not found.")
        elif choice == "0":
            break
        else:
            print("Invalid option.")


# ---------------------------------------------------------------- Task 6
def scrape_quotes(base_url, pages=1):
    """Scrape quotes, authors and tags from quotes.toscrape.com style pages."""
    import requests
    from bs4 import BeautifulSoup

    results = []
    url = base_url
    for _ in range(pages):
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0 (internship-scraper)"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for q in soup.select("div.quote"):
            results.append({
                "text": q.select_one("span.text").get_text(strip=True),
                "author": q.select_one("small.author").get_text(strip=True),
                "tags": [t.get_text(strip=True) for t in q.select("a.tag")],
            })
        nxt = soup.select_one("li.next a")
        if not nxt:
            break
        url = requests.compat.urljoin(resp.url, nxt["href"])
    return results


def scrape_headings(url):
    """Generic mode: fetch page title and headings/links from any website."""
    import requests
    from bs4 import BeautifulSoup

    resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0 (internship-scraper)"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "(no title)"
    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"]) if h.get_text(strip=True)]
    links = [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a", href=True) if a.get_text(strip=True)]
    return title, headings, links


def web_scraper():
    try:
        import requests  # noqa: F401
        import bs4  # noqa: F401
    except ImportError:
        print("Please install dependencies first:  pip install requests beautifulsoup4")
        return

    import requests

    while True:
        print("\n--- WEB SCRAPER ---")
        print("1) Quotes (quotes.toscrape.com)")
        print("2) Any website: title, headings, links")
        print("0) Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                raw = input("How many pages (1-10)? ").strip()
                pages = int(raw) if raw.isdigit() and 1 <= int(raw) <= 10 else 1
                data = scrape_quotes("https://quotes.toscrape.com/", pages)
                print(f"\nFetched {len(data)} quotes\n" + "=" * 60)
                for i, q in enumerate(data, 1):
                    print(f"{i:>2}. {q['text']}\n    - {q['author']}   Tags: {', '.join(q['tags']) or '-'}\n")
            elif choice == "2":
                url = input("Enter URL: ").strip()
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                title, headings, links = scrape_headings(url)
                print(f"\nTitle: {title}\n" + "=" * 60)
                print("Headings:")
                for h in headings[:15]:
                    print(f"  • {h}")
                print(f"\nLinks (first 15 of {len(links)}):")
                for text, href in links[:15]:
                    print(f"  • {text[:50]}  ->  {href}")
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except requests.exceptions.MissingSchema:
            print("Invalid URL.")
        except requests.exceptions.ConnectionError:
            print("Could not connect. Check the URL and your internet connection.")
        except requests.exceptions.Timeout:
            print("The request timed out.")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


# ---------------------------------------------------------------- Menu
def main():
    while True:
        print("\n--- LEVEL 3 MENU ---")
        print("1) Persistent task manager (Task 5)")
        print("2) Interactive web scraper (Task 6)")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            crud_app()
        elif choice == "2":
            web_scraper()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
