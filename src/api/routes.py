"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Recipe
from api.models import db, User, Administrador
from api.models import db, User, User, Comment
from api.models import db, User, Administrador, Category, recipe_categories
from api.models import db, User, User
from api.models import db, User, Favorito
from api.models import db, User, Calificacion
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import SQLAlchemyError
import cloudinary 
import cloudinary.uploader 
import cloudinary.api
import json

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/recetas/create', methods=['POST'])
def create_recete():
    data = request.form
    img_urls = []
    for img in request.files:
        if img.startswith("files_"):
            imgupload = request.files[img]
            try:
                upload_data = cloudinary.uploader.upload(imgupload)
                img_urls.append(upload_data['url'])
                print(f"Uploaded image URL: {upload_data['url']}")
            except Exception as e:
                return jsonify({"msg": f"Error al subir la imagen: {e}"}), 500

    print(f"Image URLs to be saved: {img_urls}")
    
    categoria_ids = json.loads(data.get('categories', '[]'))
    print(f"img_urls: {img_urls}")
    new_recipe = Recipe(
        title=data['title'],
        ingredientes=json.loads(data['ingredientes']),
        pasos=data['pasos'],
        img_ilustrativa=img_urls,
        user_id=int(data['user_id']),
    )
    for categoria_id in categoria_ids:
        categoria = Category.query.get(categoria_id)
        if categoria:
            new_recipe.categories.append(categoria)

    print(new_recipe)
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.serialize()), 201

@api.route('/recetas', methods=['GET'])
def get_all():
    recipes = Recipe.query.all()
    serialized_recipes = []
    for recipe in recipes:
        serialized_recipes.append(recipe.serialize())
        
    if serialized_recipes:
        return jsonify(serialized_recipes), 200
    else: return {'msg':'No hay recetas que mostrar actualmente!'}, 400

