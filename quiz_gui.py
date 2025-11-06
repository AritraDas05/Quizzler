import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from game_controller import GameController
from question_manager import QuestionManager
from problems_bank_opentb import OpenTBProblemBank
from game_modes import SinglePlayerMode, MultiPlayerMode
from strategies import (AdaptiveDifficultyStrategy, StaticDifficultyStrategy,
                        BasicScoringStrategy, TimeBonusScoringStrategy)
from interfaces import IView


class BaseView(IView):
    """Base view class (Template Method Pattern)"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.frame: Optional[tk.Frame] = None

    def show(self) -> None:
        if self.frame:
            self.frame.pack(expand=True, fill='both')

    def hide(self) -> None:
        if self.frame:
            self.frame.pack_forget()

    def destroy(self) -> None:
        if self.frame:
            self.frame.destroy()
            self.frame = None


class QuizGUI:
    """Main GUI - uses dependency injection (Dependency Inversion)"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Adaptive Quiz Application - OOP Design")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.controller: Optional[GameController] = None
        self.selected_answer = tk.StringVar()
        self.timer_seconds = 30
        self.timer_id: Optional[str] = None
        self.start_time = 0

        self._setup_styles()
        self._show_main_menu()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Title.TLabel', font=('Helvetica', 28, 'bold'),
                        background='#2C3E50', foreground='white')
        style.configure('Subtitle.TLabel', font=('Helvetica', 14),
                        background='#2C3E50', foreground='white')
        style.configure('Question.TLabel', font=('Helvetica', 14, 'bold'),
                        wraplength=700, justify='left')

    def _clear_window(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def _show_main_menu(self) -> None:
        self._clear_window()

        header_frame = tk.Frame(self.root, bg='#2C3E50', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        ttk.Label(header_frame, text="🎯 SOLID Quiz Master",
                  style='Title.TLabel').pack(pady=20)

        menu_frame = tk.Frame(self.root, bg='white')
        menu_frame.pack(expand=True, fill='both', padx=50, pady=50)

        ttk.Label(menu_frame, text="Select Game Mode",
                  font=('Helvetica', 18, 'bold')).pack(pady=20)

        btn_frame = tk.Frame(menu_frame, bg='white')
        btn_frame.pack(expand=True)

        tk.Button(btn_frame, text="Single Player\n(Adaptive Difficulty)",
                  font=('Helvetica', 12, 'bold'),
                  bg='#3498DB', fg='white', width=25, height=3,
                  command=self._start_single_player).pack(pady=10)

        tk.Button(btn_frame, text="Multiplayer\n(2-4 Players)",
                  font=('Helvetica', 12, 'bold'),
                  bg='#E74C3C', fg='white', width=25, height=3,
                  command=self._show_multiplayer_setup).pack(pady=10)

        tk.Button(btn_frame, text="Exit", font=('Helvetica', 12),
                  bg='#95A5A6', fg='white', width=25, height=2,
                  command=self.root.quit).pack(pady=10)

    def _start_single_player(self) -> None:
        """Create single player game using dependency injection"""
        try:
            # Create dependencies
            parameters = {'amount': 20, 'type': 'multiple', 'difficulty': 'easy'}
            problem_bank = OpenTBProblemBank(parameters)
            question_manager = QuestionManager(problem_bank)

            # Create strategies
            difficulty_strategy = AdaptiveDifficultyStrategy()
            scoring_strategy = TimeBonusScoringStrategy()

            # Create game mode
            game_mode = SinglePlayerMode(difficulty_strategy, scoring_strategy)

            # Inject dependencies into controller
            self.controller = GameController(game_mode, question_manager)
            self.controller.start_game()

            self._show_quiz()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start game: {str(e)}")
            self._show_main_menu()

    def _show_multiplayer_setup(self) -> None:
        self._clear_window()

        header_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        ttk.Label(header_frame, text="Multiplayer Setup",
                  style='Title.TLabel').pack(pady=15)

        setup_frame = tk.Frame(self.root, bg='white')
        setup_frame.pack(expand=True, fill='both', padx=50, pady=30)

        ttk.Label(setup_frame, text="Number of Players (2-4):",
                  font=('Helvetica', 12)).pack(pady=10)

        num_players_var = tk.IntVar(value=2)
        tk.Spinbox(setup_frame, from_=2, to=4, textvariable=num_players_var,
                   font=('Helvetica', 12), width=10).pack(pady=5)

        names_frame = tk.Frame(setup_frame, bg='white')
        names_frame.pack(pady=20)

        name_entries = []
        for i in range(4):
            frame = tk.Frame(names_frame, bg='white')
            frame.pack(pady=5)
            ttk.Label(frame, text=f"Player {i + 1} Name:",
                      font=('Helvetica', 11)).pack(side='left', padx=5)
            entry = tk.Entry(frame, font=('Helvetica', 11), width=20)
            entry.insert(0, f"Player {i + 1}")
            entry.pack(side='left', padx=5)
            name_entries.append(entry)

        def start_multiplayer():
            try:
                num = num_players_var.get()

                # Create dependencies
                parameters = {'amount': 30, 'type': 'multiple', 'difficulty': 'easy'}
                problem_bank = OpenTBProblemBank(parameters)
                question_manager = QuestionManager(problem_bank)

                # Create strategies
                difficulty_strategy = AdaptiveDifficultyStrategy()
                scoring_strategy = BasicScoringStrategy()

                # Create game mode with player count
                game_mode = MultiPlayerMode(num, difficulty_strategy, scoring_strategy)

                # Inject dependencies
                self.controller = GameController(game_mode, question_manager)
                self.controller.start_game()

                # Set player names
                for i in range(num):
                    name = name_entries[i].get().strip()
                    if name:
                        game_mode.set_player_name(i, name)

                self._show_quiz()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start game: {str(e)}")

        button_frame = tk.Frame(setup_frame, bg='white')
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Start Game",
                  font=('Helvetica', 12, 'bold'),
                  bg='#27AE60', fg='white', width=15, height=2,
                  command=start_multiplayer).pack(side='left', padx=10)

        tk.Button(button_frame, text="Back", font=('Helvetica', 12),
                  bg='#95A5A6', fg='white', width=15, height=2,
                  command=self._show_main_menu).pack(side='left', padx=10)

    def _show_quiz(self) -> None:
        self._clear_window()
        self.selected_answer.set("")

        import time
        self.start_time = time.time()

        # Header with scores
        header_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        current_player = self.controller.get_current_player()
        game_mode = self.controller.get_game_mode()

        if hasattr(game_mode, 'get_all_players'):
            # Multiplayer
            players = game_mode.get_all_players()
            score_text = " | ".join([f"{p.get_name()}: {p.get_score()}"
                                     for p in players])
        else:
            # Single player
            score_text = f"{current_player.get_name()}: {current_player.get_score()} pts"

        ttk.Label(header_frame, text=score_text,
                  style='Subtitle.TLabel').pack(pady=25)

        # Question frame
        question_frame = tk.Frame(self.root, bg='white')
        question_frame.pack(expand=True, fill='both', padx=30, pady=20)

        # Info bar
        info_frame = tk.Frame(question_frame, bg='white')
        info_frame.pack(fill='x', pady=5)

        self.timer_label = ttk.Label(info_frame, text=f"Time: {self.timer_seconds}s",
                                     font=('Helvetica', 14, 'bold'),
                                     foreground='red')
        self.timer_label.pack(side='right')

        difficulty = self.controller.get_current_difficulty()
        ttk.Label(info_frame,
                  text=f"Difficulty: {difficulty.upper()} | Current Player: {current_player.get_name()}",
                  font=('Helvetica', 11, 'bold'),
                  foreground='#8E44AD').pack(side='left')

        # Question
        question = self.controller.get_current_question()
        if not question:
            self._show_results()
            return

        ttk.Label(question_frame, text=question.get_text(),
                  style='Question.TLabel').pack(pady=20, anchor='w')

        # Options
        options_frame = tk.Frame(question_frame, bg='white')
        options_frame.pack(fill='both', expand=True, pady=10)

        options = self.controller.get_shuffled_options()
        for option in options:
            tk.Radiobutton(options_frame, text=option,
                           variable=self.selected_answer, value=option,
                           font=('Helvetica', 11), bg='white',
                           activebackground='#ECF0F1',
                           selectcolor='#3498DB').pack(anchor='w', pady=8, padx=20)

        tk.Button(question_frame, text="Submit Answer",
                  font=('Helvetica', 12, 'bold'),
                  bg='#27AE60', fg='white', width=20, height=2,
                  command=self._submit_answer).pack(pady=20)

        self.timer_seconds = 30
        self._update_timer()

    def _update_timer(self) -> None:
        if self.timer_seconds > 0:
            self.timer_label.config(text=f"Time: {self.timer_seconds}s")
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self._update_timer)
        else:
            self._time_up()

    def _time_up(self) -> None:
        messagebox.showwarning("Time's Up!", "You ran out of time!")
        self.controller.submit_answer("", 30)
        self._next_question_or_end()

    def _submit_answer(self) -> None:
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        answer = self.selected_answer.get()
        if not answer:
            messagebox.showwarning("No Answer", "Please select an answer!")
            self._update_timer()
            return

        import time
        time_taken = int(time.time() - self.start_time)

        is_correct, points = self.controller.submit_answer(answer, time_taken)

        if is_correct:
            messagebox.showinfo("Correct! ✓", f"Great job! +{points} points")
        else:
            correct = self.controller.get_current_question().get_correct_answer()
            messagebox.showerror("Incorrect ✗", f"The correct answer was: {correct}")

        self._next_question_or_end()

    def _next_question_or_end(self) -> None:
        if self.controller.is_game_over():
            self._show_results()
        elif self.controller.next_question():
            self._show_quiz()
        else:
            self._show_results()

    def _show_results(self) -> None:
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self._clear_window()

        header_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        ttk.Label(header_frame, text="🏆 Results",
                  style='Title.TLabel').pack(pady=15)

        results_frame = tk.Frame(self.root, bg='white')
        results_frame.pack(expand=True, fill='both', padx=50, pady=30)

        results = self.controller.get_results()

        if results['mode'] == 'single_player':
            stats = results['player']
            ttk.Label(results_frame,
                      text=f"Final Score: {stats['score']}",
                      font=('Helvetica', 24, 'bold')).pack(pady=20)

            ttk.Label(results_frame,
                      text=f"Accuracy: {stats['accuracy'] * 100:.1f}%",
                      font=('Helvetica', 16)).pack(pady=10)
        else:
            ttk.Label(results_frame, text="Leaderboard",
                      font=('Helvetica', 20, 'bold')).pack(pady=20)

            medals = ["🥇", "🥈", "🥉"]
            for i, stats in enumerate(results['players']):
                medal = medals[i] if i < 3 else f"{i + 1}."
                text = f"{medal} {stats['name']}: {stats['score']} pts ({stats['accuracy'] * 100:.1f}%)"
                ttk.Label(results_frame, text=text,
                          font=('Helvetica', 14)).pack(pady=8)

        button_frame = tk.Frame(results_frame, bg='white')
        button_frame.pack(pady=30)

        tk.Button(button_frame, text="Main Menu",
                  font=('Helvetica', 12), bg='#95A5A6', fg='white',
                  width=15, height=2,
                  command=self._show_main_menu).pack(side='left', padx=10)


def main():
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
