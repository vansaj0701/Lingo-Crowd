from flask import Flask, render_template, request, redirect, flash
from languages import languages
import sqlite3
import random
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
db_name = os.getenv("DATABASE_NAME")


def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.remote_addr
    return ip


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/requests", methods=["POST", "GET"])
def requests():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        language = request.form.get("language")
        translate_to = request.form.get("translate-to")

        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        search_id = ""

        for i in range(8):
            search_id += random.choice(letters)

        try:
            cur.execute(
                "INSERT INTO request (title, request_text, language, translate_to, search_id) VALUES (?, ?, ?, ?, ?)",
                (title, content, language, translate_to, search_id)
            )
            conn.commit()
            return redirect(f"/success?search_id={search_id}")
        except:
            return render_template("requests.html", languages=languages)
        finally:
            conn.close()
    else:
        return render_template("requests.html", languages=languages)


@app.route("/success")
def success():
    search_id = request.args.get("search_id")
    return render_template("success.html", search_id=search_id)


@app.route("/contribute", methods=["POST", "GET"])
def contribute():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    if request.method == "POST":
        language = request.form.get("language")
        translate_to = request.form.get("translate-to")
        search_id = request.form.get("search-id")

        if language and not translate_to:
            query = f"SELECT title, request_text, search_id FROM request WHERE language='{language}' GROUP BY language"
        elif translate_to and not language:
            query = f"SELECT title, request_text, search_id FROM request WHERE translate_to='{translate_to}' GROUP BY translate_to"
        elif translate_to and language:
            query = f"SELECT title, request_text, search_id FROM request WHERE translate_to='{translate_to}' AND language='{language}'"
        else:
            query = "SELECT title, request_text, search_id FROM request"

        if search_id:
            query = f"SELECT title, request_text, search_id FROM request WHERE search_id='{search_id}'"

        cur.execute(query)
        response = cur.fetchall()
        result = {id: (title, content) for title, content, id in response}

        conn.close()

    else:
        cur.execute("SELECT title, request_text, search_id FROM request")
        response = cur.fetchall()
        result = {id: (title, content) for title, content, id in response}
        conn.close()

    return render_template("contribute.html", languages=languages, result=result)


@app.route("/view/<search_id>", methods=["POST", "GET"])
def view(search_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute(
        "SELECT request_id, title, request_text, language, translate_to FROM request WHERE search_id=?", (search_id,))
    response = cur.fetchone()
    request_id, title, content, language, translate_to = response

    ip = get_ip()

    if request.method == "POST":
        contribution_language = request.form.get("contribution-language")
        add_contribution = request.form.get("add-contribution")
        contribution_id = request.form.get("contribution-id")
        vote_type = request.form.get("vote-type")

        if contribution_language and add_contribution:
            cur.execute("""
                        INSERT INTO contributions (request_id, contribution_text, language)
                        VALUES (?, ?, ?)
                        """, (request_id, add_contribution, contribution_language)
                        )
            conn.commit()

        elif contribution_id and vote_type:
            cur.execute("""
                        SELECT * FROM voting_logs
                        WHERE contribution_id=? AND ip_address=?
                        """, (contribution_id, ip)
                        )
            vote_exists = cur.fetchone()

            if not vote_exists:
                cur.execute("""
                            INSERT INTO voting_logs (contribution_id, ip_address, vote_type)
                            VALUES (?, ?, ?)
                            """, (contribution_id, ip, vote_type)
                            )

                if vote_type == 'up':
                    cur.execute(
                        "UPDATE contributions SET upvote = upvote + 1 WHERE contribution_id = ?", (contribution_id,))
                elif vote_type == 'down':
                    cur.execute(
                        "UPDATE contributions SET downvote = downvote + 1 WHERE contribution_id = ?", (contribution_id,))
                conn.commit()
            else:
                flash("You have already voted!", "warning")

    cur.execute(
        """
        SELECT contribution_id, contribution_text, language, upvote, downvote
        FROM contributions
        WHERE request_id=?
        """, (request_id,)
    )
    result = cur.fetchall()[::-1]
    conn.close()

    return render_template("view.html",
                           languages=languages,
                           title=title,
                           language=language,
                           translate_to=translate_to,
                           content=content,
                           contribution_list=result,
                           total_contributions=len(result),
                           search_id=search_id
                           )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)