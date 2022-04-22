from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Comments, Themes
from . import forms
from django.contrib import messages
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(
        request, 'boards/home.html'
    )

# タイトルを作成する関数
def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form.is_valid():
        # request.userでリクエストしてきたユーザーを取得し
        # instance.user にログイン情報を渡して  フォームをだれが作ったか保存できるようにする。
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        messages.success(request,'掲示板を作成しました')
        return redirect('boards:list_themes')

    return render(request, 'boards/create_theme.html', context={'create_theme_form': create_theme_form})

# タイトル一覧を表示する関数
def list_themes(request):
    themes = Themes.objects.fetch_all_themes()
    return render(request, 'boards/list_themes.html', context={'themes': themes})

# タイトルを編集する関数
def edit_theme(request, id):
    # get_object_or_404：編集しようとしているthemeとthemeのidを取得する(HTMLから送られてくる)
    theme = get_object_or_404(Themes, id=id)
    # 編集しようとしているユーザーとthmemeのIDが同じか確かめて違うなら404を発生させる。
    if theme.user.id != request.user.id:
        raise Http404                                   # instance=theme : 上で定義したthemeをインスタンスとして取得することができる
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request,'掲示板を更新しました')
        return redirect('boards:list_themes')
    return render(request, 'boards/edit_theme.html', context={'edit_theme_form':edit_theme_form, 'id':id})

# タイトルを削除する関数
def delete_theme(request, id):
    # get_object_or_404：編集しようとしているthemeとthemeのidを取得する(HTMLから送られてくる)
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    # 削除しようとしているthemeを表示、削除する                 instance=theme : 上で定義したthemeをインスタンスとして取得することができる
    delete_theme_form = forms.DeleteThemeForm(request.POST or None, instance=theme)
    if delete_theme_form.is_valid(): # csrf check
        theme.delete()
        messages.success(request,'掲示板を削除しました')
        return redirect('boards:list_themes')
    return render(request, 'boards/delete_theme.html', context={'delete_theme_form': delete_theme_form,})

# コメントを取得する
def post_comments(request, theme_id):
    saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
    post_comment_form = forms.PostCommentForm(request.POST or None, initial={'comment': saved_comment})
    # テーマに対して送られたコメントを全て取得する。
    comments = Comments.objects.fetch_by_theme_id(theme_id)
    # 保存する時にどのテーマに対するコメントなのか、どのユーザーのコメントなのか分かるようにする
    theme = get_object_or_404(Themes, id=theme_id)
    if post_comment_form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        # フォームのthemeインスタンスにtheme情報を入れる
        post_comment_form.instance.theme = theme
        # フォームのuserインスタンスにログインしているユーザー情報を入れる
        post_comment_form.instance.user = request.user
        post_comment_form.save()
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
        return redirect('boards:post_comments', theme_id=theme_id)
    return render(request, 'boards/post_comments.html', context={
        'post_comment_form': post_comment_form, 'theme': theme, 'comments': comments
        }
    )

# コメントを一時保存する
def save_comment(request):
    if request.is_ajax:
        comment = request.GET.get('comment')
        theme_id = request.GET.get('theme_id')
        if comment and theme_id:
            cache.set(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', comment)
            return JsonResponse({'message': '一時保存しました'})


