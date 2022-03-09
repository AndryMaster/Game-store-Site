from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, number_range

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

# {% if form.resident.data %}
#         {{ form.resident.data }}
#     {% endif %}

# class SelectMultipleField(SelectField):
#     """
#     No different from a normal select field, except this one can take (and
#     validate) multiple choices.  You'll need to specify the HTML `size`
#     attribute to the select field when rendering.
#     """
#     widget = widgets.Select(multiple=True)
#
#     def iter_choices(self):
#         for value, label in self.choices:
#             selected = self.data is not None and self.coerce(value) in self.data
#             yield (value, label, selected)
#
#     def process_data(self, value):
#         try:
#             self.data = list(self.coerce(v) for v in value)
#         except (ValueError, TypeError):
#             self.data = None
#
#     def process_formdata(self, valuelist):
#         try:
#             self.data = list(self.coerce(x) for x in valuelist)
#         except ValueError:
#             raise ValueError(self.gettext('Invalid choice(s): one or more data inputs could not be coerced'))
#
#     def pre_validate(self, form):
#         if self.data:
#             values = list(c[0] for c in self.choices)
#             for d in self.data:
#                 if d not in values:
#                     raise ValueError(self.gettext("'%(value)s' is not a valid choice for this field") % dict(value=d))


class FindForm(FlaskForm):
    keywords = StringField("Ключевые слова", validators=[length(max=32)])
    categories = SelectMultipleField("Категории", choices=[list(elem).reverse() for elem in Categories.items()])
    result_count = IntegerField("Максимальное кол-во результатов (не более 5)",
                                validators=[DataRequired(), number_range(1, 5)], default=3)
    submit = SubmitField('Поиск (фильтровать)')
