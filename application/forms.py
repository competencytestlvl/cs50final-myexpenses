from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length


class DataForm(FlaskForm):
    type = SelectField(label='Type',
                       validators=[DataRequired()],
                       choices=[('income', 'income'),
                                ])

    category = SelectField(label='Category', validators=[DataRequired()],
                           choices=[
                                    ('salary', 'salary'),
                                    ('investment', 'investment'),
                                    ('other income', 'other income')
                                    ])

    amount = IntegerField("Amount", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExpensesDataForm(FlaskForm):
    type = SelectField(label='Type',
                       validators=[DataRequired()],
                       choices=[
                                ('expense', 'expense')
                                ])

    category = SelectField(label='Category', validators=[DataRequired()],
                           choices=[
                                    ('rent', 'rent'),
                                    ('bills', 'bills'),
                                    ('other expenses', 'other expenses')
                                    ])

    amount = IntegerField("Amount", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=4, max=30), InputRequired()],
                           render_kw={"placeholder": "Your username"})
    password = PasswordField(label='Password', validators=[Length(min=4, max=30), InputRequired(),
                                                           EqualTo('confirmation', message="Password needs to match")],
                             render_kw={"placeholder": "Your password"})
    confirmation = PasswordField(label='Confirmation Password', validators=[Length(min=4, max=30), InputRequired()],
                                 render_kw={"placeholder": "Your confirmation password"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=4, max=60), InputRequired()],
                           render_kw={"placeholder": "Your username"})
    password = PasswordField(label='Password', validators=[Length(min=4, max=60), InputRequired()],
                             render_kw={"placeholder": "Your password"})
    confirmation = PasswordField(label='Confirmation Password',
                                 validators=[Length(min=4, max=60),
                                             InputRequired(),
                                             EqualTo('password', message="Password needs to match")],
                                 render_kw={"placeholder": "Your confirmation Password"})
    submit = SubmitField("Login")