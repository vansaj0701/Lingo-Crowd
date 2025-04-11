
# Lingo Crowd - Crowdsourced Translation Platform

**Lingo Crowd** is a dynamic, user-driven platform for submitting, translating, and reviewing text content across different languages. Whether you're a user looking to request a translation or a translator contributing to the global conversation, Lingo Crowd provides a space for collaboration and seamless interaction. It aims to bring together people from all over the world to break down language barriers.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps to Run Locally](#steps-to-run-locally)
- [Database Schema](#database-schema)
  - [Request Table](#request-table)
  - [Contributions Table](#contributions-table)
  - [Voting Logs Table](#voting-logs-table)
- [Usage](#usage)
  - [Request a Translation](#request-a-translation)
  - [Contribute a Translation](#contribute-a-translation)
  - [Vote on Contributions](#vote-on-contributions)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

Lingo Crowd is designed to allow users to submit translation requests and contribute their translations. The platform supports multiple languages and enables users to request translations or assist others by offering their translations. Each translation request is given a unique `search_id`, which users can use to track and contribute to the request.

### Key Features:

- **Translation Requests**: Users can submit requests for translation of content into different languages.
- **Anonymous Contributions**: Users can submit their translations without the need for authentication.
- **Upvote and Downvote System**: Translations are rated by the community to ensure the best translation is highlighted.
- **No User Authentication**: The platform does not require users to sign up or log in to submit requests or contribute.
- **IP-Based Voting**: Voting is tracked via IP addresses to ensure fairness and prevent spam voting.

---

## Features

- **Translation Requests**: Request translations for any content in any language and specify the target language.
- **Contributions**: Users can contribute their translations to the request.
- **Voting System**: Contribute by voting on the accuracy and quality of translations.
- **Search Functionality**: Filter requests by original language or the language to be translated into.

---

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5 (for responsive design)

- **Backend**:
  - Python (Flask framework)

- **Database**:
  - SQLite (for storing translation requests, contributions, and voting data)

- **Other Libraries**:
  - `random` (to generate unique search IDs)
  - `flask` (for server-side logic and rendering templates)
  - `sqlite3` (for database management)

---

## How It Works

### 1. Request a Translation
Users can visit the **Request Translation** page, where they fill out a form with a title, description (content to be translated), the source language, and the target language. After submission, each request receives a unique `search_id`, which can be used for future reference and tracking.

### 2. Contribute a Translation
Once a translation request is made, users can view open requests by selecting the language they want to contribute to. Users can submit their translations, and each contribution is associated with a specific request.

### 3. Vote on Contributions
The platform supports an upvote/downvote system to evaluate the quality of translations. Users can vote for the best translations, helping to improve the accuracy and relevance of each contribution.

### 4. IP-Based Tracking
Voting is done based on the user's IP address to ensure that each person can only vote once per contribution. This helps maintain the integrity of the voting system.

---

## Project Structure

```
├── app.py                # Main backend file with routes and logic
├── languages.py          # List of supported languages
├── templates/            # All HTML templates
│   ├── index.html        # Homepage with introduction and search box
│   ├── requests.html     # Request translation form
│   ├── success.html      # Success page after request submission
│   ├── contribute.html   # Contribute page to view requests and add translations
│   ├── view.html         # View page for individual request and its contributions
│   ├── layout.html       # Base template for consistent layout
├── static/               # Static files (CSS, images)
│   ├── styles.css        # Custom styles
│   ├── cover_page.png    # Cover image for homepage
│   ├── unity.jpg         # Image used in the main header
│   ├── contribute_image.jpg  # Image used in contribute section
│   ├── vote_symbol.png   # Voting icon (upvote/downvote)
└── lingo_crowd.db        # SQLite database file
```

---

## Installation

### Prerequisites

- **Python** 3.x
- **SQLite** (comes pre-installed with Python)

Make sure you have Python installed by running:
```bash
python --version
```

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/vansaj0701/lingo-crowd.git
   ```

2. Navigate to the project directory:
   ```bash
   cd lingo-crowd
   ```

3. Install the required dependencies (if any are needed):
   ```bash
   pip install flask
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Open your browser and visit:
   ```bash
   http://127.0.0.1:5000/
   ```
   You should now be able to access the platform locally.

---

## Database Schema

### `request` Table

This table stores information about translation requests.

| Column       | Type      | Description                               |
|--------------|-----------|-------------------------------------------|
| `title`      | TEXT      | The title of the translation request.     |
| `request_text`| TEXT     | The content to be translated.             |
| `language`   | TEXT      | The source language of the content.       |
| `translate_to`| TEXT     | The target language for the translation.  |
| `search_id`  | TEXT      | Unique identifier for each translation request. |

### `contributions` Table

This table stores user-submitted translations.

| Column         | Type      | Description                               |
|----------------|-----------|-------------------------------------------|
| `contribution_id`| INTEGER | Unique ID for each contribution.          |
| `request_id`   | INTEGER   | The ID of the translation request being contributed to. |
| `contribution_text` | TEXT | The translated content.                   |
| `language`     | TEXT      | The language in which the contribution is made. |
| `upvote`       | INTEGER   | The number of upvotes for this contribution. |
| `downvote`     | INTEGER   | The number of downvotes for this contribution. |

### `voting_logs` Table

This table tracks user votes to prevent multiple votes from the same IP address.

| Column           | Type      | Description                            |
|------------------|-----------|----------------------------------------|
| `contribution_id`| INTEGER   | The ID of the contribution being voted on. |
| `ip_address`     | TEXT      | The IP address of the voter.           |
| `vote_type`      | TEXT      | The type of vote ('up' or 'down').     |

---

## Usage

### Request a Translation

1. Go to the homepage and click on **Request a Translation**.
2. Fill out the form with the title, content, and source/target languages.
3. Click **Submit** to make the request.
4. You'll receive a `search_id` which can be used to track your request.

### Contribute a Translation

1. Go to the **Contribute** page.
2. Use the search functionality to find the translation request you want to contribute to.
3. Submit your translation by filling out the provided form.

### Vote on Contributions

1. On the **View** page of a translation request, you can upvote or downvote other users' contributions.
2. Your vote is recorded by your IP address, and you can only vote once for each contribution.

---

## Contributing

We welcome contributions to improve Lingo Crowd! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request on GitHub.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Unsplash](https://unsplash.com) for the free high-quality images used in this project.
- [Bootstrap 5](https://getbootstrap.com) for the responsive front-end framework that made designing easier.
- [Flask](https://flask.palletsprojects.com/) for the easy-to-use backend framework.
