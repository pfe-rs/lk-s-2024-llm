# Class to parse model outputs

import json
import re

class Output_parser():
    @staticmethod
    def find_json(text):
        pattern = r"""```json(.*?)```"""
        matches=re.findall(pattern,text,re.DOTALL)
        assert len(matches) > 0 
        return matches[0]
    @staticmethod
    def json_to_list(json_code):
        parsed_json=json.loads(json_code)
        if 'key_phrases' in parsed_json:
            return parsed_json["key_phrases"]
        elif 'keyphrases' in parsed_json:
            return parsed_json["keyphrases"]
        elif 'key_phrase' in parsed_json:
            return parsed_json["key_phrase"]
        elif 'keyphrase' in parsed_json:
            return parsed_json["keyphrase"]
        elif isinstance(parsed_json, list):
            return parsed_json
        else:
            print("Bad json output")
            print(parsed_json)
            raise Exception("json is not correctly written")
    @staticmethod
    def output_to_list(output):
        return Output_parser.json_to_list(Output_parser.find_json(output))