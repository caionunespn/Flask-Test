from flask import Flask, request, jsonify
import psycopg2, traceback, json
from collections import OrderedDict

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def raw(query, many):
    try:
        connection = psycopg2.connect(
            user="POSTGRES_USERNAME",
            password="POSTGRES_PASSWORD",
            host="127.0.0.1",
            port="5432",
            database="POSTGRES_DATABASE",
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        if cursor.rowcount > 0:
            if many is False:
                response = cursor.fetchone()
            elif many is True:
                response = cursor.fetchall()
            else:
                response = {}
            return response

    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
        return jsonify(error)

    finally:
        if connection:
            cursor.close()
            connection.close()


@app.route("/")
def hello_world():
    return jsonify("You're at index")


@app.route("/category", methods=["POST"])
def addCategory():
    data = request.json
    descricao = data["descricao"]
    insert_category_query = "INSERT INTO categoria (descricao) VALUES ('{0}') RETURNING id, descricao".format(
        descricao
    )

    try:
        result = raw(insert_category_query, False)
        data = {}
        data["id"] = result[0]
        data["descricao"] = result[1]
        return jsonify(data)

    except Exception as error:
        print(error)
        return jsonify(error)


@app.route("/category", methods=["GET"])
def listCategories():
    list_categories_query = "SELECT * FROM categoria order by id"
    try:
        result = raw(list_categories_query, True)
        data = {}
        for index, obj in enumerate(result):
            obj_data = {"id": obj[0], "descricao": obj[1]}
            data[index] = obj_data

        return jsonify(data)
    except Exception as error:
        print(error)
        return jsonify(error)


@app.route("/category/<id>", methods=["DELETE"])
def deleteCategory(id=None):
    delete_category_query = "DELETE FROM categoria where id={0}".format(id)

    try:
        result = raw(delete_category_query, None)
        return jsonify(result)
    except Exception as error:
        print(error)
        return jsonify(error)
