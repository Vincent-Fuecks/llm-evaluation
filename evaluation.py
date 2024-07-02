from utils import extractJson
from answer_relevancy.templates import generate_statements, generate_verdicts, generate_reason
from answer_facts_correctness.templates import generate_facts, generate_facts_evaluation

def finetuneModelEvaluation(pipe, question, groundTruthAnswer, llmAnswer, score):
    # Answer Relevancy Score
    anserRelevancyScore = None
    statements = extractJson(pipe(generate_statements(llmAnswer))[0]['generated_text'])
    verdicts =  extractJson(pipe(generate_verdicts(question, statements))[0]['generated_text'])
    generateReasonDic = extractJson(pipe(generate_reason(verdicts, question, score))[0]['generated_text'])
    try:
        anserRelevancyScore = generateReasonDic["score"]
        print("Answer Relevancy Score: ", (generateReasonDic["score"]))
    except:
        print("[ERROR] LLM returned non-json format.")

    # Answer Facts Correctness
    answerFactsCorrectnessScore = None
    generatedFacts = extractJson(pipe(generate_facts(llmAnswer))[0]['generated_text'])
    generatedgroundTruthFacts= extractJson(pipe(generate_facts(groundTruthAnswer))[0]['generated_text'])
    answerCorrectnissEvaluationDic = extractJson(pipe(generate_facts_evaluation(generatedFacts, generatedgroundTruthFacts))[0]['generated_text'])

    try:
        score = min(((len(generatedgroundTruthFacts["facts"]) - answerCorrectnissEvaluationDic["total_score"])/len(generatedgroundTruthFacts["facts"]))*10, 10)
        answerFactsCorrectnessScore = score
        print("Answer Facts Correctness Score: ", score)
    except:
        print("[ERROR] LLM returned non-json format.")
    
    return (anserRelevancyScore, answerFactsCorrectnessScore)

