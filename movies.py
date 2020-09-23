class movies(dict):
    
    def __init__(self):
        self.dict = dict()
        self.message = ""
    
    def add(self,index,title,url,seeds):
        self.dict[index] = {}
        self.dict[index]['title'] = title
        self.dict[index]['url'] = url
        self.dict[index]['seeds'] = seeds
    
    def build_message(self):
        i = 1
        while i <= 10:
            try:
                seeds = self.dict[i]['seeds']
                if not seeds:
                    self.message += "{}.{}\n".format(i,self.dict[i]['title'])
                else:
                    self.message += "{}.{} seeds:{}\n".format(i,self.dict[i]['title'],seeds)
                i += 1
            except:
                break
        self.message += "\nEnter your choice"
        return self.message

    def get_url(self,index):
        return self.dict[index]['url']
    
    def get_title(self,index):
        return self.dict[index]['title']
    
    def get_seeds(self,index):
        return self.dict[index]['seeds']

    def reset(self):
        self.dict = {}
        self.message = ""