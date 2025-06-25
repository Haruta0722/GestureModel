もしこのプロジェクトをgit cloneしてFastAPIの部分に加えるものがあるのなら、git clone後にbackendディレクトリに移動  
そこでpython3 -m venv venv と　venv\Scripts\activate.bat を実行して仮想環境を構築、起動  
そしてpip install -r requirements.txtコマンドを打ち込んで必要なパッケージをインストール  
もし別のパッケージを入れたならpip freeze > requirements.txtをしてrequirements.txtにパッケージの記述をすることを忘れずに。  
また、git add　や git commit , git push　する際はvenvディレクトリに記述されたパッケージの情報を入れずに  
requirements.txtとその他変更があったファイルのみをgithubにアップをお願いします！

後はfrontendに移動した後、npm installを実行することをお願いします。  
特にmediapipeをインストールする必要はないっす。
