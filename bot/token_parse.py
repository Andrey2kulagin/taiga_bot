import base64
import json


async def parse_user_id(token):
    # делим токен по частям, нам нужна вторая
    token_parts = token.split(".")
    # декодим, и чтобы функция не ругалась на длину строки - срем лишним к конец строки. Этот костыль даст знать о себе,
    # если размер этой части токена изменится
    decoded_part = base64.b64decode(token_parts[1] + "b==")
    # переводим байтики в юникод
    decoded_part = decoded_part.decode("utf-8")
    # мусор который мы оставили все еще в строке, ищем, где закрывается объект
    end_index = decoded_part.find('}') + 1
    # отсекаем все что после объекта
    decoded_part = decoded_part[:end_index]
    # пихаем в словарь
    print(decoded_part)
    decoded_dict = json.loads(decoded_part)
    # возвращаем id
    print(decoded_dict)
    return decoded_dict["user_id"]
