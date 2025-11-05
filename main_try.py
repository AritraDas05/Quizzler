# main.py
from problems_bank_abstract import ProblemBank
from problems_bank_opentb import OpenTBProblemBank
# In the future, you could also have:
# from problems_bank_local import LocalProblemBank

def load_and_show_questions(bank: ProblemBank):
    bank.load_questions()
    print(f"Loaded {len(bank.questions)} questions.")
    print("First question:", bank.get_question(0)["question"])

if __name__ == "__main__":
    parameters = {"amount": 5, "type": "multiple", "category": 19}

    # You can swap this line and everything else still works:
    problem_bank = OpenTBProblemBank(parameters)
    # problem_bank = LocalProblemBank("data/questions.json")  # also valid later

    # Pass it as a ProblemBank (abstraction, not concrete type)
    load_and_show_questions(problem_bank)
