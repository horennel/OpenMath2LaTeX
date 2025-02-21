# OpenMath2LaTeX

## 一个基于openai api的数学公式ORC识别的macOS菜单栏应用程序

### 该应用程序仅适用于macOS⚠️

### 效果图

![menubar_off.jpg](assets%2Fmenubar_off.jpg)
![menubar_on.jpg](assets%2Fmenubar_on.jpg)
![history.jpg](assets%2Fhistory.jpg)
![settings.jpg](assets%2Fsettings.jpg)

### 如何构建和安装

- 克隆库

```angular2html
git clone https://github.com/horennel/OpenMath2LaTeX.git
```

- 不要使用conda的虚拟环境来构建该应用程序⚠️
- 在项目里创建虚拟环境和进入虚拟环境

```angular2html
cd OpenMath2LaTeX
python3 -m venv env
source env/bin/activate
```

- 安装依赖环境

```angular2html
pip3 install -r requirements.txt
```

- 打包应用程序

```angular2html
python3 setup.py py2app
```

- 将dist中的OpenMath2LaTeX.app移动到应用程序文件夹即可


- 具体可以查看py2app的文档

### 如何使用

- 权限（⚠️重要）
    - 进入macOS的设置-> 隐私与安全性-> 输入监控
    - 添加OpenMath2LaTeX.app并打开权限
    - 如果执行过重复安装⚠️，请先在输入监控中删除（-）OpenMath2LaTeX.app，再添加（+）OpenMath2LaTeX.app
- 通知
    - 进入macOS的设置-> 通知-> OpenMath2LaTeX
    - 打开通知（可以根据个人喜好，建议打开通知）
- 配置api
    - 点击settings进入配置页面
    - 填写api参数，选择合适的快捷键和按键时间，以及保存的历史记录个数
    - 点击保存
- 正式使用
    - 点击On/Off开始
    - 使用任意截图软件，例如`Snipaste`，截图并复制到剪切板
    - 按下你设置的快捷键，并持续你设置的时间，然后释放按键
    - 查看通知的提示，识别成功后，会收到通知栏的通知
    - 成功识别后，，即可粘贴Latex公式到任意地方
- 点击history可查看历史记录，并复制latex公式到剪切板

### 如何调试

- 打开终端

```angular2html
dist/OpenMath2LaTeX.app/Contents/MacOS/OpenMath2LaTeX
```

### 致谢和技术栈

- [图标网站作者ELÍAS的个人主页](https://eliasruiz.com/)
- [ORC识别：openai-python](https://github.com/openai/openai-python)
- [复制和粘贴剪贴板：pyperclip](https://github.com/asweigart/pyperclip)
- [macOS菜单栏应用程序：rumps](https://github.com/jaredks/rumps)
- [macOS应用程序构建：py2app](https://github.com/ronaldoussoren/py2app)
- [图像处理：pillow](https://github.com/python-pillow/Pillow)
- [web服务：fastapi](https://github.com/fastapi/fastapi)
- [orm数据库模型：peewee](https://github.com/coleifer/peewee)
- [键盘事件监控：pynput](https://github.com/moses-palmer/pynput)
- [本地数据库：SQLite](https://www.sqlite.org/)