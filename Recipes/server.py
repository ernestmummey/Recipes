from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import redirect
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt        
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)

Email_Regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
pword = re.compile(r"^(?=.*[a-z])(?=.*[A-Z]){8,20}$")
#(r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]){8,20}$")
name = re.compile(r"^[a-zA-Z-']{2,40}$")


app.secret_key = "secret key"

@app.route("/")
def home():
    return render_template("registration.html")


@app.route("/form", methods=["POST"])
def reg_form():
    is_valid = True
    if not name.match(request.form["first_name"]):
        is_valid = False
        flash("Please provide a valid first name")

    if not name.match(request.form["last_name"]):
        is_valid = False  
        flash("Please provide a valid last name")

    if not Email_Regex.match(request.form['e-mail']):
        is_valid = False         
        flash("Email is not valid!")
    
    if not pword.match(request.form['Password']):
        is_valid = False
        flash("Provide password with: 1 lowercase : 1 uppercase:")

    if not request.form['Password']==request.form['confirm_password']: 
        is_valid = False       
        flash("Passwords do not match")

    if not is_valid:
        return redirect("/")
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['Password'])
        query = "INSERT INTO users (`first_name`, `last_name`, `email`,`password`) VALUES (%(fname)s, %(lname)s, %(Email)s, %(pword)s);"
        data = {
                'fname':request.form["first_name"],
                'lname':request.form["last_name"],
                'Email':request.form['e-mail'],
                'pword': pw_hash
        }
        mysql = connectToMySQL('recipes_schema')
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id
        print(user_id)
        flash("Your registration form was successful")
        return redirect("/recipes")


@app.route("/login", methods=["POST"])
def login_form():
    query = "SELECT * FROM users WHERE email = %(username)s;"
    data = { "username" : request.form["Email"] }
    mysql = connectToMySQL("recipes_schema")
    Email = mysql.query_db(query, data)
    print(Email)
    if len(Email) > 0:
        if bcrypt.check_password_hash(Email[0]['password'],request.form['pword']):
            session['user_id'] = Email[0]['id']
            return redirect('/recipes')
    flash("You could not be logged in")
    return redirect("/")

# --------------------------------Get Request---------------------------------

@app.route("/recipes")
def homepage():
    if 'user_id' not in session:
        flash("You are not logged in")
        return redirect('/')

    query = "SELECT * FROM recipes_schema.users  WHERE id = %(id)s;"
    data = { 
        "id" : session["user_id"]
    }
    mysql = connectToMySQL("recipes_schema")
    user = mysql.query_db(query, data)
    

    query = "SELECT recipes.id, users.first_name, recipes.name, recipes.minutes FROM recipes_schema.recipes JOIN users ON recipes.user_id = users.id WHERE recipes.user_id = %(id)s;"
    data = { 
        "id" : session["user_id"]
    }
    mysql = connectToMySQL("recipes_schema")
    recipe = mysql.query_db(query, data)
    return render_template("dashboard.html", recipes_name = recipe, new_user = user[0] )

@app.route("/recipes/new")
def add_recipe():
    return render_template('add_recipe.html')


@app.route("/recipes/<int:id>/edit")
def recipe_edit(id):
    query = "SELECT recipes.id, recipes.description, recipes.instructions, recipes.name, recipes.minutes FROM recipes_schema.recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
    data = {
        'id':id
    }
    mysql = connectToMySQL('recipes_schema')
    edits = mysql.query_db(query, data)
    session['recipe_id'] = id
    return render_template("edit_recipe.html", form = edits)


@app.route("/recipes/<id>")
def show_page(id):
    query = "SELECT * FROM recipes_schema.recipes WHERE recipes.id = %(id)s;"
    data = {
        'id':id
    }
    mysql = connectToMySQL('recipes_schema')
    show = mysql.query_db(query, data)
    print(show)
    return render_template("show_recipe.html", show_recipe = show)



@app.route("/logout")
def delete():
    session.clear()
    return redirect("/")

@app.route("/delete/<id>")
def destroy_mess(id):
    query = ('DELETE FROM recipes WHERE id = %(recipe_id)s;')
    data = {
        'recipe_id' : id
    }
    mysql = connectToMySQL('recipes_schema')
    mysql.query_db(query, data)
    return redirect('/recipes')

# --------------------------------Post Request--------------------------------


@app.route("/recipes/add", methods=["POST"])
def new_recipe():
    if 'user_id' not in session:
        flash("You are not logged in")
        return redirect('/')

    is_valid = True
    if len(request.form["recipe_name"]) < 3:
        is_valid = False
        flash("Please provide at least 3 characters")
        

    if len(request.form["recipe_descrip"]) < 3:
        is_valid = False
        flash("Please provide at least 3 characters")
        

    if len(request.form["recipe_instruct"]) < 3:
        is_valid = False
        flash("Please provide at least 3 characters")
        

    if not is_valid:
        return redirect("/recipes/new")
    else:
        query = "INSERT INTO recipes (`user_id`,`name`, `description`, `minutes`,`instructions`) VALUES (%(id)s,%(r_name)s, %(r_desc)s, %(radio)s, %(r_inst)s);"
        data = {
                'id': session["user_id"],
                'r_name':request.form["recipe_name"],
                'r_desc':request.form["recipe_descrip"],
                'radio': request.form['yes_no'],
                'r_inst':request.form['recipe_instruct']
        }
        mysql = connectToMySQL('recipes_schema')
        mysql.query_db(query, data)
    return redirect("/recipes" )
    
    
@app.route("/recipe/edit", methods=["POST"])
def edit_recipe():
    if 'user_id' not in session:
        flash("You are not logged in")
        return redirect('/')

    is_valid = True
    if len(request.form["r_name"]) < 3:
        is_valid = False
        flash("Please provide at least 3 characters")
        

    if len(request.form["r_descrip"]) < 3:
        is_valid = False
        flash("Please provide at least 3 characters")
        

    if len(request.form["r_instruct"]) < 3:
        is_valid = False
        flash("Please provide at least 3 characters")
        

    if not is_valid:
        return redirect(f"/recipes/{session['recipe_id']/edit")
    else:
        query = "UPDATE recipes SET `name` = %(rname)s, `description` = %(rdesc)s, `minutes` = %(radio)s, `instructions`= %(rinst)s WHERE id = %(id)s;"
        data = {
                'id': session["user_id"],
                'rname':request.form["r_name"],
                'rdesc':request.form["r_descrip"],
                'radio': request.form['yes_no'],
                'rinst':request.form['r_instruct']
        }
        mysql = connectToMySQL('recipes_schema')
        mysql.query_db(query, data)
        return redirect("/recipes")





if __name__ == "__main__":
    app.run(debug=True)