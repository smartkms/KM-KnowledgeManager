from db_service import store_text, query

res = store_text("Perica reze raci rep", dict(avtor="Peter", leto=2025))
print(res)
res = query("Kaj dela perica?")
print(res)
