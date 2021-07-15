from flask import Flask, render_template, request, redirect, url_for
from declarationForm import CreateUserForm
from datetime import datetime
import shelve, User

app = Flask(__name__)


@app.route('/')
def baseUser():
    return render_template('baseUser.html')


@app.route('/baseAdmin')
def baseAdmin():
    return render_template('baseAdmin.html')


@app.route('/declarationForm', methods=['GET', 'POST'])
def create_user():
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('HealthDeclaration.db', 'c')
            users_dict = db['Users']
        except IOError:
            print("Error in retrieving Users from HealthDeclaration.db.")
        except:
            print("An unknown error has occured.")
        else:
            user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                            create_user_form.ic.data, create_user_form.phone_no.data,
                            create_user_form.room_no.data,
                            date_time, create_user_form.q1.data,
                            create_user_form.q2.data, create_user_form.q3.data, create_user_form.q4.data,
                            create_user_form.q5.data, create_user_form.q6.data,
                            create_user_form.q7.data, create_user_form.status.data)
            user.set_status()

            user.set_ans()
            users_dict[user.get_user_id()] = user
            db['Users'] = users_dict

            db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('declarationForm.html', form=create_user_form)


@app.route('/view_declaration_info')
def retrieve_users():
    users_dict = {}
    try:
        db = shelve.open('HealthDeclaration.db', 'r')
        users_dict = db['Users']
        db.close()
    except IOError:
        print("Error in retrieving form info.")
    except:
        print("An unknown error has occured.")
    else:
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            user.set_ans()
            user.set_status()
            users_list.append(user)

        return render_template('view_declaration_info.html', count=len(users_list), users_list=users_list)


@app.route('/viewDetails/<int:id>/')
def view_details(id):
    update_user_form = CreateUserForm(request.form)
    users_dict = {}
    try:
        db = shelve.open('HealthDeclaration.db', 'r')
        users_dict = db['Users']
        db.close()
    except IOError:
        print("error in retrieving updated info")
    except:
        print("an unknown error has occured.")
    else:
        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.ic.data = user.get_ic()
        update_user_form.phone_no.data = user.get_phone_no()
        update_user_form.room_no.data = user.get_room_no()
        update_user_form.q1.data = user.get_q1()
        update_user_form.q2.data = user.get_q2()
        update_user_form.q3.data = user.get_q3()
        update_user_form.q4.data = user.get_q4()
        update_user_form.q5.data = user.get_q5()
        update_user_form.q6.data = user.get_q6()
        update_user_form.q7.data = user.get_q7()
        user.get_status()

    return render_template('viewDetails.html', form=update_user_form)


@app.route('/retrieve_user_info')
def retrieve_admin():
    ok = 0
    users_dict = {}
    try:
        db = shelve.open('HealthDeclaration.db', 'r')
        users_dict = db['Users']
        db.close()
    except IOError:
        print("Error while retrieving user info")
    except:
        print("An unknown error has occured.")
    else:
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            user.set_ans()
            user.set_status()
            users_list.append(user)
            if user.get_status() == "Safe":
                ok += 1
                print(ok)

        return render_template('retrieve_user_info.html', count=len(users_list), users_list=users_list, safe=ok)


@app.route('/update_declaration_form/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        try:
            db = shelve.open('HealthDeclaration.db', 'w')
            users_dict = db['Users']
        except IOError:
            print("error in updating info.")
        except:
            print("An unknown error has occured.")
        else:

            user = users_dict.get(id)
            user.set_first_name(update_user_form.first_name.data)
            user.set_last_name(update_user_form.last_name.data)
            user.set_ic(update_user_form.ic.data)
            user.set_phone_no(update_user_form.phone_no.data)
            user.set_room_no(update_user_form.room_no.data)
            user.set_time(date_time)
            user.set_q1(update_user_form.q1.data)
            user.set_q2(update_user_form.q2.data)
            user.set_q3(update_user_form.q3.data)
            user.set_q4(update_user_form.q4.data)
            user.set_q5(update_user_form.q5.data)
            user.set_q6(update_user_form.q6.data)
            user.set_q7(update_user_form.q7.data)
            user.set_ans()
            user.set_status()

            db['Users'] = users_dict
            db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        try:
            db = shelve.open('HealthDeclaration.db', 'r')
            users_dict = db['Users']
            db.close()
        except IOError:
            print("error in retrieving updated info")
        except:
            print("an unknown error has occured.")
        else:
            user = users_dict.get(id)
            update_user_form.first_name.data = user.get_first_name()
            update_user_form.last_name.data = user.get_last_name()
            update_user_form.ic.data = user.get_ic()
            update_user_form.phone_no.data = user.get_phone_no()
            update_user_form.room_no.data = user.get_room_no()
            update_user_form.q1.data = user.get_q1()
            update_user_form.q2.data = user.get_q2()
            update_user_form.q3.data = user.get_q3()
            update_user_form.q4.data = user.get_q4()
            update_user_form.q5.data = user.get_q5()
            update_user_form.q6.data = user.get_q6()
            update_user_form.q7.data = user.get_q7()
            user.get_status()

        return render_template('update_declaration_form.html', form=update_user_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('Error500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
