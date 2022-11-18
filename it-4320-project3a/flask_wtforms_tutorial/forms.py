"""Form class declaration."""
import json
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length

class StockForm(FlaskForm):
    """Generate Your Graph."""

    # This will hold the symbols from the imported NYSE data 
    stock_choices = [
        # Default from Alpha Vantage, IBM is already present in the given JSON file 
        ("GOOGL", "GOOGL"),
    ]
    stockFile = open("nyse-listed.json")
    data = json.load(stockFile)
    keystring = "ACT Symbol"
    for value in data:
        # Pull the symbol from each entry 
        new_choice = (value[keystring], value[keystring])
        stock_choices.append(new_choice)
    
    symbol = SelectField("Choose Stock Symbol",[DataRequired()],
        choices=stock_choices
    )

    chart_type = SelectField("Select Chart Type",[DataRequired()],
        choices=[
            ("1", "1. Bar"),
            ("2", "2. Line"),
        ],
    )

    time_series = SelectField("Select Time Series",[DataRequired()],
        choices=[
            ("1", "1. Intraday"),
            ("2", "2. Daily"),
            ("3", "3. Weekly"),
            ("4", "4. Monthly"),
        ],
    )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")



