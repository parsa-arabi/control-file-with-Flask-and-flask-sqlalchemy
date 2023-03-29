import requests.cookies

from database import *

db.create_all()

path = "./static/Files/"
path2 = "./static/imgs/"

# admin23 = files(name="username", filename="password")
# db.session.add(admin23)
# db.session.commit()

# admin2 = user(username="1", password="1")
# db.session.add(admin2)
# db.session.commit()

@app.route("/")
def index():
    if request.cookies.get("cookie"):
        return redirect("/files")
    else:
        return render_template("index.html")

@app.route("/files")
def get_files():
    if request.cookies.get("cookie"):
        return render_template("file_page.html", name=request.cookies.get("cookie"), num=len(files.query.all()), filename=files.query.all())
    else:
        return redirect("/")

@app.route("/log_out")
def log_out():
    flash("شما از حساب کاربری خود خارج شدید", "danger")
    resp = make_response(redirect("/"))
    resp.delete_cookie("cookie")
    return resp

@app.route("/sign_in")
def sign_in():
    if request.cookies.get("cookie"):
        flash("شما در حساب کاربری خود وارد هستید", "warning")
        return render_template("login.html", name=request.cookies.get("cookie"))
    else:
        return render_template("login.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        for i in range(len(user.query.all())):
            if user.query.all()[i].username == username and user.query.all()[i].password == password:
                flash("وارد شدید", "success")
                resp = make_response(redirect("/"))
                resp.set_cookie("cookie", username)
                return resp
        else:
            flash("رمز یا نام کاربری درست نیست", "danger")
            return redirect("/sign_in")

@app.route("/sign_up")
def sign_up():
    if request.cookies.get("cookie"):
        flash("شما در حساب کاربری خود وارد هستید", "warning")
        return render_template("register.html", name=request.cookies.get("cookie"))
    else:
        return render_template("register.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        img = request.files.get("img")
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        if password == re_password:
            if len(password) < 8 or len(username) < 8:
                flash("ثبت نشد نام کاربری و رمز باید بیشتر از 8 رقم باشند", "warning")
                return redirect("/sign_up")
            for i in range(len(user.query.all())):
                if user.query.all()[i].username == username or user.query.all()[i].password == password:
                    flash("ثبت نشد. این نام کاربری یا رمز عبور را قبلا کسی ثبت کرده", "warning")
                    return redirect("/sign_up")
            else:
                if img:
                    img.save(os.path.join(path2, username + ".jpg"))
                    admin = user(username=username, password=password)
                    db.session.add(admin)
                    db.session.commit()
                    flash("ثبت نام کامل شد", "success")
                    resp = make_response(redirect("/files"))
                    resp.set_cookie("cookie", username)
                    return resp
                else:
                    admin2 = user(username=username, password=password)
                    db.session.add(admin2)
                    db.session.commit()
                    flash("ثبت نام کامل شد", "success")
                    resp = make_response(redirect("/files"))
                    resp.set_cookie("cookie", username)
                    return resp
        else:
            flash("ثبت نشد رمز ها یکی نیستند", "warning")
            return redirect("/sign_up")

@app.route("/new")
def new():
    if request.cookies.get("cookie"):
        flash("در صورت طول کشیدن آپلود شدن فایل آپلودی ، فایل شما سنگین است . نگران نباشید", "info")
        return render_template("new_file.html", name=request.cookies.get("cookie"))
    else:
        flash("برای اضافه کردن فایل شما باید وارد شوید", "warning")
        return redirect("/sign_in")

@app.route("/new_file", methods=['POST', 'GET'])
def new_file():
    if request.method == 'POST':
        file = request.files.get("file")
        if file:
            file.save(os.path.join(path,  "(" + request.cookies.get("cookie") + ")" + file.filename))
            admin = files(filename=file.filename, url="(" + request.cookies.get("cookie") + ")" + file.filename, author=user.query.filter_by(username=request.cookies.get("cookie")).first())
            db.session.add(admin)
            db.session.commit()
            flash("ذخیره شد", "success")
        else:
            flash("ذخیره نشد", "danger")
        return redirect("/")

@app.route("/delete/<int:post_id><string:url>",methods=['POST','GET'])
def delete(post_id, url):
    if request.cookies.get("cookie"):
         file = files.query.get(post_id)
         db.session.delete(file)
         db.session.commit()
         os.remove('./static/Files/' + url)
         flash("پاک شد", "success")
         return redirect("/")
    else:
        flash("شما اول باید وارد شوید", "warning")
        return redirect('/sign_in')

@app.route("/profile")
def profile():
    if request.cookies.get("cookie"):
        for i in range(len(user.query.all())):
            if user.query.all()[i].username == request.cookies.get("cookie"):
                return render_template("profile.html", name=request.cookies.get("cookie"), data=user.query.all()[i])
    else:
        flash("ابتدا باید وارد شوید", "warning")
        return redirect("/")

@app.route("/new_profile", methods=["POST", "GET"])
def editp():
    if request.cookies.get("cookie"):
        if request.method == "POST":
            img = request.files.get("file")
            username = request.form.get("username")
            passwords = request.form.get("password")
            re_password = request.form.get("re_password")
            user2 = user.query.filter_by(username=request.cookies.get("cookie")).first()
            if passwords == re_password:
                user2.password = passwords
                user2.username = username
                if img:
                    img.save(os.path.join(path2, username + ".jpg"))
                if not img:
                    print("salam")
                    os.rename("./static/imgs/" + str(request.cookies.get("cookie")) + ".jpg", path2 + str(username) + ".jpg")
                db.session.commit()
                flash("تغیرات اعمال شد!", "success")
                response = make_response(redirect("/"))
                response.set_cookie("cookie", username)
                return response
        else:
            flash("رمز ها یکی نیستند!", "danger")
            return redirect("/prof")
    else:
        flash("ابتدا باید وارد شوید!", "warning")
        return redirect("/login")


@app.errorhandler(404)
def not_found_error(error):
    if request.cookies.get("cookie"):
        return render_template("404.html", name=request.cookies.get("cookie")), 404
    else:
        return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    if request.cookies.get("cookie"):
        return render_template('500.html', name=request.cookies.get("cookie")), 500
    else:
        return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=24555)