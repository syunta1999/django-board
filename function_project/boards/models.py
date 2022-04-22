from django.db import models
from django.db.models import Count
from datetime import datetime

# Create your models here.
# モデルを用いる時は。テーブルの定義をするクラスとテーブルデータの挿入、取り出しをするクラスと分けることもできる。



# テーブルデータの挿入、取り出しをするクラス
# 掲示板のテーマ一覧を取得する
class ThemesManeger(models.Manager):

    def fetch_all_themes(self):
        return self.order_by('id').all()
    # コメントの多い順に上から表示する
    

# テーブルの定義をするクラス
# 掲示板のテーマ
class Themes(models.Model):

    title = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    
    # ThemesManegerクラスをオブジェクト化することで他のクラス内で使える使えるようにしている 
    objects = ThemesManeger()

    class Meta:
        db_table = 'themes'



# テーブルデータの挿入、取り出しをするクラス
# 掲示板のテーマに書かれたコメントを取得する。
class CommentsManeger(models.Manager):
    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()

# テーブルの定義をするクラス
# 掲示板のコメント  
class Comments(models.Model):

    comment = models.CharField(max_length=100)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    theme = models.ForeignKey('Themes', on_delete=models.CASCADE)

    objects = CommentsManeger()

    class Meta:
        db_table = 'comments'

