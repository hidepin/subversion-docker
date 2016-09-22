subversion-docker
============================================================

初期設定
============================================================

1. 作成したいリポジトリ名称をdocker-compose.xmlで環境変数に指定する。
   (samplerepoとする場合。なお、repoは必須)

    ```
    version: '2'

    services:
      subversion:
        environment:
          - REPOS=sample
    ```

    複数指定したい場合は、 **:** で区切る

2. imageを作成する

    ```
    docker-compose build
    ```

3. 起動する

    ```
    docker-compose up -d
    ```

4. ユーザを作成する

    ```
    docker exec -it subversiondocker_subversion_1 htpasswd /opt/svn/settings/htpasswd (ユーザ名)
    ```

5. (Optional)アクセス制御をかける


    ```
    vi /opt/docker/subversion/volumes/subversion/opt/svn/settings/authz
    ```

(Optional) コミット時のチェック
============================================================

コミット時に下記のチェックを行う場合の設定

- 2MBを超えるファイルは、commitメッセージに「force」が含まれていないとコミットできない。
- 10MBを超えるファイルは、コミットできない。
- 圧縮ファイル、isoファイル等バイナリファイルと考えられる拡張子のファイルは、commitメッセージに「force」が含まれていないとコミットできない。
- r00など、拡張子の前にrev名をつけているファイルは、commitメッセージに「force」が含まれていないとコミットできない。
- 4桁以上の数字がファイル名に含まれているファイルは、commitメッセージに「date」or 「force」が含まれていないとコミットできない。

1. tmplとして配置シテイルファイルをリネーム

    ```
    cd /opt/docker/subversion/volumes/subversion/opt/svn/(リポジトリ名)/hooks/
    mv pre-commit.size_format_check.tmpl pre-commit
    ```

2. パーミッションを設定
    ```
    cd /opt/docker/subversion/volumes/subversion/opt/svn/(リポジトリ名)/hooks/
    chmod +x pre-commit
    ```
