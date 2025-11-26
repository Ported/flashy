"""Gameplay screen for solving problems."""

import time

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from flashy.game import AnswerFeedback, GameController
from flashy.ui.voice import VoiceInput


class GameplayScreen(Screen):
    """Main gameplay screen for solving problems.

    Uses GameController to manage game logic - this screen just displays.
    """

    CSS = """
    GameplayScreen {
        align: center middle;
    }

    #game-box {
        width: 60;
        height: auto;
        border: double green;
        padding: 2;
    }

    #game-box.flash-correct {
        border: double lime;
    }

    #game-box.flash-incorrect {
        border: double red;
    }

    #game-box.boss-level {
        border: double red;
    }

    #level-title {
        text-align: center;
        text-style: bold;
        color: green;
        padding-bottom: 1;
    }

    #level-title.boss-title {
        color: red;
    }

    #timer {
        text-align: center;
        color: yellow;
        text-style: bold;
        padding: 1;
    }

    #timer.time-low {
        color: red;
    }

    #score-bar {
        text-align: center;
        padding: 1;
    }

    #progress {
        text-align: center;
        padding: 1;
    }

    #problem {
        text-align: center;
        text-style: bold;
        padding: 2;
    }

    #feedback {
        text-align: center;
        height: 2;
        padding: 1;
    }

    .correct {
        color: green;
    }

    .incorrect {
        color: red;
    }

    #voice-container {
        align: center middle;
        height: auto;
    }
    """

    def __init__(self, player_name: str, level_number: int) -> None:
        super().__init__()
        self.player_name = player_name
        self.level_number = level_number
        self.controller = GameController(player_name, level_number)
        self.problem_start_time = 0.0  # When current problem started
        self.level_start_time = 0.0  # When level started (for timed levels)
        self._timer_interval = None  # Timer update interval

    def compose(self) -> ComposeResult:
        level = self.controller.level
        is_boss = self.controller.is_timed

        yield Header()
        with Center():
            box_classes = "boss-level" if is_boss else ""
            with Vertical(id="game-box", classes=box_classes):
                title_classes = "boss-title" if is_boss else ""
                if is_boss:
                    title_text = f"⚔️ BOSS: {level.name} ⚔️"
                else:
                    title_text = f"Level {level.number}: {level.name}"
                yield Static(title_text, id="level-title", classes=title_classes)
                # Timer only shown for timed levels
                if is_boss:
                    yield Static("", id="timer")
                yield Static("Score: 0", id="score-bar")
                yield Static("", id="progress")
                yield Static("", id="problem")
                with Center(id="voice-container"):
                    yield Static("Starting...", id="voice-placeholder")
                yield Static("", id="feedback")
        yield Footer()

    def on_mount(self) -> None:
        """Start the level."""
        self.level_start_time = time.time()
        # Start timer updates for timed levels
        if self.controller.is_timed:
            self._refresh_timer()
            self._timer_interval = self.set_interval(1.0, self._refresh_timer)
        self._show_problem()

    def _refresh_timer(self) -> None:
        """Update the timer display and check for time expiry."""
        if not self.controller.is_timed:
            return

        elapsed = time.time() - self.level_start_time
        remaining = self.controller.time_remaining(elapsed)

        # Check if time expired
        if self.controller.is_time_expired(elapsed):
            self._time_expired()
            return

        # Update timer display
        timer = self.query_one("#timer", Static)
        mins = int(remaining) // 60
        secs = int(remaining) % 60
        timer.update(f"⏱️ {mins}:{secs:02d}")

        # Add warning style when low on time
        if remaining <= 15:
            timer.add_class("time-low")
        else:
            timer.remove_class("time-low")

    def _time_expired(self) -> None:
        """Handle time running out on a timed level."""
        # Stop the timer interval
        if self._timer_interval:
            self._timer_interval.stop()
            self._timer_interval = None

        # Finish the level (will get 0 stars due to incomplete)
        self._finish_level()

    def _show_problem(self) -> None:
        """Display the current problem."""
        problem = self.controller.current_problem
        if problem is None:
            self._finish_level()
            return

        # Update progress display
        self._update_progress()
        self._update_score_bar()

        # Show problem
        problem_text = f"[bold]{problem.display()} = ?[/bold]"
        self.query_one("#problem", Static).update(problem_text)

        # Start timing for this problem
        self.problem_start_time = time.time()

        # Mount fresh voice input for this problem
        container = self.query_one("#voice-container")
        container.remove_children()
        container.mount(VoiceInput(expected=problem.answer))

    def _update_progress(self) -> None:
        """Update the progress dots display."""
        progress_parts = []
        for i in range(self.controller.total_problems):
            if i < len(self.controller.results):
                if self.controller.results[i].is_correct:
                    progress_parts.append("[green]●[/]")
                else:
                    progress_parts.append("[red]●[/]")
            elif i == self.controller.problem_index:
                progress_parts.append("◉")
            else:
                progress_parts.append("○")
        progress_str = " ".join(progress_parts)
        self.query_one("#progress", Static).update(progress_str)

    def _update_score_bar(self) -> None:
        """Update the score bar with score and streak."""
        score_text = f"Score: {self.controller.total_score}"
        if self.controller.streak >= 2:
            score_text += f"  |  🔥 {self.controller.streak} streak!"
        self.query_one("#score-bar", Static).update(score_text)

    @on(VoiceInput.AnswerReceived)
    def on_voice_answer(self, event: VoiceInput.AnswerReceived) -> None:
        """Handle voice input answer."""
        # Calculate time taken for this problem
        problem_time = time.time() - self.problem_start_time

        # Submit to controller
        feedback = self.controller.submit_answer(event.answer, problem_time)

        # Show feedback
        self._show_feedback(feedback)

        # Update displays
        self._update_progress()
        self._update_score_bar()

        # Flash border
        game_box = self.query_one("#game-box")
        if feedback.is_correct:
            game_box.add_class("flash-correct")
        else:
            game_box.add_class("flash-incorrect")

        # Remove flash and show next problem after delay
        self.set_timer(0.3, self._next_problem)

    def _show_feedback(self, feedback: AnswerFeedback) -> None:
        """Update the feedback display based on answer result."""
        feedback_widget = self.query_one("#feedback", Static)

        if feedback.is_correct:
            if feedback.points_earned > 0:
                text = f"✓ Correct! +{feedback.points_earned} pts"
            else:
                text = "✓ Correct!"
            feedback_widget.update(text)
            feedback_widget.add_class("correct")
            feedback_widget.remove_class("incorrect")
        else:
            text = f"✗ Nope! Answer: {feedback.correct_answer}"
            feedback_widget.update(text)
            feedback_widget.add_class("incorrect")
            feedback_widget.remove_class("correct")

    def _next_problem(self) -> None:
        """Remove flash and show next problem."""
        game_box = self.query_one("#game-box")
        game_box.remove_class("flash-correct")
        game_box.remove_class("flash-incorrect")
        self._show_problem()

    def _finish_level(self) -> None:
        """Finish the level and show results."""
        from flashy.ui.screens.result import ResultScreen

        # Stop timer if running
        if self._timer_interval:
            self._timer_interval.stop()
            self._timer_interval = None

        # Finish via controller (saves progress and history)
        stars, is_new_best = self.controller.finish()

        # Show results screen
        self.app.pop_screen()
        self.app.push_screen(
            ResultScreen(
                self.player_name,
                self.level_number,
                self.controller.correct_count,
                self.controller.total_problems,
                stars,
                is_new_best,
                self.controller.total_score,
                self.controller.best_streak,
            )
        )
