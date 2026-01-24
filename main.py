from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)


from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# No database initialization
# Dummy login entries page (no DB)
@app.get("/logins", response_class=HTMLResponse)
def list_logins(request: Request):
    return templates.TemplateResponse("logins.html", {"request": request, "logins": []})


# Display all users from the database (admin only)
@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request):
    is_admin = request.cookies.get("is_admin")
    if is_admin != "true":
        return HTMLResponse(content="<h3>Access denied. Admins only.</h3>", status_code=403)
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# About page
@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Login page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login with database check and admin session
@app.post("/login")
def login_post(name: str = Form(...), password: str = Form(...), response: Response = None):
    db = SessionLocal()
    user = db.query(User).filter(User.username == name, User.password == password).first()
    db.close()
    if user:
        # Only admin with correct password can see users section
        if name == "admin" and password == "admin123":
            resp = RedirectResponse(url="/login-thankyou", status_code=303)
            resp.set_cookie(key="is_admin", value="true", httponly=True)
            return resp
        else:
            resp = RedirectResponse(url="/login-thankyou", status_code=303)
            resp.delete_cookie(key="is_admin")
            return resp
    else:
        return HTMLResponse(content="<h3>Invalid username or password.</h3>", status_code=401)

# Thank you page after login
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

# Registration form submission (DB)
@app.post("/register")
def register_submit(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        db.close()
        return HTMLResponse(content="<h3>User already exists. Please try a different username or email.</h3>", status_code=400)
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    return RedirectResponse(url=f"/register-thankyou?username={username}&email={email}", status_code=303)
@app.get("/login-thankyou", response_class=HTMLResponse)
def login_thankyou(request: Request):
    return templates.TemplateResponse("login_thankyou.html", {"request": request})


# Registration thank you page
@app.get("/register-thankyou", response_class=HTMLResponse)
def register_thankyou(request: Request, username: str, email: str):
    return templates.TemplateResponse("thankyou.html", {"request": request, "name": username, "email": email})
# Welcome page
@app.get("/", response_class=HTMLResponse)
def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

# Form submission and thank you (no DB)
@app.post("/submit")
def submit_form(name: str = Form(...), email: str = Form(...), number: str = Form(...)):
    return RedirectResponse(url=f"/thanks?name={name}&email={email}", status_code=303)

# Thank you page after form submission
@app.get("/thanks", response_class=HTMLResponse)
def thanks_page(request: Request, name: str, email: str):
    return templates.TemplateResponse("thankyou.html", {"request": request, "name": name, "email": email})
# Dummy user entries page (no DB)
@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": []})






