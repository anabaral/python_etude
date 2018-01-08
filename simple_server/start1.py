from flask import Flask
app = Flask(__name__)

@app.route('/1')
def test1():
    return '1' * 256

@app.route('/2')
def test2():
    return '2' * 256

@app.route('/3')
def test3():
    return '3' * 256

@app.route('/4')
def test4():
    return '4' * 256

@app.route('/5')
def test5():
    return '5' * 256

@app.route('/6')
def test6():
    return '6' * 256

@app.route('/7')
def test7():
    return '7' * 256

@app.route('/8')
def test8():
    return '8' * 256

@app.route('/9')
def test9():
    return '9' * 256

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9080,debug=False)
