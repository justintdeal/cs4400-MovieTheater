from theater import app
import theater.src.initDB as db

schema = "./theater/db/schema.sql"
data = "./theater/db/data.sql"
db.initDB(schema, data)

app.secret_key="afd34cf"
app.run(debug=True)
