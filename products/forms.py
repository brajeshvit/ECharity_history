from django import forms

from products.models import Product, ProductImage
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

class PostForm(forms.ModelForm):

    class Meta:
        model = Product 
        fields = ('user', 'title', 'description', 'price', 'active', 'quantity','address', 'zip_Code', 'date_created', 'date_Update', 'expire_date', )


     
        
class ImageForm(forms.ModelForm):
    image_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
    )
    delete_image = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = ProductImage
        fields = ["title", "image"]

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _(""),
                
                layout.HTML(u"""{% load i18n %}
                    <div id="image_upload_widget">
                        <div class="preview">
                         {% load staticfiles %}
                            {% if instance.image %}
                                <img src="{% static instance.image %}" alt="title" />
                            {% endif %}
                        </div>
                        <div class="uploader">
                            <noscript>
                                <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                            </noscript>
                        </div>
                        <p class="help_text" class="help-block">{% trans "" %}</p>
                        <div class="messages"></div>
                    </div>
                """),
                "image_path",
                "delete_image",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Save'), css_class="btn btn-primary"),
            )
        )
