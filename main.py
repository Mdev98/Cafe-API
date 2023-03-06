from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

import random as R

app = Flask(__name__)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Render the API documentation 
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    records = db.session.query(Cafe).all()
    random_cafe = R.choice(records)

    return jsonify(random_cafe.to_dict())

@app.route("/all")
def get_all_cafe():
    records = db.session.query(Cafe).all()
    return jsonify([{'name' : record.name, 'price' : record.coffee_price, 'image' : record.img_url} for record in records])

@app.route("/cafe/<int:cafe_id>", methods=['GET'])
def get_single_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)

    if not cafe:
        return jsonify(success=False, message="Record not found")
    
    
    return jsonify(success=True, data=cafe.to_dict())

@app.route("/search", methods=['GET'])
def search_cafe():
    loc = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=loc).first()
    if cafe:
        return jsonify(cafe.to_dict())
    else:
        return jsonify(success=False, message="Sorry we don't have cafe at that location")
    

@app.route("/add", methods=['POST'])
def add_cafe():

    cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )

    db.session.add(cafe)
    db.session.commit()
    return jsonify(success=True, data=cafe.to_dict())


@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_coffee_price(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    new_price = request.form['price']

    if not cafe:
        return jsonify(success=False, message="Record not found")
    

    if request.args['api-key'] == "TOPSECRET":
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(success=True, data=cafe.to_dict())
    
    return jsonify(success=False, message="Not Authorize")



@app.route("/delete/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)

    if not cafe:
        return jsonify(success=False, message="Record not found")

    if request.args['api-key'] == "TOPSECRET":
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(success=True, message="Record deleted")
    
    return jsonify(success=False, message="Not Authorize")



if __name__ == '__main__':
    app.run(debug=True)
