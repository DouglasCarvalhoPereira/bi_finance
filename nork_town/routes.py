from nork_town import app, db, login_manager
from nork_town.forms import Form_Edit_RegisterPeople, FormLogin, FormNewCar
from nork_town.models import Cars, User, Peoples
from flask import Flask, redirect, render_template, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required

#DEFINE TIPO DE SESSÃO DO USUÁRIO
@login_manager.user_loader
def load_user(id_usuario):
      return User.query.get(int(id_usuario))

@app.route('/') #HOME
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET']) #LOGIN
def login():
    form_login = FormLogin()

    email = request.form.get('email')
    password = request.form.get('password')
    remember_user = request.form.get('remember_user')

    #Validade send data
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user, remember=remember_user)
            flash(f'Login realizado com sucesso!')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('people_feed'))

        else:
            flash(f'E-mail ou Senha incorretos!','alert-danger')

    return render_template('login.html', form_login=form_login)

@app.route('/sair')
def logout():
    logout_user()
    return redirect(url_for('index'))   

@app.route('/cadastro/pessoa', methods=['POST', 'GET']) #CADASTRO PROFISSIONAL
@login_required
def register_people():
    new_people = Form_Edit_RegisterPeople()

    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    
    if new_people.validate_on_submit():
        user = Peoples(name=full_name, email=email, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Cadastro realizado com sucesso!', 'alert-success')
        return redirect(url_for('people_feed'))

    return render_template('people-registration.html', new_people=new_people)



@app.route('/pessoa/<id_people>/editar', methods=['POST', 'GET']) #PAGINA DO PROFISSIONAL
@login_required
def edit_register_people(id_people):
    users = Peoples.query.get(id_people)

    new_people = Form_Edit_RegisterPeople()

    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')

    if new_people.validate_on_submit():
        update = Peoples.query.filter_by(email=users.email).update({
                    User.name : full_name, 
                    User.email : email, 
                    User.phone_number : phone_number, 
                    })
        db.session.commit()
        flash(f'Perfil atualizado com sucesso!')
        return redirect(url_for('people_page', id_people=users.id))
        
    elif request.method == 'GET':
        new_people.full_name.data = users.name
        new_people.email.data = users.email
        new_people.phone_number.data = users.phone_number

    return render_template('edit-people-registration.html', id_people=id_people, users=users, new_people=new_people)


@app.route('/projeto/novo', methods=['POST', 'GET']) #PUBLICA NOVO PROJETO
@login_required
def new_car():

    #New Car
    form_new_car = FormNewCar()
    form_new_car.people.choices = Peoples.query.all()
                      
    #AUTHENTICATED NEW PROJECT
    people = str(request.form.get('people'))
    model = request.form.get('model')
    brand = request.form.get('brand')
    car_type = request.form.get('car_type')
    color_car = request.form.get('color_car')
    description = request.form.get('description')

    #Get Id
    people_id = people.split('-')[0]

    if form_new_car.validate_on_submit():
        if current_user.is_authenticated:
            car = Cars(model=model, brand=brand, car_type=car_type, color_car=color_car, 
                            description=description, id_user=people_id)
            db.session.add(car)
            db.session.commit()
            flash(f'Carro "{model}" criado com sucesso!')
            
            return redirect(url_for('cars_feed'))        

    return render_template('new-car.html', form_new_car=form_new_car)


@app.route('/carros') #FEED DE PROJETOS
@login_required
def cars_feed():
    cars = Cars.query.order_by(Cars.id.desc())
    cars_all = Cars.query.all() 
    user = User.query.all()
    return render_template('cars-feed.html', cars=cars, user=user, cars_all=cars_all)

@app.route('/pessoas') #FEED DE PROFISSIONAIS
@login_required
def people_feed():
    users = Peoples.query.order_by(Peoples.id.desc())
    return render_template('people-feed.html', users=users)

@app.route('/pessoa/<id_people>/') #PAGINA DO PROFISSIONAL
@login_required
def people_page(id_people):
    users = Peoples.query.get(id_people)
    cars = Cars.query.get(id_people)

    return render_template('people-page.html', id_people=id_people, users=users, cars=cars)

@app.route('/pessoa/carro/<id_car>') #PAGINA NO PROJETO
@login_required
def car_page(id_car):
    id_cars = Cars.query.get(id_car)
    user = User.query.all()
    return render_template('car-page.html', user=user, id_cars=id_cars)