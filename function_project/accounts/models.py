from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager

# Create your models here.
# モデルを用いる時は。テーブルの定義をするクラスとテーブルデータの挿入、取り出しをするクラスと分けることもできる。

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    # Falseはログイン不可
    is_active = models.BooleanField(default=False)
    # Falseは管理者権限無し
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'


# テーブルのデータを定義するクラス  
# クラスは models.Manager として継承する 

class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now() 
        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()

    

class UserActivateTokens(models.Model):

    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey('Users', on_delete=models.CASCADE)

    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_activate_tokens'
    
#　デコレータ関数　関数オブジェクトを引数にとって引数にとった関数に実行時に変更を加える 

# Userが作成されたときに自動で実行される。
# sebderで指定したクラスのオブジェクトが呼び出される
# 引数 sender=User でUserクラスのインスタンスを取得している

# Userが新しく追加されるたびに、下の関数が実行される post_saveは新しく着かされたときに実行する設定する関数

@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    print(str(uuid4))
    print(datetime.now() + timedelta(days=1))
    # UserActivateTokens関数を実行してトークンを作成。
    user_activate_token = UserActivateTokens.objects.create(
        # expired_atは源氏時刻化来日後を指定して、これは期限として扱う
        user=instance, token=str(uuid4()), expired_at=datetime.now() + timedelta(days=1)
    )
    # 本来はメール機能を作ってURLを送る方がよい
    print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')





