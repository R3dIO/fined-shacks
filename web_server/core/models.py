import logging

from pymongo import errors

from web_server import mongo

logger = logging.getLogger(__name__)


class User:
    def __init__(self, uid, email, tags):
        self.uid = uid
        self.email = email
        self.tags = tags if tags else []


def save_user(uid, email):
    try:
        result = mongo.db.users.insert_one({'uid': uid, 'email': email})
    except errors.OperationFailure as e:
        logger.debug(e)
        return e.details.get("errmsg")
    except:
        raise


def update_user_tags(email, tags):
    try:
        result = mongo.db.users.update_one({'email': email, 'tags': tags})
    except errors.OperationFailure as e:
        logger.debug(e)
        return e.details.get("errmsg")
    except:
        raise


class Content:
    TYPE = "content"

    def __init__(self, article_url, title, excerpt, url_image):
        self.type = self.TYPE
        self.url = article_url
        self.title = title
        self.excerpt = excerpt
        self.url_image = url_image

    def create_mongo_document(self):
        return {
            'type': self.TYPE, 'url': self.url, 'title': self.title, 'url_image': self.url_image
        }


def save_content(content: Content):
    try:
        result = mongo.db.content.insert_one(content.create_mongo_document())
    except errors.OperationFailure as e:
        logger.debug(e)
        return e.details.get("errmsg")
    except:
        raise


def fetch_content(tags, page, per_page):
    try:
        skip_count = (page - 1) * per_page

        matched_content = mongo.db.content.aggregate([
                    {
                        '$match': {
                            'tags': {
                                '$in': tags
                            }
                        }
                    },
                    {'$skip': skip_count},
                    {'$limit': per_page},
                    {'$project': {'_id': 0, 'type': 1, 'title': 1, 'url': 1, 'excerpt': 1, 'url_image': 1}}
                ])
        # sorting
        articles.sort(key=lambda x: x['creation_date'], reverse=True)
        articles = truncate_descriptions(articles)
        return articles
    except errors.OperationFailure as e:
        app.logger.error(e)
        app.logger.debug(traceback.format_exc())
        return e.details.get("errmsg")
    except Exception as e:
        print(traceback.format_exc())
        app.logger.error(e)
        app.logger.debug(traceback.format_exc())
        return None