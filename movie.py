from theater import app
import theater.src.initDB as db

schema = "./theater/db/schema.sql"
data = "./theater/db/data.sql"
procedures = "./theater/db/procedures.sql"
db.initDB(schema, data, procedures)



app.secret_key="afd34cf"
app.run(debug=True)
