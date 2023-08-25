import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, EmailStr

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates("./templates")


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class UserBillet(BaseModel):
    name: str
    email: EmailStr
    password: str


users = []


@app.get("/", response_class=HTMLResponse)
@app.get("/main", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def get_all_users(request: Request):
    print(users)
    context = {
        "request": request,
        "title": "List of users",
        "users_list": [
            {
                "user_name": user.name,
                "user_email": user.email,
            }
            for user in users
        ],
    }
    return templates.TemplateResponse("users_table.html", context)


@app.get("/add_user", response_class=HTMLResponse)
async def user_add_form(request: Request):
    context = {
        "request": request,
        "title": "Add user"
    }
    return templates.TemplateResponse("add_user_form.html", context)


@app.post("/register")
async def post_data(user_name=Form(), user_email=Form(), user_passwd=Form()):
    new_id = 1
    if users:
        new_id = max(users, key=lambda u: u.id).id + 1
    users.append(
        User(
            id=new_id,
            name=user_name,
            email=user_email,
            password=user_passwd
        )
    )
    return RedirectResponse(url="/", status_code=303)


if __name__ == "__main__":
    uvicorn.run(
        "task06:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
    