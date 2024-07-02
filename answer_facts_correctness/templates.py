def generate_facts(naturalLanguageMessage):
        return f"""Given a natural language message as input, generate a JSON object that extracts factual statements according to the following guidelines:
(1) A factual statement is considered objective and verifiable through evidence.
(2) Opinions, beliefs, and hypotheticals should be ignored.
(3) Negations should be converted to positive statements (e.g., "The car was not red" becomes "The car had a color other than red").
(4) Focus on explicitly stated facts in the message. Do not make inferences or assumptions about unstated information (e.g., the existence of an engine based on "gasoline-powered").

The JSON object will have the following structure:
facts (array): This array will contain string objects which are exact factual statements extracted from the message.

**
IMPORTANT: Please make sure to only return in JSON format.
IMPORTANT: You should NOT incorporate any prior knowledge you have and take the presented facts in the input at face value.
Example Natural Language Message: The first gasoline-powered car was invented by Karl Benz in 1886. It had three wheels and reached a top speed of 16 kilometers per hour.
Example JSON:
{{
  "facts": [
        "The first gasoline-powered car was invented by Karl Benz.",
        "The car was invented in 1886.",
        "The car had three wheels.",
        "The car reached a top speed of 16 kilometers per hour."
  ]
}}
**

Natural Language Message:
{naturalLanguageMessage}

JSON:
"""

def generate_facts_evaluation(generatedFacts, groundTruthFacts):
        return f"""Given the following question, ground truth facts and generated facts, evaluate the generated facts based on following guidelines:
(1) Non-Contradiction: Analyze both ground truth facts and generated facts to identify any factual statements that directly contradict each other, add for every contradiction fact 2 to the total score.
(2) Missing Facts: Analyze both ground truth facts and generated facts to identify any missing facts in generated facts compared to ground truth facts, add for every missing fact 1 to the total score.
(3) Relevant Addition: If a generated fact contains additional information relevant to the question and not present in the ground truth, add for every additional fact -0.25 to the total score.
(4) Irrelevant Fact (Maximum 1 Points): If a generated fact contains additional information irrelevant to the question, add for every irrelevant fact 0.25 to the total score.

The Count starts by zero.
Fact Comparison Logic: Use a fuzzy matching approach to compare facts, allowing for synonyms and paraphrases with a confidence score (0-1). Facts with a higher confidence score of similarity have a greater impact on the evaluation.

Generate a JSON object containing:
"subcategory": A Dictionary explaining the reason for the subcategory scores including Non-Contradiction, Missing Facts, Relevant Addition and Irrelevant Information with the coresonding subcategory score.
"total_score": The final score (between 0 and 10) calculated based on the points of every guideline point.

**
IMPORTANT: Please make sure to only return in JSON format.
Example Question: When and how was the first gasoline-powered car invented?
Example Ground Truth Facts: {{ "facts": [ "The first gasoline-powered car was invented by Karl Benz.", "The car was invented in 1886.", "The car had three wheels."] }}
Example Generated Facts: {{ "facts": [ "Karl Benz invented the first gasoline-powered car.", "The car was invented in 1900.", "The legal age for driving is 18 years in Germany", "The car reached a top speed of 16 kilometers per hour." ] }}
Example JSON:
{{
  "subcategory": {{
      "non-contradiction": {{
        "reason": "Number of contradicting facts 1 (invention year (1886 vs 1900))",
        "score": 2
      }},
      "missing-facts": {{
        "reason": "Number of Missing facts 1 (The car had three wheels.)",
        "score": 1
      }},
      "relevant-addition": {{
        "reason": "Relevant Addition: One relevant addition found. Generated fact includes the top speed (16 kilometers per hour) which is not present in ground truth facts.",
        "score": -0.25
      }},
     "irrelevant-fact": {{
        "reason": "Irrelevant Information: One irrelevant addition found. Generated fact includes the legal driving age in Germany (18 years) which is irrelevant to the question.",
        "score": 0.25
      }}
    }},
  "total_score": 3
}}
**

Ground Truth Facts:
{groundTruthFacts}

Generated Facts:
{generatedFacts}

JSON:
"""