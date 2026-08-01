import random
import time

import config

from seleniumbase import SB


class Browser:

    def __init__(self):
        self._sb = None
        self.sb = None

    def __enter__(self):
        self._sb = SB(
            uc=True,
            headless=config.HEADLESS,
        )
        self.sb = self._sb.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._sb is not None:
            self._sb.__exit__(
                exc_type,
                exc_value,
                traceback,
            )
            self._sb = None
            self.sb = None

    def restart(self):
        """Restart the underlying SeleniumBase SB driver in-place."""
        try:
            # Attempt a clean quit first
            if self._sb is not None:
                try:
                    quit_method = getattr(self.sb, "quit", None)
                    if callable(quit_method):
                        quit_method()
                except Exception:
                    pass

                try:
                    self._sb.__exit__(None, None, None)
                except Exception:
                    pass

            # Create a fresh SB instance
            self._sb = SB(uc=True, headless=config.HEADLESS)
            self.sb = self._sb.__enter__()
        except Exception:
            # If restart fails, ensure internal refs are cleared
            self._sb = None
            self.sb = None

    def ensure_alive(self):
        """Return True if driver appears responsive, else restart and return False."""
        if self.sb is None:
            self.restart()
            return False
        try:
            # quick probe
            _ = self.sb.get_current_url()
            return True
        except Exception:
            self.restart()
            return False

    def driver(self):
        return self.sb

    def random_delay(self):
        delay = random.uniform(
            config.REQUEST_DELAY_MIN,
            config.REQUEST_DELAY_MAX,
        )
        time.sleep(delay)

    def wait(self, seconds):
        if self.sb is None:
            return
        self.sb.sleep(seconds)

    def solve_cloudflare(self):
        if self.sb is None:
            return
        try:
            self.sb.uc_gui_handle_captcha()
        except Exception:
            pass

    def open(self, url):
        if self.sb is None:
            raise RuntimeError("Browser is not initialized")

        self.random_delay()

        self.sb.uc_open_with_reconnect(
            url,
            reconnect_time=3,
        )

        title = self.sb.get_title()

        if (
            "Just a moment" in title
            or "Attention Required" in title
        ):
            print("Cloudflare detected. Solving...")
            self.solve_cloudflare()

        self.sb.wait_for_ready_state_complete()

    def refresh(self):
        if self.sb is None:
            return

        self.sb.refresh()
        title = self.sb.get_title()

        if (
            "Just a moment" in title
            or "Attention Required" in title
        ):
            print("Cloudflare detected. Solving...")
            self.solve_cloudflare()

        self.sb.wait_for_ready_state_complete()

    def html(self):
        if self.sb is None:
            return ""
        return self.sb.get_page_source()

    def title(self):
        if self.sb is None:
            return ""
        return self.sb.get_title()

    def current_url(self):
        if self.sb is None:
            return ""
        return self.sb.get_current_url()

    def screenshot(self, path):
        if self.sb is None:
            return
        self.sb.save_screenshot(path)

    def quit(self):
        if self.sb is None:
            return
        quit_method = getattr(self.sb, "quit", None)
        if callable(quit_method):
            quit_method()