@api.route('/recetas/<int:id>', methods=['GET'])
def get_recipe_id(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if recipe:
        print(recipe.serialize())
        return jsonify(recipe.serialize()), 200
    else: return {"msg":"No existe la receta solicitada!"}, 400

@api.route('/recetas/<int:id>', methods=['DELETE'])
def recipe_delete(id):
    recipe = Recipe.query.filter_by(id=id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return {"msg":"Su receta se elimino con exito!"}, 200
    else: return {"msg":"No hay una receta que eliminar!"}, 400

@api.route('/recetas/update/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.form
    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return jsonify({"msg": "Recipe not found!"}), 404

    recipe.title = data.get('title', recipe.title)
    recipe.ingredientes = json.loads(data.get('ingredientes', json.dumps(recipe.ingredientes)))
    recipe.pasos = data.get('pasos', recipe.pasos)

    img_urls = []
    for img in request.files:
        if img.startswith("files_"):
            imgupload = request.files[img]
            try:
                upload_data = cloudinary.uploader.upload(imgupload)
                img_url = upload_data['url']
                img_urls.append(img_url)
                print(f"Uploaded image URL: {img_url}")
            except Exception as e:
                return jsonify({"msg": f"Error al subir la imagen: {e}"}), 500
    print(f"Image URLs to be saved: {img_urls}")
    recipe.img_ilustrativa = img_urls


    categoria_ids = json.loads(data.get('categories', '[]'))
    if (categoria_ids, int):
        categoria_ids = [categoria_ids]
    categoria_ids = [int(id) for id in categoria_ids]

    recipe.categories.clear()
    for categoria_id in categoria_ids:
        categoria = Category.query.get(categoria_id)
        if categoria:
            recipe.categories.append(categoria)

    db.session.commit()
    return jsonify(recipe.serialize()), 200


@api.route("/administrador", methods=["POST"])
def signup():
    body = request.get_json()
    
    if not body:
        return jsonify({"msg": "No se recibió ningún dato"}), 400  

    print(body)

    administrador = Administrador.query.filter_by(email=body["email"]).first()
    print(administrador)

    if administrador is None: 
        administrador = Administrador(
            name=body["name"],
            last_name=body["last_name"],
            email=body["email"],  
            password=body["password"], 
            is_active=True
        )
        db.session.add(administrador)
        db.session.commit()

        response_body = {
            "msg": "usuario de administrador creado"
        }
        return jsonify(response_body), 201  
    else:
        return jsonify({"msg": "ya hay un usuario con ese email"}), 


@api.route('/administrador', methods=['GET'])
def get_administradores():
    all_administradores = list(Administrador.query.all())
    results = list(map(lambda administrador: administrador.serialize(), all_administradores)) 

    return jsonify(results), 200

@api.route('/administrador/<int:administrador_id>', methods=['GET'])
def get_administrador(administrador_id):
    # Buscar el administrador por ID
    administrador = Administrador.query.filter_by(id=administrador_id).first()
    
    if administrador is None:
        return jsonify({"error": "administrador no encontrado"}), 404  # Error 404 si no se encuentra

    return jsonify(administrador.serialize()), 200  

@api.route('/administrador/<int:administrador_id>', methods=['DELETE'])
def delete_administrador(administrador_id):
    try:
        # Buscar el administrador por ID
        administrador = Administrador.query.filter_by(id=administrador_id).first()
        
        if administrador is None:
            return jsonify({"error": "administrador no encontrado"}), 404  # Error 404 si no se encuentra

        # Eliminar el administrador
        db.session.delete(administrador)
        db.session.commit()

        return jsonify({"msg": "administrador eliminado exitosamente"}), 200  
    except Exception as e:
        return jsonify({"error": "Ocurrió un error al eliminar el administrador", "detail": str(e)}), 500  

@api.route('/administrador/<int:administrador_id>', methods=['PUT'])
def update_administrador(administrador_id):
    body = request.get_json() 

    if not body:
        return jsonify({"msg": "No se recibió ningún dato"}), 400  

  
    administrador = Administrador.query.filter_by(id=administrador_id).first()
    
    if administrador is None:
        return jsonify({"error": "administrador no encontrado"}), 404  

    administrador.name = body.get('name', administrador.name)
    administrador.last_name = body.get('last_name', administrador.last_name)
    administrador.email = body.get('email', administrador.email)
    administrador.password = body.get('password', administrador.password)  
    administrador.is_active = body.get('is_active', administrador.is_active)

   
    db.session.commit()

    return jsonify({"msg": "administrador actualizado exitosamente"}), 200  

@api.route('/usuario', methods=['POST'])
def create_usuario():
    body = request.form
    img_to_send = request.files.get('file')
    print("Image file:", img_to_send)
    img_profile_url=None
    print("Form data:", request.form)
    print("Files data:", request.files)

    if img_to_send:
        try:
            upload_data = cloudinary.uploader.upload(img_to_send)
            img_profile_url = upload_data['url']
        except Exception as e:
            print(f"Error al subir imagen: {e}")
            return jsonify({"msg": f"Error al subir imagen: {e}"}), 500
    # Verificar si el usuario ya existe por email
    usuario = User.query.filter_by(email=body["email"]).first()
    if usuario is None:
        new_usuario = User(
            name=request.form['name'],
            last_name=request.form["last_name"],
            email=request.form["email"],
            password=request.form["password"],  
            is_active=True,
            img_profile= img_profile_url
        )
        db.session.add(new_usuario)
        db.session.commit()

        return jsonify({"msg": "Usuario creado exitosamente"}), 201
    else:
        return jsonify({"msg": "Ya existe un usuario con ese email"}), 409

@api.route('/usuario', methods=['GET'])
def get_usuarios():
    all_usuarios = User.query.all()
    results = [usuario.serialize() for usuario in all_usuarios]
    return jsonify(results), 200

@api.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = User.query.filter_by(id=usuario_id).first()
    
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario.serialize()), 200

@api.route('/usuario/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    usuario = User.query.filter_by(id=usuario_id).first()
    
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario eliminado exitosamente"}), 200

@api.route('/usuario/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    body = request.get_json()

    if not body:
        return jsonify({"msg": "No se recibió ningún dato"}), 400

    usuario = User.query.filter_by(id=usuario_id).first()
    
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Actualizar los campos del usuario con los nuevos datos
    usuario.name = body.get('name', usuario.name)
    usuario.last_name = body.get('last_name', usuario.last_name)
    usuario.email = body.get('email', usuario.email)
    usuario.password = body.get('password', usuario.password)  
    usuario.is_active = body.get('is_active', usuario.is_active)

    db.session.commit()

    return jsonify({"msg": "Usuario actualizado exitosamente"}), 200

@api.route('/usuario/login', methods=['POST'])

def login_user():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")
    
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify('Se logueo correctamente!', access_token), 200
    
    else:
        return jsonify('Hubo un error en las credenciales'), 401
    
@api.route('/administrador/login', methods=['POST'])
def login_admin():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")
    
    admin = Administrador.query.filter_by(email=email).first()

    if admin and admin.password == password:
        access_token = create_access_token(identity=admin.id)
        return jsonify('Se logueo correctamente!', access_token), 200
    else:
        return jsonify('Hubo un error en las credenciales'), 401
    
@api.route('/comentario', methods=['GET'])
def get_comentarios():
    try:
        all_comentarios = Comment.query.all()
        print(f'Comentarios recuperados: {all_comentarios}')
        results = list(map(lambda comentario: comentario.serialize(), all_comentarios))
        print(f'Resultados serializados: {results}')
        return jsonify(results), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500
    


@api.route("/comentario", methods=["POST"])
def create_comment():
    body = request.get_json() 
    if not body:
        return jsonify({"msg": "No se recibió ningún dato"}), 400
    if "user_id" not in body or "recipe_id" not in body or "comment_text" not in body:
        return jsonify({"msg": "Datos incompletos"}), 400
    if not body["comment_text"].strip():
        return jsonify({"msg": "El texto del comentario no puede estar vacío"}), 400

    user = User.query.get(body["user_id"])
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    recipe = Recipe.query.get(body["recipe_id"])
    if not recipe:
        return jsonify({"msg": "Receta no encontrada"}), 404

    try:
        comentario = Comment(
            user_id=user.id,
            recipe_id=recipe.id,
            comment_text=body["comment_text"]
        )
        db.session.add(comentario)
        db.session.commit()

        response_body = {
            "msg": "Comentario creado con éxito",
            "comment": comentario.serialize()  
        }
        return jsonify(response_body), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear el comentario", "error": str(e)}), 500
   

@api.route('/edit/comentario/<int:comentario_id>', methods=['PUT'])
def edit_comentario(comentario_id):
 
    comentario = Comment.query.get(comentario_id)
    if not comentario:
        return jsonify({"msg": "Comentario no encontrado"}), 404
    
    data = request.get_json()
    
    if 'comment_text' not in data:
        return jsonify({"msg": "El texto del comentario es requerido"}), 400

    comentario.comment_text = data['comment_text']
    db.session.commit()
    return jsonify(comentario.serialize()), 200


@api.route('/delete/comentario/<int:comentario_id>', methods=['DELETE']) 
@jwt_required()
def delete_comentario(comentario_id): 
    user_id = get_jwt_identity()
    print (user_id)
    comentario = Comment.query.get(comentario_id)
    if comentario.user_id!=user_id:
        return jsonify({"msg": "Comentario no pertenece al usuario"}), 404 

    if not comentario:
        return jsonify({"msg": "Comentario no encontrado"}), 404  
    
    db.session.delete(comentario)
    db.session.commit()  
    
    return jsonify({"msg": "Comentario eliminado exitosamente"}), 200

@api.route('/comentario/<int:comentario_id>', methods=['GET'])
def get_comentario(comentario_id):
    try:
        comentario = Comment.query.get(comentario_id)
        if not comentario:
            return jsonify({"msg": "Comentario no encontrado"}), 404
        
        return jsonify(comentario.serialize()), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500 
    

@api.route('/comentario/receta/<int:recipe_id>', methods=['GET'])
def get_comments_by_recipe(recipe_id):
    try:
        comentarios = Comment.query.filter_by(recipe_id=recipe_id).all()
        
        if not comentarios:
            return jsonify({"msg": "No hay comentarios para esta receta"}), 404

        results = [comentario.serialize() for comentario in comentarios]
        return jsonify(results), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500


       
@api.route('/categorias/create', methods=['POST'])

def create_categoria():
    body = request.get_json()
    nombre = body.get('nombre')

    new_categoria = Category(name=nombre)
    db.session.add(new_categoria)
    db.session.commit()
    return jsonify(new_categoria.serialize()), 200

@api.route('/categorias', methods=['GET'])
def get_categories():
    categories= Category.query.all()
    return jsonify([categoria.serialize() for categoria in categories]), 200

@api.route('/categorias/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"msg":"Categoria no encontrada"}),400
    return jsonify({category.serialize()}),200

@api.route('/categorias/<int:id>', methods=['PUT'])
def update_category(id):
    body = request.get_json()
    category = Category.query.get(id)
    name = body.get('name')
    if name:
        category.name = name

    db.session.commit()
    return jsonify(category.serialize()),200

@api.route('/categorias/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"msg":"Categoria no encontrada!!"}),400
    db.session.delete(category)
    db.session.commit()
    return jsonify({"msg": "Categoria eliminada"}),200

@api.route('/favoritos', methods=['GET'])
@jwt_required()
def obtener_favoritos():
    user_id = get_jwt_identity()  
    favoritos = Favorito.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        "user_id": user_id,
        "favoritos": [favorito.serialize() for favorito in favoritos]
    }),200


@api.route('/favoritos/<int:recipe_id>', methods=['POST'])
@jwt_required()
def agregar_favorito(recipe_id):
    user_id = get_jwt_identity()  

    favorito_existente = Favorito.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if favorito_existente:
        return jsonify({"msg": "La receta ya está en favoritos"}), 409

    nuevo_favorito = Favorito(user_id=user_id, recipe_id=recipe_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    return jsonify({"msg": "Receta añadida a favoritos"}), 201

@api.route('/favoritos/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def eliminar_favorito(recipe_id):
    user_id = get_jwt_identity() 

    # Buscar el favorito en la base de datos
    favorito = Favorito.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not favorito:
        return jsonify({"msg": "La receta no está en favoritos"}), 404

    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Receta eliminada de favoritos"}), 200

@api.route('/recetas/filter/<int:categoria_id>', methods=['GET'])
def filtrar_recetas(categoria_id):
        recetas = Recipe.query.join(recipe_categories).join(Category).filter(Category.id == categoria_id).all()
        if not recetas:
            return jsonify({"message": "No se encontraron recetas"}), 404
        return jsonify([recipe.serialize() for recipe in recetas]), 200

@api.route('/recetas/filter/search', methods=['GET'])
def search_recipe():
    query = request.args.get('query')
    if not query:
        return jsonify({"msg": "No se proporciono palabra de busqueda"}), 400
    recetas = Recipe.query.filter(Recipe.title.ilike(f"%{query}%")).all()
    if not recetas: 
        return jsonify({"message": "No se encontraron recetas"}), 404 
    return jsonify([recipe.serialize() for recipe in recetas]), 200

@api.route('/calificaciones', methods=['POST'])
@jwt_required()
def agregar_o_actualizar_calificacion():
    data = request.get_json()
    user_id = get_jwt_identity()
    recipe_id = data.get('recipe_id')
    qualification = data.get('qualification')

    if not (1 <= qualification <= 5):
        return jsonify({"error": "La calificación debe ser entre 1 y 5"}), 400

    calificacion_existente = Calificacion.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if calificacion_existente:
        calificacion_existente.qualification = qualification
        mensaje = "Calificación actualizada exitosamente"
    else:
        calificacion_existente = Calificacion(user_id=user_id, recipe_id=recipe_id, qualification=qualification)
        db.session.add(calificacion_existente)
        mensaje = "Calificación agregada exitosamente"
    
    db.session.commit()
    return jsonify({"message": mensaje, "calificacion": calificacion_existente.serialize()}), 200

@api.route('/calificaciones', methods=['DELETE'])
@jwt_required()
def eliminar_calificacion(calificacion_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    recipe_id = data.get('recipe_id')
    calificacion = Calificacion.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if not calificacion:
        return jsonify({"error": "Calificación no encontrada"}), 404

    db.session.delete(calificacion)
    db.session.commit()
    return jsonify({"message": "Calificación eliminada exitosamente"}), 200

@api.route('/calificaciones/promedio/<int:recipe_id>', methods=['GET'])
def obtener_promedio_calificacion(recipe_id):
    calificaciones = Calificacion.query.filter_by(recipe_id=recipe_id).all()
    if not calificaciones:
        return jsonify({"error": "No se encontraron calificaciones para esta receta"}), 404

    promedio = sum([cal.qualification for cal in calificaciones]) / len(calificaciones)
    return jsonify({"recipe_id": recipe_id, "promedio": round(promedio, 2)}), 200


