from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import connect, create_items, get_item_by_id, get_all_items, update_item, delete_item


app = FastAPI()
conn = connect()
cursor = conn.cursor()


class ItemCreate(BaseModel):
    item_name: str
    item_description: str


class Item(BaseModel):
    item_id: int
    item_name: str
    item_description: str


class ItemUpdate(BaseModel):
    item_name: str
    item_description: str


@app.on_event("startup")
async def startup_event():
    initialize_db()


@app.get("/")
async def get_all_items():
    return {"data": "hello world"}


@app.post("/create_items", response_model=Item)
async def add_items(item: ItemCreate):
    item_id = create_item(item.item_name, item.item_description)

    if item_id:
        return {
            "item_id": item_id,
            "item_name": item.item_name,
            "item_description": item.item_description
        }
    else:
        raise HTTPException(status_code=400, detail="Item not created")


@app.post("/get_item/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = get_item_by_id(item_id)

    if item:
        return {
            "item_id": item[0],
            "item_name": item[1],
            "item_description": item[2]
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/see_all_items", response_model=list[Item])
async def see_all_items():
    items = get_all_items()
    return [{"item_id": item[0], "item_name": item[1], "item_description": item[2]} for item in items]


@app.put("/update_item/{item_id}", response_model=Item)
async def edit_item(item_id: int, item: ItemUpdate):
    updated = update_item(item_id, item.item_name, item.item_description)

    if updated:
        return {
            "item_id": item_id,
            "item_name": item.item_name,
            "item_description": item.item_description
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/delete_item/{item_id}", response_model=dict)
async def delete(item_id: int):
    deleted = delete_item(item_id)

    if deleted:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found to delete")
