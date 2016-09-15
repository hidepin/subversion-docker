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

   新規htpasswd作成時のみ **-c** をつける
   
    ```
    docker exec -it subversiondocker_subversion_1 htpasswd [-c] /opt/svn/settings/htpasswd (ユーザ名)
    ```

5. (Optional)アクセス制御をかける


    ```
    vi /opt/docker/subversion/volumes/subversion/opt/svn/settings/authz
    ```
