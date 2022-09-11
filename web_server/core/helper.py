from ..common.constants import STR_CATEGORY_TAGS

def categorize_annual_income(form_json):
    if "income" in form_json:
        income = form_json["income"]
        if income <= 20000:
            return "low_income"
        elif 20000 < income < 50000:
            return "medium_income"
        else:
            return "excellent_income"
    else:
        return "no_income"

def categorize_amount_invested(form_json):
    if "amount_invested" in form_json:
        invested = form_json["amount_invested"]
        if invested <= 100:
            return "low_amount_invested"
        elif 1000 < invested < 3500:
            return "medium_amount_invested"
        else:
            return "excellent_amount_invested"
    else:
        return "no_amount_invested"


def categorize_age(form_json):
    if "age" in form_json:
        age = form_json["age"]
        if age < 18:
            return "teen"
        elif 18 <= age < 25:
            return "young_adult"
        elif 25 <= age < 40:
            return "adult"
        elif 40 <= age < 60:
            return "elder"
        else:
            return "grandpeople"


def categorize_credit_cards_issues(form_json):
    if "credit_cards_issued" in form_json:
        cards = form_json["credit_cards_issued"]
        if cards == 1:
            return "low_credit_cards_issued"
        elif 1 < cards <= 3:
            return "medium_credit_cards_issued"
        elif cards >= 4:
            return "high_credit_card_issued"
    else:
        return "no_credit_cards_issued"


def categorize_credit_score(form_json):
    if "credit_score" in form_json:
        return form_json["credit_score"].lower() + "_credit_score"
    else:
        return "no_credit_score"


def categorize_health_insurance(form_json):
    if "health_insurance" in form_json and form_json["health_insurance"]:
        return "health_insurance_present"
    else:
        return "health_insurance_absent"


def add_city(form_json):
    if "city" in form_json and isinstance(form_json["city"], str):
        city = form_json["city"]
        city = city.lower().strip()
        if city:
            return "city_{0}".format(city)
        else:
            return "city_present"

def categorize(form_json):
    final_user_tags = set()
    final_user_tags.add(categorize_annual_income(form_json))
    final_user_tags.add(categorize_age(form_json))
    final_user_tags.add(categorize_credit_score(form_json))
    final_user_tags.add(categorize_health_insurance(form_json))
    final_user_tags.add(add_city(form_json))

    final_user_tags.update(["_".join(form_json[key].replace(" ","").lower().split()) for key in STR_CATEGORY_TAGS])
    return final_user_tags

def generate_tags_from_form(form_json):
    final_user_tags = categorize(form_json)

    print(final_user_tags)
    return final_user_tags

# if __name__ == '__main__':
#     generate_tags_from_form(example)
