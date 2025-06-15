もしこのプロジェクトをgit cloneしてFastAPIの部分に加えるものがあるのなら、git clone後にbackendディレクトリに移動、\n
そこでpython3 -m venv venv と　venv\Scripts\activate.bat を実行して仮想環境を構築、起動\n
そしてpip install -r requirements.txtコマンドを打ち込んで必要なパッケージをインストール\n
もし別のパッケージを入れたならpip freeze > requirements.txtをしてrequirements.txtにパッケージの記述をすることを忘れずに。\n
また、git add　や git commit , git push　する際はvenvディレクトリに記述されたパッケージの情報を入れずに\n
requirements.txtとその他変更があったファイルのみをgithubにアップをお願いします！


