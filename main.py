from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:parnagoli@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text(1000))
    
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
           
        

@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build-a-Blog", blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def main_page():
    return redirect('/')

@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        title_error=''
        body_error=''
        post = Blog(title, blog)
        db.session.add(post)
        db.session.commit()
        def empty(x):
            if x=='':
                return True
        if empty(title) :
             title_error='please fill title' 
        if empty(blog):
            body_error='please fill body'   
        if not title_error and not body_error: 
           return redirect('/individual_blog?id=' + str(post.id))
        else:
            return render_template('newpost.html',title=title,title_error=title_error,blog=blog,body_error=body_error)
    
    else:
        return render_template('newpost.html')


@app.route('/individual_blog')
def singleblog():

    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
       
    return render_template('individual-blog.html', blog=blog)


if __name__ == '__main__':
    app.run()




