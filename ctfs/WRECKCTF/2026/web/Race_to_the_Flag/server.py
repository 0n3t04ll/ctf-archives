import os
import time
import uuid
import sqlite3

from dotenv import load_dotenv

load_dotenv()

from flask import (
    Flask,
    redirect,
    render_template_string,
    request,
    session,
    jsonify,
)

app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_PATH = "/tmp/racedb.sqlite3"
PURCHASE_SECRET = os.environ["PURCHASE_SECRET"]
BLOCKED_KEYWORDS = [
    "os", "popen", "system", "subprocess", "import", "eval",
    "exec", "builtins", "globals", "getattr", "class", "mro",
    "subclasses", "config",
]


def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS sessions "
        "(session_id TEXT PRIMARY KEY, username TEXT, balance INTEGER, coupon_used INTEGER)"
    )
    conn.commit()
    conn.close()


init_db()


def is_blocked(text):
    if "_" in text:
        return True
    lower = text.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in lower:
            return True
    return False


STYLE = """
html, body { margin: 0; background: #003057; color: #e0e0e0; }
.content {
    padding: 2rem;
    width: 90%;
    max-width: 700px;
    margin: auto;
    font-family: 'Courier New', monospace;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
h1 { color: #B3A369; }
h2 { color: #B3A369; }
a { color: #B3A369; }
.btn {
    background: #B3A369;
    color: #003057;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-family: inherit;
    font-weight: bold;
}
.btn:hover { background: #c4b57a; }
.btn:disabled { background: #555; cursor: not-allowed; }
input[type=text] {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #B3A369;
    background: #002244;
    color: #e0e0e0;
    font-size: 1rem;
    font-family: inherit;
    width: 300px;
}
.balance { font-size: 1.5rem; color: #B3A369; }
.shop-item {
    background: #002244;
    border: 1px solid #B3A369;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}
.msg { padding: 10px; border-radius: 8px; margin: 5px 0; }
.msg.ok { background: #1b4332; color: #95d5b2; }
.msg.err { background: #3d0000; color: #ff6b6b; }
"""


@app.get("/")
def index():
    return render_template_string(
        """
        <style>{{ style }}</style>
        <div class="content">
            <h1>Burdell's Buzz Mart</h1>
            <p>Welcome to George P. Burdell's unofficial campus shop! Pick a username to start browsing.</p>
            <form method="POST" action="/register">
                <input type="text" name="username" placeholder="Username" required />
                <br><br>
                <button class="btn" type="submit">Enter Shop</button>
            </form>
        </div>
        """,
        style=STYLE,
    )


@app.post("/register")
def register():
    username = request.form.get("username", "").strip()
    if not username:
        return redirect("/")

    session_id = str(uuid.uuid4())
    conn = get_db()
    conn.execute(
        "INSERT INTO sessions (session_id, username, balance, coupon_used) VALUES (?, ?, 1, 0)",
        (session_id, username),
    )
    conn.commit()
    conn.close()

    session["session_id"] = session_id
    return redirect("/shop")


@app.get("/shop")
def shop():
    session_id = session.get("session_id")
    if not session_id:
        return redirect("/")

    conn = get_db()
    row = conn.execute(
        "SELECT username, balance FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    conn.close()

    if not row:
        return redirect("/")

    username, balance = row
    return render_template_string(
        """
        <style>{{ style }}</style>
        <div class="content">
            <h1>Burdell's Buzz Mart</h1>
            <p>Welcome, <b>{{ username }}</b>! George P. Burdell always takes care of fellow Yellow Jackets.</p>
            <p class="balance">BuzzBucks: $<span id="balance">{{ balance }}</span></p>
            <p id="msg"></p>

            <div class="shop-item">
                <h2>Referral Bonus</h2>
                <p>Every new Jacket gets a one-time $1 campus referral bonus!</p>
                <button class="btn" onclick="claimCoupon()">Claim Bonus</button>
            </div>

            <div class="shop-item">
                <h2>Burdell's Premium Membership</h2>
                <p>Get your personalized membership receipt, signed by George P. Burdell himself. Costs $3.</p>
                <button class="btn" onclick="buyItem()">Buy ($3)</button>
            </div>
        </div>
        <script>
            function showMsg(text, ok) {
                const el = document.getElementById("msg");
                el.textContent = text;
                el.className = ok ? "msg ok" : "msg err";
            }
            async function claimCoupon() {
                const r = await fetch("/claim-coupon", {method: "POST"});
                const data = await r.json();
                if (data.success) {
                    document.getElementById("balance").textContent = data.balance;
                    showMsg("Bonus claimed!", true);
                } else {
                    showMsg(data.error, false);
                }
            }
            async function buyItem() {
                const r = await fetch("/buy", {method: "POST"});
                const data = await r.json();
                if (data.success) {
                    showMsg("Purchase complete! Redirecting to receipt...", true);
                    window.location.href = "/receipt?secret=" + encodeURIComponent(data.secret);
                } else {
                    showMsg(data.error, false);
                }
            }
        </script>
        """,
        style=STYLE,
        username=username,
        balance=balance,
    )


@app.post("/claim-coupon")
def claim_coupon():
    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"error": "no session"}), 401

    conn = get_db()
    row = conn.execute(
        "SELECT coupon_used, balance FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "invalid session"}), 400

    coupon_used, balance = row

    if coupon_used:
        conn.close()
        return jsonify({"error": "already claimed"}), 400

    time.sleep(0.1)

    conn.execute(
        "UPDATE sessions SET balance = balance + 1, coupon_used = 1 WHERE session_id = ?",
        (session_id,),
    )
    conn.commit()

    new_balance = conn.execute(
        "SELECT balance FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0]
    conn.close()

    return jsonify({"success": True, "balance": new_balance})


@app.post("/buy")
def buy():
    session_id = session.get("session_id")
    if not session_id:
        return jsonify({"error": "no session"}), 401

    conn = get_db()
    row = conn.execute(
        "SELECT balance FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "invalid session"}), 400

    balance = row[0]
    if balance < 3:
        conn.close()
        return jsonify({"error": "not enough money"}), 400

    conn.execute(
        "UPDATE sessions SET balance = balance - 3 WHERE session_id = ?",
        (session_id,),
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "secret": PURCHASE_SECRET})


@app.get("/receipt")
def receipt():
    secret = request.args.get("secret", "")
    if secret != PURCHASE_SECRET:
        return render_template_string(
            """
            <style>{{ style }}</style>
            <div class="content">
                <h1>Access Denied</h1>
                <p>You need a valid purchase secret to view your receipt.</p>
                <a href="/">Back to shop</a>
            </div>
            """,
            style=STYLE,
        )

    session_id = session.get("session_id")
    if not session_id:
        return redirect("/")

    conn = get_db()
    row = conn.execute(
        "SELECT username FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    conn.close()

    if not row:
        return redirect("/")

    username = row[0]

    if is_blocked(username):
        return render_template_string(
            """
            <style>{{ style }}</style>
            <div class="content">
                <h1>Error</h1>
                <p>Invalid characters detected in username.</p>
                <a href="/">Register again</a>
            </div>
            """,
            style=STYLE,
        )

    template = (
        "<style>" + STYLE + "</style>"
        '<div class="content">'
        "<h1>Burdell's Premium Membership</h1>"
        "<p>This certifies that " + username + " is an official member of George P. Burdell's inner circle.</p>"
        "<p>Go Jackets!</p>"
        "</div>"
    )
    return render_template_string(template)


if __name__ == "__main__":
    app.run(debug=True)
