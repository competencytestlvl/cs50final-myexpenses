from application.forms import DataForm, ExpensesDataForm, LoginForm, RegistrationForm
from application import create_app, db
from application.item_models import Expenses, User
from flask import flash, render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from itertools import groupby
import json
from operator import itemgetter
from werkzeug.security import check_password_hash, generate_password_hash

# Create instance of app
app = create_app()


@app.route("/")
@login_required
def index():
    """Directs to the main page of the app."""

    current_id = current_user.id
    print(f"Current user: {current_id}")
    # Query transactions from database and return list
    transactions = Expenses.query.order_by(Expenses.date_added.desc()).all()

    transactions2 = Expenses.query.filter_by(user_id=current_id)
    for item in transactions2:
        print(item.amount)

    return render_template("index.html", transactions=transactions)


# -------------ADD INCOME-------------------
@app.route("/add_income", methods=["GET", "POST"])
@login_required
def add_income():
    """Adds new income records into database."""

    # Instance of the data form
    form = DataForm()
    if form.validate_on_submit():
        inputs = Expenses(type=form.type.data,
                          category=form.category.data,
                          amount=form.amount.data,
                          user_id=current_user.id)

        db.session.add(inputs)
        db.session.commit()
        flash('Successfully added income.', category="success")
        return redirect(url_for('index'))
    return render_template('add_income.html', form=form)


# -------------ADD EXPENSES-------------------
@app.route("/add_expenses", methods=["GET", "POST"])
@login_required
def add_expenses():
    """Adds new expenses records into database."""

    # Instance of the expenses form
    expense_form = ExpensesDataForm()
    if expense_form.validate_on_submit():
        expense_inputs = Expenses(type=expense_form.type.data,
                                  category=expense_form.category.data,
                                  amount=expense_form.amount.data,
                                  user_id=current_user.id)
        db.session.add(expense_inputs)
        db.session.commit()
        flash('Successfully added expenses.', category="success")
        return redirect(url_for('index'))
    return render_template('add_expenses.html', form=expense_form)


