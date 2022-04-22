from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Users
        fields = ['username','age', 'email', 'password']

    # パスワードが正しいか確かめる関数  クリーンデータを使う 
    # super()は親クラスのメソッドを呼び出したいときに使う。
    # 今回はRegisterFormクラスて定義したメソッドがそれにあたる。
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    # パスワードをセーブするメソッド。views.pyで呼び出される。
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)  # passwordのバリーデーション
        user.set_password(self.cleaned_data['password'])        # passwordの暗号化
        user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

class UserEditForm(forms.ModelForm):
    username = forms.CharField(label="名前")
    age = forms.IntegerField(label="年齢",min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)

    # model = Postで仕様モデルを定義します。
    # fields = ('name', 'text', 'file')で実際にフォームで使用する項目を選択。
    # dateは投稿者に選択させるのではなく現在時刻を自動入力してくれればいいのではずしています。
    # goodを含んでしまうとgoodボタンを押さないと投稿できなくなるので外しています。
    # いいねボタンって普通投稿フォームと独立してるでしょ？
    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture')

class PasswordChangeForm(forms.ModelForm):

    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Users
        fields = ('password', )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    # パスワードをセーブするメソッド。views.pyで呼び出される。
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)  # passwordのバリーデーション
        user.set_password(self.cleaned_data['password'])        # passwordの暗号化
        user.save()
        return user