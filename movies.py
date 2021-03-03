"""Dictionary to store torrent details."""


class movies(dict):
    """Handle dictionary functions."""

    def __init__(self):
        """Initialize."""
        self.dict = dict()
        self.message = ""

    def chatid(self, chatid):
        """Create unique dictionary."""
        self.dict[chatid] = {}

    def add(self, chatid, index, title, url, seeds):
        """Add details."""
        self.dict[chatid][index] = {}
        self.dict[chatid][index]['title'] = title
        self.dict[chatid][index]['url'] = url
        self.dict[chatid][index]['seeds'] = seeds

    def build_message(self, chatid):
        """Build search results."""
        i = 1

        while i <= 15:
            try:
                seeds = self.dict[chatid][i]['seeds']
                title = self.dict[chatid][i]['title']

                # Building message based on seeds.
                if not seeds:
                    self.message += f"{i}.{title}\n"
                else:
                    self.message += f"{i}.{title} seeds:*{seeds}*\n"
                i += 1
            except Exception as e:
                print(e)
                break
        self.message += "\nEnter your choice"
        return self.message

    def get_url(self, chatid, index):
        """Return url."""
        return self.dict[chatid][index]['url']

    def get_title(self, chatid, index):
        """Return title."""
        return self.dict[chatid][index]['title']

    def get_seeds(self, chatid, index):
        """Return seeds."""
        return self.dict[chatid][index]['seeds']

    def reset(self, chatid):
        """Reset dictionary."""
        self.dict[chatid] = {}
        self.message = ""