@app.route('/delete/<int:input_id>')
def delete(input_id):
    """Delete records from database."""

    item_to_delete = Expenses.query.get_or_404(input_id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash("Record deleted", category='success')
        return redirect(url_for('index'))

    except:
        flash("Error occurred while deleting record.", category='error')
        return redirect(url_for('index'))


@app.route('/edit/<int:input_id>', methods=["GET", "POST"])
def edit(input_id):
    """Edit records from database."""

    # Query db for matching id
    item_to_edit = Expenses.query.get_or_404(input_id)
    print(item_to_edit.id)
    # Show form based on transaction type - income
    if item_to_edit.type == "income":
        form = DataForm()
        # For POST request
        if form.validate_on_submit():
            item_to_edit.type = form.type.data
            item_to_edit.amount = form.amount.data
            item_to_edit.category = form.category.data
            # Commit changes to database
            db.session.commit()
            flash("Record has been updated.", category='success')
            return redirect(url_for('index'))

        # For GET request - Form fields inherit the existing income data
        form.type.data = item_to_edit.type
        form.category.data = item_to_edit.category
        form.amount.data = item_to_edit.amount
        return render_template('edit.html', form=form)

    else:
        # Show form based on transaction type - expenses
        form = ExpensesDataForm()
        # For POST request
        if form.validate_on_submit():
            item_to_edit.type = form.type.data
            item_to_edit.amount = form.amount.data
            item_to_edit.category = form.category.data
            # Commit changes to database
            db.session.commit()
            flash("Record has been edited", category='success')
            return redirect(url_for('index'))
        # For GET request - Form inherit the existing expense data
        form.type.data = item_to_edit.type
        form.category.data = item_to_edit.category
        form.amount.data = item_to_edit.amount
        return render_template('edit.html', form=form)


@app.route("/dashboard")
def dashboard():
    """Visualizes Data into interactive charts."""

    # Query the total income and expenses
    value_query = db.func.sum(Expenses.amount)

    # -----------DATA OF INCOME VS EXPENSES------------
    income_expenses = db.session.query(value_query, Expenses.type).group_by(
        Expenses.type).order_by(Expenses.type).all()

    earnings_expenses_list = []
    for grand_total, _ in income_expenses:
        earnings_expenses_list.append(grand_total)
        print(f"{grand_total}, {_}")
    print(f"{earnings_expenses_list}\n")

    # -----------DATA VS CATEGORY------------
    category_comparison = db.session.query(value_query, Expenses.type, Expenses.category).group_by(
        Expenses.category).order_by(Expenses.category).all()
    # INCOME
    income_category_value = []
    income_category = []

    # EXPENSES
    expenses_category_value = []
    expenses_category = []
    for amounts, category_type, description in category_comparison:
        if category_type == "income":
            income_category_value.append(amounts)
            income_category.append(description)
            print(f"{amounts}, {category_type}, {description}")
        else:
            # In case the transaction is an expense
            expenses_category_value.append(amounts)
            expenses_category.append(description)
            print(f"{amounts}, {category_type}, {description}")

    print(income_category)
    print(f"{income_category_value}\n")

    print(expenses_category)
    print(f"{expenses_category_value}\n")

    # -----------DATA OF EXPENDITURE AND INCOME VS TIMELINE------------
    dates_added = db.session.query(value_query,
                                   Expenses.type,
                                   Expenses.date_added).group_by(Expenses.date_added).order_by(
        Expenses.date_added).all()

    date_expenses_list = []
    date_income_list = []
    date_timeline_list = []

    for amount, expense_type, dates in dates_added:
        date_timeline_list.append(dates.strftime("%Y-%m-%d"))

        # To filter expense entries
        if expense_type == 'expense':
            date_expenses_list.append(amount)
            date_income_list.append(0)

        # To filter income entries
        else:
            date_income_list.append(amount)
            date_expenses_list.append(0)

    # Group expense data and labels into dedicated list
    z = zip(date_timeline_list, date_expenses_list)
    r = [(k, sum(int(i[1]) for i in v)) for k, v in groupby(z, key=itemgetter(0))]
    date_expense_labels, expense_values = map(list, zip(*r))

    print(f"{date_expense_labels}")
    print(f"{expense_values}\n")

    # Group income data and labels into dedicated list
    x = zip(date_timeline_list, date_income_list)
    y = [(k, sum(int(j[1]) for j in c)) for k, c in groupby(x, key=itemgetter(0))]
    date_income_labels, income_values = map(list, zip(*y))

    print(f"{date_income_labels}")
    print(income_values)

    # -------- Other data aggregation -----------
    total_income = sum(income_category_value)
    total_expenses = sum(date_expenses_list)
    total_balance = total_income - total_expenses
    average_income = round(sum(income_category_value) / len(income_category_value))

    # -----------EXPORT DATA TO CHART------------
    return render_template('dashboard.html',
                           # Dump json data into empty lists
                           income_expenses=json.dumps(earnings_expenses_list),
                           income_category=json.dumps(income_category),
                           income_category_value=json.dumps(income_category_value),
                           expenses_category=json.dumps(expenses_category),
                           expenses_category_value=json.dumps(expenses_category_value),
                           expense_values=json.dumps(expense_values),
                           date_expense_labels=json.dumps(date_expense_labels),
                           income_values=json.dumps(income_values),
                           total_balance=total_balance,
                           total_expenses=total_expenses,
                           average_income=average_income
                           )


# ----------------------------LOGIN------------------------------------
@app.route('/login', methods=["POST", "GET"])
def login():
    """Login user"""
    form = LoginForm()
    if form.validate_on_submit():
        # Query database for username and validate form submission
        user = User.query.filter_by(username=form.username.data).first()
        # if user exists
        if user:
            # Compare hashed password from submission to database password
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash(f"Logged in successfully as {form.username.data}.", category="success")
                # Return user to the home page
                return redirect(url_for("index"))
            else:
                flash("Incorrect password..please try again", category="error")
        else:
            flash("Username does not exist", category="error")
    return render_template("login.html", form=form)


# ---------------------------LOGOUT-------------------------------
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logs user out of session."""
    logout_user()
    return redirect(url_for('login'))


# ----------------------------REGISTER------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user to database."""

    form = RegistrationForm()
    username = form.username.data
    # POST Request
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            # Create encrypted password
            hashed_password = generate_password_hash(form.password.data, "sha256")
            # Create instance of new user
            user = User(username=username, password=hashed_password)
            print(user.username, user.password)
            db.session.add(user)
            db.session.commit()

        # Clear form fields
        form.username.data = ''
        form.password.data = ''
        flash("User added successfully", category="success")
        # Redirect user to login page upon successful sign up
        return redirect(url_for('login'))
    # GET request
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
