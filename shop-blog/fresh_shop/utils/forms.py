from django import forms

from goods.models import Goods


class SearchForm(forms.Form):
    searchgoods = forms.CharField(required=True, min_length=1, error_messages={'required': '请输入有效的商品名字', 'min_length': '最少输入一个字符'})

    def clean(self):
        searchgoods = self.cleaned_data['searchgoods']
        goods = Goods.objects.filter(name__contains=searchgoods).first()
        if goods:
            return self.cleaned_data
        else:
            raise forms.ValidationError({'searchgoods': '对不起，暂时还没有相关商品'})