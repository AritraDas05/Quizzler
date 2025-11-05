from problems_bank_abstract import ProblemBank
from problems_bank_opentb import OpenTBProblemBank

def load_and_show_questions(bank: ProblemBank):
    bank.load_questions()
    print(f"Loaded {len(bank.questions)} questions.")
    print("First question:", bank.get_question(0)["question"])

if __name__ == "__main__":
    parameters = {"amount": 5, "type": "multiple", "category": 19}

    problem_bank = OpenTBProblemBank(parameters)

    load_and_show_questions(problem_bank)
