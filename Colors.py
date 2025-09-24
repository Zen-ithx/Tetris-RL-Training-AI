class Colors:
    cyan   = (0, 255, 255)
    yellow = (255, 255, 0)   
    purple = (128, 0, 128)
    red    = (255, 0, 0)
    blue   = (0, 0, 255)
    orange = (255, 127, 0)  
    grey   = (50, 50, 50) 
    green  = (0, 255, 0)
    
    
    @classmethod
    def get_cell_colors(cls):
        return [cls.grey,cls.green,cls.red,cls.orange,cls.yellow,cls.purple,cls.cyan,cls.blue]
    
    
    
    