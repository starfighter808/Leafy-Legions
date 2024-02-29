import pygame as pg

class Battle_Map():
   
    def __init__(self, battle_data, map_image):
        self.Battle_points = []
        self.Path1 = []
        self.Path2 = []
        self.Path3 = []
        self.Path4 = []
        self.Path5 = []
        self.Battle_Data = battle_data
        self.image = map_image
        
    def process_map_data(self):
        #Grabs Grid info as well as movement points
        for layer in self.Battle_Data["layers"]:
            
            if layer["name"] == "Tile Layer 1":
                self.Battle_points = layer["data"]
              

            elif layer["name"] == "Path 1":
                for obj in layer["objects"]:  
                  Path_Data = obj["polyline"]
                  Path_DataX = obj["x"]
                  Path_DataY = obj["y"]
             
                  self.process_Path1(Path_DataX, Path_DataY, Path_Data)
          
            elif layer["name"] == "Path 2":
                for obj in layer["objects"]:  
                  Path_Data = obj["polyline"]
                  Path_DataX = obj["x"]
                  Path_DataY = obj["y"]
             
                  self.process_Path2(Path_DataX, Path_DataY, Path_Data)
          
            elif layer["name"] == "Path 3":
                for obj in layer["objects"]:  
                  Path_Data = obj["polyline"]
                  Path_DataX = obj["x"]
                  Path_DataY = obj["y"]
             
                  self.process_Path3(Path_DataX, Path_DataY, Path_Data)
          
            elif layer["name"] == "Path 4":
                for obj in layer["objects"]:  
                  Path_Data = obj["polyline"]
                  Path_DataX = obj["x"]
                  Path_DataY = obj["y"]
             
                  self.process_Path4(Path_DataX, Path_DataY, Path_Data)
          
            elif layer["name"] == "Path 5":
                for obj in layer["objects"]:  
                  Path_Data = obj["polyline"]
                  Path_DataX = obj["x"]
                  Path_DataY = obj["y"]
             
                  self.process_Path5(Path_DataX, Path_DataY, Path_Data)

    def process_Path1(self,Px,Py, data):
        for point in data:
            temp_x = point.get("x")
            self.Path1.append((Px + temp_x,Py))
    
    def process_Path2(self,Px,Py, data):
        for point in data:
            temp_x = point.get("x")
            self.Path2.append((Px + temp_x,Py))

    def process_Path3(self,Px,Py, data):
        for point in data:
            temp_x = point.get("x")
            self.Path3.append((Px + temp_x,Py))
    
    def process_Path4(self,Px,Py, data):
        for point in data:
            temp_x = point.get("x")
            self.Path4.append((Px + temp_x,Py))

    def process_Path5(self,Px,Py, data):
        for point in data:
            temp_x = point.get("x")
            self.Path5.append((Px + temp_x,Py))

        
    def draw(self, surface):
        surface.blit(self.image, (0, 0))

        


