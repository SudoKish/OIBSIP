import requests


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "VoiceAssistant/1.0 (Educational Python Project)"
}


def search_wikipedia(query):

    try:

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 1
        }

        response = requests.get(
            WIKIPEDIA_API,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )

        if results:

            return results[0]["title"]

        return None

    except requests.RequestException as e:

        print("Wikipedia search error:", e)

        return None


def get_wikipedia_summary(title):

    try:

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + title.replace(" ", "_")
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            extract = data.get("extract")

            if extract:

                if len(extract) > 500:

                    extract = extract[:500] + "..."

                return extract

        return None

    except requests.RequestException as e:

        print("Wikipedia summary error:", e)

        return None


def answer_question(question):

    question = question.strip().lower()

    if not question:
        return "Please ask me a question."

    # -----------------------------
    # Specific knowledge questions
    # -----------------------------

    if "who invented python" in question or \
       "who created python" in question or \
       "who developed python" in question:

        search_query = "Guido van Rossum"

    elif "what is python" in question:

        search_query = "Python programming language"

    elif "how python works" in question or \
         "how does python work" in question:

        search_query = "Python programming language"

    elif "tell me about artificial intelligence" in question:

        search_query = "Artificial intelligence"

    else:

        search_query = question

    title = search_wikipedia(search_query)

    if title:

        answer = get_wikipedia_summary(title)

        if answer:

            return answer

    return "Sorry, I could not find an answer to that question."

if __name__ == "__main__":

    while True:

        question = input(
            "\nAsk a question (type exit to stop): "
        )

        if question.lower().strip() in (
            "exit",
            "quit",
            "stop",
            "goodbye",
            "good bye"
        ):

            print("Goodbye!")

            break

        answer = answer_question(
            question
        )

        print("\nAnswer:")
        print(answer)