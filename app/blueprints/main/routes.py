import json
from flask import request, jsonify, render_template
from app.blueprints.main import main_bp
from app.extensions import db
from app.models.tomato import TomatoVariety, Person

@main_bp.route('/')
def index():
    varieties = db.session.scalars(db.select(TomatoVariety).order_by(TomatoVariety.id)).all()
    persons = db.session.scalars(db.select(Person).order_by(Person.name)).all()
    persons_json = json.dumps([{"id": p.id, "name": p.name} for p in persons])
    varieties_json = json.dumps([{
        "id": v.id,
        "name": v.name,
        "category": v.category,
        "color": v.color,
        "size": v.size,
        "origin": v.origin,
        "description": v.description,
        "image_url": v.image_url,
        "fallback_image_url": v.fallback_image_url,
        "owner_id": v.owner_id,
        "owner_name": v.owner.name if v.owner else None,
        "in_stock": v.in_stock
    } for v in varieties])
    return render_template('index.html', varieties=varieties, persons=persons, persons_json=persons_json, varieties_json=varieties_json)

@main_bp.route('/api/varieties/<int:variety_id>', methods=['POST'])
def edit_variety(variety_id):
    variety = db.get_or_404(TomatoVariety, variety_id)
    data = request.get_json() or {}
    
    # Simple validation
    name = data.get('name')
    if not name or not name.strip():
        return jsonify({'success': False, 'message': 'Le nom de la variété est requis.'}), 400
        
    # Owner and stock status updates
    owner_id_raw = data.get('owner_id')
    if owner_id_raw is not None and owner_id_raw != 'null' and str(owner_id_raw).strip() != '':
        target_owner_id = int(owner_id_raw)
    else:
        target_owner_id = None

    # Check name uniqueness for the target owner (excluding self)
    existing = TomatoVariety.query.filter(
        TomatoVariety.name == name,
        TomatoVariety.owner_id == target_owner_id,
        TomatoVariety.id != variety_id
    ).first()
    if existing:
        return jsonify({'success': False, 'message': 'Une variété avec ce nom existe déjà pour ce propriétaire.'}), 400

    # Update fields
    variety.name = name.strip()
    variety.category = (data.get('category') or '').strip() or None
    variety.color = (data.get('color') or '').strip() or None
    variety.size = (data.get('size') or '').strip() or None
    variety.origin = (data.get('origin') or '').strip() or None
    variety.description = (data.get('description') or '').strip() or None
    variety.image_url = (data.get('image_url') or '').strip() or None
    variety.fallback_image_url = (data.get('fallback_image_url') or '').strip() or None
    
    variety.owner_id = target_owner_id
    variety.in_stock = bool(data.get('in_stock', True))

    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Variété mise à jour avec succès.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erreur de base de données: {str(e)}'}), 500

