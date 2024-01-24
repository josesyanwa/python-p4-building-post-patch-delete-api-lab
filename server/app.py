#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_serialized = bakery.to_dict()
    return jsonify(bakery_serialized), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return jsonify(baked_goods_by_price_serialized), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return jsonify(most_expensive_serialized), 200

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form

    new_baked_good = BakedGood(
        name=data['name'],
        price=data['price'],
        description=data['description']
    )

    db.session.add(new_baked_good)
    db.session.commit()

    return jsonify(new_baked_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    bakery = Bakery.query.get_or_404(id)

    data = request.form

    if 'name' in data:
        bakery.name = data['name']

    db.session.commit()

    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({'message': f'Baked Good with ID {id} deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
