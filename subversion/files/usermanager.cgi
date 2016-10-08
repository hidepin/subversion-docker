#!/usr/bin/env python
# coding: utf-8

import cgi
import fcntl
import subprocess
import re

htpasswd_cmd = '/usr/bin/htpasswd'
htpasswd_file = '/opt/svn/settings/htpasswd'
htpasswd_lock = '/opt/svn/settings/htpasswd.lock'

html = '''Content-Type: text/html

<html>
<head>
  <title>svn user management</title>
</head>
<body>
<h1>Subversion ユーザの管理</h1>
<br>
<b>%s</b><br>
※ ユーザ名には、英数字と「-_.」が使用可能です。(「-_.」は２文字目以降に使用できます。)<br>
<br>

<form action="" method="POST">
ユーザ名: <input type="text" name="username" value="" size="20"><br>
元のパスワード: <input type="password" name="org_passwd" value="" size="20"><br>
新しいパスワード: <input type="password" name="new_passwd" value="" size="20"><br>
<input type="submit" value="送信">
</form>
</body>
</html>
'''

# ユーザ名は、先頭英数字のみ２文字目以降「-_.」を加えて許容する
def allowed_username(username):
    regexp = re.compile(r'^[0-9A-Za-z][-_.0-9A-Za-z]*$')
    result = regexp.search(username)
    if result != None :
        return True
    return False

# パスワードは、asciiのうち表示可能な「\x21からx7E」を許容する
def allowed_passwd(passwd):
    regexp = re.compile(r'^[\x21-\x7E]+$')
    result = regexp.search(passwd)
    if result != None :
        return True
    return False

# username/org_passwd/new_passwdに使用不可能な文字が含まれていないか？
# org_passwd/new_passwdが同じパスワードでないかを確認する
# 文字が入力されていないinput欄はチェック対象外とする
def check_input(username, org_passwd, new_passwd):
    if username and not allowed_username(username) \
       or  org_passwd and not allowed_passwd(org_passwd) \
       or  new_passwd and not allowed_passwd(new_passwd):
        return True

    return False

# htpasswdのパスワード確認機能を使用して、その実行結果の標準エラーを返します。
def verify_passwd(username, password):
    proc = subprocess.Popen(['htpasswd', '-bv', htpasswd_file, username, password],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout_data, stderr_data = proc.communicate()

    return stderr_data

# htpasswdのパスワード登録、更新機能を使用して、その実行結果のコード値を返します。
# 0    : 成功
# 0以外: 失敗
def update_passwd(username, password):
    proc = subprocess.Popen(['htpasswd', '-b', htpasswd_file, username, password],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout_data, stderr_data = proc.communicate()

    return proc.returncode == 0

# ユーザを作成する
def create_user(username, new_passwd):
    with open(htpasswd_lock) as flock:
        try:
            fcntl.flock(flock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except Exception as e:
            return e.message + "他のユーザが処理中です。しばらくたって、やり直してください。"

        try:
            if 'not found' in verify_passwd(username, ''):
                if update_passwd(username, new_passwd):
                    return username + 'を作成しました。'
                else:
                    return username + 'の作成に失敗しました。'
            else:
                return username + 'は作成できませんでした。(すでに作成済みでないか確認してください)'
        finally:
            fcntl.flock(flock, fcntl.LOCK_UN)

# ユーザのパスワードを変更する
def update_user(username, org_passwd, new_passwd):
    with open(htpasswd_lock) as flock:
        try:
            fcntl.flock(flock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
            return "他のユーザが処理中です。しばらくたって、やり直してください。"

        try:
            if 'correct' in verify_passwd(username, org_passwd):
                if update_passwd(username, new_passwd):
                    return username + 'のパスワードを更新しました。'
                else:
                    return username + 'のパスワードを更新に失敗しました。'
            else:
                return username + 'のパスワードは更新できませんでした。(ユーザ名とパスワードの組み合わせを確認してください)'
        finally:
            fcntl.flock(flock, fcntl.LOCK_UN)

form = cgi.FieldStorage()
username = form.getvalue('username', '')
org_passwd = form.getvalue('org_passwd', '')
new_passwd = form.getvalue('new_passwd', '')

msg = 'ユーザ名と新しいパスワードを入力してください。(変更の場合は元のパスワードも入力してください)'
if check_input(username, org_passwd, new_passwd):
    # 入力文字に許容されない文字がある場合の処理
    msg = 'ユーザ名、パスワードに使用できない文字が含まれているか、新しいパスワードと、元のパスワードが同じです。'
elif username and org_passwd and new_passwd:
    # パスワードを変更する処理
    msg = update_user(username, org_passwd, new_passwd)
elif username and not org_passwd and new_passwd:
    # ユーザを作成する処理
    msg = create_user(username, new_passwd)

print html % cgi.escape(msg)
