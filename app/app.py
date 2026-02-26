from fastapi import FastAPI,HTTPException

app=FastAPI()
text={1:{"text":"new","content":"cool"}}
@app.get("/")
def getter():
    return text

@app.get("/products{id}")
def finder(id:int):
    data=getter()
    if id not in data:
        raise HTTPException(status_code=404,detail=f"product id {id} not found")
    return data.get(id)

# @app.post()
#
#
# @app.delete()
#
#
# @app.put()