from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, length

from wtforms.widgets import ListWidget, CheckboxInput
from pharse import Categories


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


# class BrifStoreForm(Form):
#     choices = [(1, 'one'),
#                (2, 'two'),
#                (3, 'tree')]
#     resident = MultiCheckboxField('Label', choices=choices, coerce=int)


class FindForm(FlaskForm):
    keywords = StringField("Ключевые слова", validators=[length(max=32)])
    categories = SelectMultipleField("Категории", choices=[list(elem).reverse() for elem in Categories.items()])
    result_count = IntegerField("Максимальное кол-во результатов (не более 5)",
                                validators=[DataRequired(), length(min=1, max=5)], default=1)
    submit = SubmitField('Поиск (фильтровать)')
