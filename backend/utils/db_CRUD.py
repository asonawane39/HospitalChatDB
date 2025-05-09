from sqlalchemy import text

def query_sql_db(conn, data):
    print("[*] Accessing MySQL...")
    try:
        query_type = data['query'].strip().lower().split()[0]
        is_write = query_type in {"insert", "update", "delete"}

        # Execute query
        result = conn.execute(text(data['query']))

        # Commit if it's a write operation
        if is_write:
            conn.commit()
            return {
                "message": "Record inserted" if query_type == "insert" else "Query executed",
                "status": "success",
                "data": [],
                "response_length": "single",
                "dbtype":data['dbtype'],
                "dataheaders": []
            }

        # Handle SELECT queries
        if data['response_length'] == 'multiple':
            rows = result.fetchall()
            res = {header: [] for header in data['dataheaders']}

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    res[data['dataheaders'][j]].append(value)

            return {
                "message": "Done!!",
                "status": "success",
                "data": res,
                "response_length": "multiple",
                "dbtype":data['dbtype'],
                "dataheaders": data['dataheaders']
            }

        else:  # single row
            row = result.fetchone()
            res = dict(zip(data['dataheaders'], row)) if row else {}

            return {
                "message": "Done!!",
                "status": "success",
                "data": res,
                "response_length": "single",
                "dbtype":data['dbtype'],
                "dataheaders": data['dataheaders']
            }

    except Exception as err:
        print("[*] Hey sorry!!, I can't do that right now :( ....")
        print(err)  # ✅ Keep visible for debugging
        return {
            "message": "Hey sorry!!, I can't do that right now :( ....",
            "status": "Failed",
            "data": "",
            "response_length": "",
            "dbtype":data['dbtype'],
            "dataheaders": ""
        }

# def query_sql_db(conn, data):
#     print("[*] accessing MYSQL...")
#     try:
#         if data['response_length'] == 'multiple':
#             rows = conn.execute(text(data['query']))
#             if len(data['dataheaders']) == 0: 
#                 return {
#                     "message": "record inserted"
#                 }
#             res = dict()

#             for key in data['dataheaders']: res[key] = []

#             for i in rows:
#                 if count == 5: break
#                 col = 0
#                 for k in i: 
#                     res[data['dataheaders'][col]].append(k)
#                     col += 1
#                 count += 1
#             return {
#                 "message": "Done!!",
#                 "status":"success",
#                 "data": res,
#                 "response_length": data["response_length"],
#                 "dataheaders": data['dataheaders']
#             }
#         else:
#             res = conn.execute(text(data['query']))
#             if len(data['dataheaders']) == 0: 
#                 return {
#                     "message": "record inserted"
#                 }
#             conn.commit()
#             res = dict()
#             conn.close()
#             return {
#                 "message": "Done!!",
#                 "status":"success",
#                 "data": next(res),
#                 "response_length": data["response_length"],
#                 "dataheaders": data['dataheaders']
#             }
        
#     except Exception as err:
#         print("[*] Hey sorry!!, I cant do that right now :( ....")
#         # print(err)
#         return {
#                 "message": "Hey sorry!!, I cant do that right now :( ....",
#                 "status":"Faliled",
#                 "data": "",
#                 "response_length": "",
#                 "dataheaders": ""
#             }

# def query_mongo_db(client, data):
#     try:
#         print("[*] Accessing MongoDB...")
#         print(data)
#         local_scope = {"db": client}
#         exec(data['query'], {}, local_scope)

#         result = local_scope.get("result")

#         if data["response_length"] == 'multiple':
#             rows = []
#             for res in result:
#                 rows.append(res)
#             return {
#                 "message": "Done!!",
#                 "status":"success",
#                 "data":  rows,
#                 "response_length": data["response_length"],
#                 "dataheaders": data['dataheaders']
#             }
#         else:
#             # if isinstance(result, int):
#             return {
#                     "message": "Done!!",
#                     "status":"success",
#                     "data": next(result),
#                     "response_length": data["response_length"],
#                     "dataheaders": data['dataheaders']
#                 }
                
#     except Exception:
#         print("[*] Hey sorry!!, I cant do that right now :( ....")
#         return {
#                 "message": "Hey sorry!!, I cant do that right now :( ....",
#                 "status":"Faliled",
#                 "data": "",
#                 "response_length": "",
#                 "dataheaders": ""
#             }

def query_mongo_db(client, data):
    try:
        print("[*] Accessing MongoDB...")
        print("[*] Incoming Query Data:", data)

        db = client
        local_scope = {"db": db}

        query = data['query'].encode().decode('unicode_escape')
        exec(query, {}, local_scope)  # fixed: use local_scope
        result = local_scope.get("result")

        if hasattr(result, "__iter__") and not isinstance(result, dict):
            rows = list(result)
            return {
                "message": "Done!!",
                "status": "success",
                "data": rows,
                "response_length": "multiple",
                "dbtype":data['dbtype'],
                "dataheaders": data['dataheaders']
            }

        return {
            "message": "Done!!",
            "status": "success",
            "data": result,
            "response_length": "single",
            "dbtype":data['dbtype'],
            "dataheaders": data['dataheaders']
        }

    except Exception as err:
        print("[*] Hey sorry!!, I can't do that right now :( ....")
        print("Error:", err)
        return {
            "message": "Hey sorry!!, I can't do that right now :( ....",
            "status": "Failed",
            "data": "",
            "response_length": "",
            "dbtype":data['dbtype'],
            "dataheaders": ""
        }

