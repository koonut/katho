from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,session)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Library, Experience, Question,Conversation,Video,Options,Feedback
from flaskblog.posts.forms import PostForm, ExperienceForm
from sqlalchemy import func

posts = Blueprint('posts', __name__)


@posts.route("/Library/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Library(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Library has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_Library.html', title='New Library',
                           form=form, legend='Create a New Library')


@posts.route("/Library/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Library.query.get_or_404(post_id)
    current_post=Experience.query.filter(Experience.post_id==post_id)
    expId=request.form.get('eid' , type=int)
    if(expId!=None):
        dele = Experience.query.filter(Experience.eid==expId).first()
        conversations = Conversation.query.filter(Conversation.experience_id==expId).all()
        for conversation in conversations:
            db.session.delete(conversation)
        db.session.delete(dele)
        db.session.commit()
        
    return render_template('Library.html', title=post.title, post=post,experiences=current_post)

@posts.route("/Library/existing", methods=['GET', 'POST'])
@login_required
def existing_experience():
    page = request.args.get('page', 1, type=int)
    posts = Library.query.order_by(Library.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('existing_libraries.html', posts=posts)
   # return render_template('existing_libraries.html', etitle='Existing Libraries',
   #                         legend='Existing Libraries')

@posts.route("/Library/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Library.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Library has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_Library.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/Library/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Library.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    # Delete related experiences and conversations
    experiences = Experience.query.filter_by(post_id=post_id).all()
    for experience in experiences:
        # Delete related conversations
        conversations = Conversation.query.filter_by(experience_id=experience.eid).all()
        for conversation in conversations:
            db.session.delete(conversation)

        db.session.delete(experience)

    db.session.delete(post)
    db.session.commit()
    flash('Your Library has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/upload_video', methods=['GET', 'POST'])
@login_required
def upload_video():

    # filename = request.args.get('filename', type=str)
    
    con=db.session.query(func.max(Conversation.id)).scalar()
    video=Video(url='D:\Koonut',filename='abc',user_id=current_user.id,con_id=con)
    db.session.add(video)
    db.session.commit()
    return redirect(request.referrer)


#-------------------------------------------------
#creating a post for conversation page


## try using while do
@posts.route('/conversation' ,methods=['GET','POST'])
@login_required
def conversation():
    new = request.args.get('new')
    print('new :',new)
    if new == 1:
        questions =''
        db.session.add(conversation)
        db.session.commit()
        return render_template('conversation.html', title='Conversation Page',
                            optionCount=0,optionCountO=0,con=con,lib=lib,type_current=type_current,question='None')
    elif new == None:
        questions = request.form.get('question')
        scores = request.form.getlist('scores[]')
        options_list =request.form.getlist('options[]')
        optionCount = request.form.get('optionCount', type=int)
        questions1 = request.form.get('question1')
        optionCountO= request.form.get('optionCountO', type=int)
        scores1 = request.form.getlist('scores1[]')
        options_list1 =request.form.getlist('options1[]')
        #store the data
        if optionCount == None:
            optionCount=session.get('optionCounts' )
            questions=session.get('questions')
            scores=session.get('scores')
            options_list=session.get('options_list')

        else:#get data
            session['optionCounts'] = optionCount
            session['newOptionCounts'] = optionCount
            session['questions']=questions
            session['scores']=scores
            session['options_list']=options_list
        optionCountO=request.form.get('optionCountO', type=int)
        print("count: ",optionCount)
        print("countO: ",optionCountO)
        print("data :" ,questions,scores,options_list,optionCount)
    
        late_ex=db.session.query(func.max(Experience.eid)).scalar()
        current_library=db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
        text_type="Conversation"
        conversation = Conversation(library_id=current_library, experience_id=late_ex,  types=text_type)
        
        con = Experience.query.filter_by(eid=late_ex,post_id=current_library) 
        lib=Library.query.filter_by(id=current_library)
        type_current=Conversation.query.filter_by(library_id=current_library,experience_id=late_ex).first()
        
        #get data from form in array
        s_name=request.form.getlist('name[]')
        score1=request.form.getlist('score1[]')
        score2=request.form.getlist('score2[]')
        score3=request.form.getlist('score3[]')
        print("data:",s_name,score1,score2,score3)
        for i in range(0,len(s_name)):
            option_id=db.session.query(func.max(Options.id)).scalar()
            feedback=Feedback(score_name=s_name[i],point1=score1[i],point2=score2[i],point3=score3[i],option_id=option_id)
            db.session.add(feedback)
            db.session.commit()
            return render_template('conversation.html', title='Conversation Page',
                                optionCount=optionCount,optionCountO=optionCountO,con=con,lib=lib,type_current=type_current)
        print("question :",questions)
        if questions == 'None':# it supposet to be == 'None' but the form doesn't work with that 
            
            db.session.add(conversation)
            db.session.commit()
            return render_template('conversation.html', title='Conversation Page',
                                optionCount=optionCount,optionCountO=optionCountO,con=con,lib=lib,type_current=type_current)
        else:
            this_question=Question(question_text=questions,dragV_id=1)
            db.session.add_all([conversation, this_question])
            current_question=db.session.query(func.max(Question.id)).scalar()
            if optionCount is not None:
                optionCount = int(optionCount)
            else:
                optionCount = 0
    
            for i in range(0,optionCount):
                this_option=Options(text=options_list[i],score=scores[i],question_id=current_question,visible=0)
                db.session.add(this_option)
                db.session.commit()
        
            current_show=Options.query.filter_by(question_id=current_question)
            return render_template('conversation.html', title='Conversation Page',
                            optionCount=optionCount,optionCountO=optionCountO,con=con,lib=lib,type_current=type_current,current_show=current_show,question=questions)
    late_ex=db.session.query(func.max(Experience.eid)).scalar()
    current_library=db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
    lib=Library.query.filter_by(id=current_library)
    con = Experience.query.filter_by(eid=late_ex,post_id=current_library) 
    type_current=Conversation.query.filter_by(library_id=current_library,experience_id=late_ex).first()
    return render_template('conversation.html', title='Conversation Page',
                            optionCount=0,optionCountO=0,con=con,lib=lib,type_current=type_current,question='None')
#-------------------------------------------------
#creating a post for options page

@posts.route('/options', methods=['GET','POST'], endpoint='options')
@login_required
def options():
    
    return render_template("options.html", post=post)


#------------------------------------------------------
#creating a post for 3rd row display

@posts.route('/options_options', methods=['GET','POST'])
@login_required
def options_options():
    #post = Post.query.get_or_404(post_id)
    return render_template("options_options.html", post=post)
@posts.route('/media_Library')
@login_required
def media_Library():
    #post = Post.query.get_or_404(post_id)
    return render_template("media_Library.html", post=post, title='Media Library Page')

#-------------------------------------------------
#creating a Feedback for conversation page

@posts.route('/Feedbackcon', methods=['GET','POST'])
@login_required
def Feedbackcon():
    #post = Post.query.get_or_404(post_id)
    return render_template("Feedbackcon.html", post=post)


#-------------------------------------------------------------
# creating a post for Vitual tour page
@posts.route('/virtualtour')
@login_required
def virtualtour():
    buttonCount = request.args.get('button_count', type=int)
    return render_template('virtualtour.html', title='virtualtour Page', buttonCount=buttonCount)


#-------------------------------------------------
#creating a post for virtual tour hotspot page

@posts.route('/hotspot', methods=['GET'])
@login_required
def hotspot():
    return render_template("hotspot.html", post=post)

#-------------------------------------------------
#creating a post for hotspot settings page

@posts.route('/hotspotsettings', methods=['GET'])
@login_required
def hotspotsettings():
    return render_template("hotspotsettings.html", post=post)

#---------------------------------------------------
# Creating new experience
@posts.route("/experience/new/<int:post_id>", methods=['GET', 'POST'])
@login_required
def new_experience(post_id): 
    form = ExperienceForm()
    if form.validate_on_submit():
        experience = Experience(etitle=form.etitle.data, econtent=form.econtent.data, user_id=current_user.id, post_id=post_id)
        db.session.add(experience)
        db.session.commit()
        flash('Your experience has been created!', 'success')
        return redirect(url_for('main.home'))
    elif form.virtual_tour.data:
        experience = Experience(etitle=form.etitle.data, econtent=form.econtent.data, user_id=current_user.id, post_id=post_id)
        db.session.add(experience)
        db.session.commit()
        return redirect(url_for('posts.virtualtour'))
    elif form.conversation.data:
        library_instance = Library.query.get(post_id)
        experience_instance = Experience(etitle=form.etitle.data, econtent=form.econtent.data, user_id=current_user.id, post_id=post_id)
        db.session.add(experience_instance)
        db.session.commit()
        late_ex=db.session.query(func.max(Experience.eid)).scalar()
        current_library=db.session.query(Experience.post_id).filter(Experience.eid == late_ex).scalar()
        text_type="Conversation"
        conversation = Conversation(library_id=current_library, experience_id=late_ex,  types=text_type)
        db.session.add(conversation)
        db.session.commit()
        late_con=db.session.query(func.max(Conversation.id)).scalar()
        con = Experience.query.filter_by(eid=late_ex,post_id=current_library)
        return redirect(url_for('posts.conversation',con=con,late_con=late_con,questions=None,optionCount=0,optionCountO=0,new=1))
    return render_template('create_experience.html', title='New Experience', form=form, legend='New Experience')

#-----------------------------------------------------
#-------------------------------------------------
#creating a post for conversation page
@posts.route('/conversationlist')
@login_required
def conversationlist():
    
    current_library=request.args.get('library_id', type=int)
    late_ex=request.args.get('experience_id', type=int)
    optionCount = request.args.get('optionCount', type=int)
    optionCountO=request.args.get('optionCountO', type=int)
    con = Experience.query.filter_by(eid=late_ex,post_id=current_library)
    lib=Library.query.filter_by(id=current_library)
    type_current=Conversation.query.filter_by(library_id=current_library,experience_id=late_ex).first()
    # type_current=Conversation.query.filter_by(id=current_con)
    current_question=db.session.query(func.max(Question.id)).scalar()
    return render_template('conversation.html', title='Conversation Page', optionCount=optionCount,optionCountO=optionCountO,con=con,lib=lib,type_current=type_current,current_question=current_question)



