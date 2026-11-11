
import requests
import sys
import re
import threading
import itertools
import os
import json
from dotenv import load_dotenv

KNOWN_GENRES = {
    "action",
    "adventure",
    "comedy",
    "drama",
    "ecchi",
    "fantasy",
    "horror",
    "mahou shoujo",
    "mecha",
    "music",
    "mystery",
    "psychological",
    "romance",
    "sci-fi",
    "slice of life",
    "sports",
    "supernatural",
    "thriller",
}

# HISTORY FILE ==========================================
FOLDER = "1st"
FILENAME = os.path.join(FOLDER, "anime_results.json")


def main():

    # Create folder if not exists
    os.makedirs(FOLDER, exist_ok=True)

    print("\n===== ANIME SEARCH SYSTEM =====\n")
    print("1. SEARCH ANIME")
    print("2. VIEW SEARCH HISTORY")
    print("3. EXIT")

    choice = input("\nENTER YOUR CHOICE : ").strip()

    if choice == "1":

        print("\n===== LIST YOUR FAVORITE ANIME =====\n")
        print(f"SOME GENRE : {KNOWN_GENRES}\n")

        user_input = input("ENTER NAME/GENRE/TRENDING : ")

        sys.stdout.write("\r" + " " * 30 + "\r")
        sys.stdout.write("\n")
        sys.stdout.flush()

        cleaned_input = clean_input(user_input)
        api = get_api(cleaned_input)
        result = search_anime(api, cleaned_input)

        if result:
            save_results(cleaned_input, result)

    elif choice == "2":

        view_history()

    elif choice == "3":

        print("\nTHANKS FOR USING ANIME SEARCH!")
        sys.exit(0)

    else:

        print("INVALID CHOICE!")
        sys.exit(1)


# CLEAN USER INPUT ======================================
def clean_input(x: str) -> str:

    if not isinstance(x, str):
        raise TypeError("Anime name must be a string.")

    x = " ".join(x.strip().split())

    if not x:
        print("ENTER SOMETHING....")
        sys.exit(1)

    elif len(x) < 2:
        print("INPUT TOO SHORT....")
        sys.exit(1)

    elif not any(char.isalnum() for char in x):
        print("INVALID INPUT....")
        sys.exit(1)

    return x


# GET API ===============================================
def get_api(y: str) -> str:

    load_dotenv()
    api_key = os.getenv("anime_api")

    if not api_key:
        print("NO API KEY FOUND ...")
        sys.exit(1)

    return api_key


# SEARCH_ANIME ==========================================
def search_anime(api, user_input: str, limit=5):

    query = """
    query ($search: String, $genre: String, $sort: [MediaSort], $perPage: Int) {
      Page (page: 1, perPage: $perPage) {
        media (type: ANIME, search: $search, genre: $genre, sort: $sort) {
          title {
            romaji
            english
          }
          averageScore
          seasonYear
          genres
        }
      }
    }
    """

    # Default variables
    variables = {
        "search": None,
        "genre": None,
        "sort": ["POPULARITY_DESC"],
        "perPage": limit,
    }

    lower_input = user_input.lower()

    if lower_input in ["trending", "trend", "top"]:

        variables["sort"] = ["TRENDING_DESC"]
        print("🔥 Showing Trending Anime:\n")

    elif lower_input in KNOWN_GENRES:

        variables["genre"] = user_input.title()
        print(f"🎭 Showing Top {user_input} Anime:\n")

    else:

        variables["search"] = user_input
        variables["sort"] = ["SEARCH_MATCH"]
        print(f"🔍 Search Results for '{user_input}':\n")

    try:

        response = requests.post(
            url="https://graphql.anilist.co",
            json={
                "query": query,
                "variables": variables
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            print("GRAPHQL ERROR:", data["errors"])
            return []

        results = data["data"]["Page"]["media"]

        if not results:
            print("Koi anime nahi mila!")
            return []

        print("=" * 40)

        for index, anime in enumerate(results, start=1):

            title = anime["title"]["english"] or anime["title"]["romaji"]

            print(f"\n{index}. {title}")
            print(f"Score  : {anime['averageScore']}")
            print(f"Year   : {anime['seasonYear']}")
            print(f"Genres : {', '.join(anime['genres'])}")

        print("=" * 40)

        return results

    except requests.exceptions.Timeout:
        print("REQUEST TIMEOUT!")
        return []

    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR! CHECK INTERNET.")
        return []

    except requests.exceptions.HTTPError:

        if response.status_code == 400:
            print("BAD REQUEST!")

        elif response.status_code == 401:
            print("UNAUTHORIZED!")

        elif response.status_code == 403:
            print("FORBIDDEN!")

        elif response.status_code == 404:
            print("RESOURCE NOT FOUND!")

        elif response.status_code == 429:
            print("RATE LIMIT EXCEEDED!")

        elif response.status_code >= 500:
            print("SERVER ERROR!")

        else:
            print(f"HTTP ERROR: {response.status_code}")

        return []

    except ValueError:
        print("INVALID JSON RESPONSE!")
        return []

    except KeyError as error:
        print(f"UNEXPECTED API RESPONSE: {error}")
        return []


# SAVE RESULTS ==========================================
def save_results(user_input: str, results: list):

    try:

        if os.path.exists(FILENAME):

            with open(FILENAME, "r", encoding="utf-8") as file:

                try:
                    old_data = json.load(file)
                except json.JSONDecodeError:
                    old_data = []

        else:
            old_data = []

        search_data = {
            "search_query": user_input,
            "total_results": len(results),
            "anime": []
        }

        for anime in results:

            anime_data = {
                "romaji": anime["title"]["romaji"],
                "english": anime["title"]["english"],
                "score": anime["averageScore"],
                "year": anime["seasonYear"],
                "genres": anime["genres"]
            }

            search_data["anime"].append(anime_data)

        old_data.append(search_data)

        with open(FILENAME, "w", encoding="utf-8") as file:

            json.dump(
                old_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nRESULTS SUCCESSFULLY SAVED!")
        print(f"FILE : {FILENAME}")

    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR SAVING RESULTS: {error}")


# VIEW SEARCH HISTORY ===================================
def view_history():

    if not os.path.exists(FILENAME):
        print("\nNO SEARCH HISTORY FOUND!")
        return

    try:

        with open(FILENAME, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not history:
            print("\nNO SEARCH HISTORY FOUND!")
            return

        print("\n========== SEARCH HISTORY ==========\n")

        for index, search in enumerate(history, start=1):

            print(f"\nSEARCH #{index}")
            print(f"Query   : {search['search_query']}")
            print(f"Results : {search['total_results']}")

            for anime_index, anime in enumerate(
                search["anime"], start=1
            ):

                title = anime["english"] or anime["romaji"]

                print(f"\n  {anime_index}. {title}")
                print(f"     Score  : {anime['score']}")
                print(f"     Year   : {anime['year']}")
                print(f"     Genres : {', '.join(anime['genres'])}")

            print("-" * 40)

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"ERROR READING HISTORY: {error}")


if __name__ == "__main__":
    main()
