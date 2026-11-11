import requests
import sys
import re
import threading
import itertools
import os
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

def main():
    print("\n=====LIST YOUR FAVORITE ANIME=====\n")
    print(f"SOME GENRE : {KNOWN_GENRES}\n")
    user_input=input("ENTER NAME/GENRE/TRENDING : ")
    sys.stdout.write("\r"+" "*30+"\r")
    sys.stdout.write("\n")
    sys.stdout.flush()
    cleaned_input=clean_input(user_input)
    api=get_api(cleaned_input)
    result=search_anime(api,cleaned_input)
    
    print(api)


# CLEAN USER INPUT ======================================
def clean_input(x:str)->str:
    if not isinstance(x, str):
        raise TypeError("Anime name must be a string.")
    x = " ".join(x.strip().split())
    x=x.lower()
    if not x :
        print("ENTER SOMETHING....")
        sys.exit(1)
    elif len(x)<2:
        print("INPUT TOO SHORT....")
        sys.exit(1)
    elif not re.fullmatch(r"[a-zA-Z0-9 ]+", x):
        print("INVALID INPUT....")
        sys.exit(1)
    return x 

#GET API ===============================================
def get_api(y:str)->str:
    load_dotenv()
    api_key=os.getenv("anime_api")
    if not api_key :
        print("NO API KEY FOUND ...")
        sys.exit(1)
    return api_key

#SEARCH_ANIME ==========================================
def search_anime(api,z:str,limit=5):
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
# Default variables (ALL None)
    variables = {
      "search": None,
      "genre": None,
      "sort": ["POPULARITY_DESC"],
      "perPage": limit,
    }
    if z in ["trending", "trend", "top"]:
        variables["sort"] = ["TRENDING_DESC"]
        print("🔥 Showing Trending Anime:\n")

if __name__=="__main__":
    main()
