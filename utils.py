import re
import json


def extractJson(llmOutput:str):
    llmOutput = llmOutput[llmOutput.rfind("JSON:"):]
    try:
        llmOutput = re.sub("\n", "", llmOutput)
        start = llmOutput.find("{")
        end = llmOutput.rfind("}") + 1
        llmOutput = llmOutput[start:end] if start != -1 and end != 0 else ""
        return json.loads(llmOutput)
    except:
        print("[Warrning] LLM returned not Json format:")
        print(llmOutput)
        return llmOutput

def initialize_model():
    pass