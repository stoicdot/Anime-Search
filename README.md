# 🎌 Anime Search

A Python-based Anime Search application powered by the **AniList GraphQL API**. Search your favorite anime, explore trending titles, filter anime by genre, and save your search history locally.

## ✨ Features

- 🔍 **Anime Search** – Search anime by title.
- 🎭 **Genre Filtering** – Explore anime by different genres.
- 🔥 **Trending Anime** – Discover currently trending anime.
- 📊 **Anime Information** – Get anime titles, average scores, release years, and genres.
- ⏳ **Loading Animation** – Terminal spinner using Python threading.
- 💾 **Search History** – Automatically save previous searches in JSON format.
- 📂 **Local Storage** – Organize search history inside a dedicated folder.
- ⚠️ **Error Handling** – Handle API errors, connection issues, and request timeouts.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Requests | HTTP API requests |
| AniList GraphQL API | Anime data retrieval |
| JSON | Store search history |
| Threading | Loading animation |
| Python-dotenv | Environment variable management |

## 📁 Project Structure

```text
Anime-Search/
│
├── 1st/
│   └── anime_results.json
│
├── main.py
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd Anime-Search
```

### 3. Install dependencies

```bash
pip install requests python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project directory:

```env
anime_api=your_api_key_here
```

**Note:** The public AniList GraphQL API does not require an API key for basic anime searches. The environment variable setup is retained for future integrations.

### 5. Run the application

```bash
python main.py
```

## 🚀 How to Use

After running the application, you will see:

```text
===== ANIME SEARCH SYSTEM =====

1. SEARCH ANIME
2. VIEW SEARCH HISTORY
3. EXIT

ENTER YOUR CHOICE:
```

### Search Anime

Enter an anime title:

```text
ENTER NAME/GENRE/TRENDING: Naruto
```

### Search by Genre

Available genres include:

- Action
- Adventure
- Comedy
- Drama
- Fantasy
- Horror
- Romance
- Sci-Fi
- Sports
- Thriller

### Explore Trending Anime

```text
ENTER NAME/GENRE/TRENDING: trending
```

### View Search History

Select option `2` to view your previously saved anime searches.

## 📦 Data Storage

Search results are automatically stored in:

```text
1st/anime_results.json
```

The JSON file stores:

- Search query
- Total results
- Anime titles
- Average scores
- Release years
- Genres

Previous search records are preserved when new searches are saved.

## 🌐 API Reference

This project uses the AniList GraphQL API.

**API Endpoint:**

https://graphql.anilist.co

Official Documentation:

https://docs.anilist.co/

## 🔒 Security

- API credentials should be stored in `.env`.
- Never upload real API keys or secrets to GitHub.
- `.env` and local search history should be excluded using `.gitignore`.

## 🔮 Future Improvements

- [ ] Anime descriptions and cover images
- [ ] Detailed anime information
- [ ] Anime recommendations
- [ ] Advanced search filters
- [ ] Delete search history option
- [ ] Interactive terminal interface

## 👨‍💻 Author

**Stoic**

Developed as a Python learning project to explore API integration, GraphQL, JSON handling, exception handling, and multithreading.

## 📜 License

This project is open-source and available for learning and educational purposes.