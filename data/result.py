import json
from datetime import datetime

def generate_json_results(model_id, model_settings, cow_results):
    data = {
        f"model_{model_id}": {
            "model_settings": {
                "date_model": datetime.now().strftime("%Y-%m-%d-%H-%M"),
                "number_cow": model_settings["number_cow"],
                "nb_box": model_settings["nb_box"],
                "percentage_water": model_settings["percentage_water"]
            },
            "info_cows": {}
        }
    }

    for cow_id, cow_info in cow_results.items():
        cow_data = {
            f"cow_{cow_id}": {
                "death_cause": cow_info["death_cause"],
                "turn_milkings": cow_info["turn_milkings"]
            }
        }
        data[f"model_{model_id}"]["info_cows"].update(cow_data)

    return json.dumps(data, indent=4)