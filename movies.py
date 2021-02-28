"""Dictionary to store torrent details."""


class movies(dict):
    """Handle dictionary functions."""

    def __init__(self):
        """Initialize."""
        self.dict = dict()
        self.message = ""

    def add(self, index, title, url, seeds):
        """Add details."""
        self.dict[index] = {}
        self.dict[index]['title'] = title
        self.dict[index]['url'] = url
        self.dict[index]['seeds'] = seeds

    def build_message(self):
        """Build search results."""
        i = 1

        while i <= 10:
            try:
                seeds = self.dict[i]['seeds']
                title = self.dict[i]['title']
                # Building message based on seeds.
                if not seeds:
                    self.message += f"{i}.{title}\n"
                else:
                    self.message += f"{i}.{title} seeds:{seeds}\n"
                i += 1
            except Exception as e:
                print(e)
                break

        self.message += "\nEnter your choice"
        return self.message

    def get_url(self, index):
        """Return url."""
        return self.dict[index]['url']

    def get_title(self, index):
        """Return title."""
        return self.dict[index]['title']

    def get_seeds(self, index):
        """Return seeds."""
        return self.dict[index]['seeds']

    def reset(self):
        """Reset dictionary."""
        self.dict = {}
        self.message = ""
