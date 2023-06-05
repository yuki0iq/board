import asyncio, quart, aiosqlite
import context

app = quart.Quart(__name__)


async def get_db():
    if 'db' not in quart.g:
        quart.g.db = await aiosqlite.connect(context.db_name)
    return quart.g.db


@app.after_serving
async def shutdown():
    if 'db' in quart.g:
        await quart.g.db.close()


@app.get("/")
async def posts():
    db = await get_db()
    async with db.execute("""SELECT id, text FROM post ORDER BY id DESC""") as cur:
        posts = await cur.fetchall()
        print(posts)
    return await quart.render_template("index.html", posts=posts)


@app.route("/create/", methods=["POST"])
async def create():
    form = await quart.request.form
    db = await get_db()
    async with db.execute("INSERT INTO post (text) VALUES (?)", (form["text"], )):
        pass
    await db.commit()
    return quart.redirect('/')


app.run()
