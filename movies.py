class movies(dict):
    
    def __init__(self):
        self.dict = dict()
        self.message = ""
    
    def add(self,index,title,url):
        self.dict[index] = {}
        self.dict[index]['title'] = title
        self.dict[index]['url'] = url
    
    def build_message(self):
        i = 1
        while i <= 10:
            try:
                self.message += "{}.{}\n".format(i,self.dict[i]['title'])
                i += 1
            except:
                break
        self.message += "\nEnter your choice"
        return self.message

    def get_url(self,index):
        return self.dict[index]['url']

    def reset(self):
        self.dict = {}
        self.message = ""