import asyncio, quart, aiosqlite
import context

app = quart.Quart(__name__)
db = None


@app.before_serving
async def startup():
    db = await aiosqlite.connect(context.db_name)


@app.after_serving
async def shutdown():
    await db.close()


@app.get("/")
async def posts():
    async with db.execute("""SELECT id, text FROM post ORDER BY id DESC""") as cur:
        posts = await cur.fetchall()
    return await quart.render_template("index.html", posts=posts)


@app.route("/create/", methods=["POST"])
async def create():
    form = await request.form
    async with db.execute("INSERT INTO post (text) VALUES (?)", (form["text"], )):
        await db.commit()
    return redirect(url_for("index"))


app.run()
