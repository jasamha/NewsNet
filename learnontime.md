### flask项目
#### 易忘点
* 默认浏览器将数据作为text/html解析,需要告诉浏览器当前数据的类型为［image/png］ 如response.mimetype='image/png'
* requirements.txt 文件,用于记录所有依赖包及其精确的版本号
    * (venv) $ pip freeze >requirements.txt 生成对应的依赖包到文件中
    * (venv) $ pip install -r requirements.txt 安装文件中所有的依赖包
#### 知识点
* 装饰器property